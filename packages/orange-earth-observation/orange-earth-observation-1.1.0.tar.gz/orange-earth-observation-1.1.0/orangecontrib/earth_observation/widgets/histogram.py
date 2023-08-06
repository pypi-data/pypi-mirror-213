import numpy as np
import cv2
import os
import rasterio
import matplotlib.pyplot as plt
from Orange.widgets import widget, gui
from Orange.widgets.widget import Output, MultiInput
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QGraphicsView
from Orange.widgets import settings
from skimage.exposure import match_histograms
from drb.drivers.file import DrbFileFactory
from drb.drivers.image import DrbImageFactory, DrbImageBaseNode


class OWHistogram(widget.OWWidget):
    name = "EO Histogram"
    description = "Visualize histogram of an image" \
                  " and performs contrast adjustment"
    icon = "icons/histogram.svg"
    priority = 60

    input_nodes = []
    output_node = None

    clip_limit = settings.Setting(2)

    want_main_area = True
    graph_name = "thumbnailView"
    auto_commit = settings.Setting(True)

    class Inputs:
        data = MultiInput("List[DrbImageBaseNode]",
                          DrbImageBaseNode, auto_summary=False)

    class Outputs:
        output = Output("DrbImageBaseNode",
                        DrbImageBaseNode, auto_summary=False)

    def __init__(self):
        super().__init__()
        self.output = None

        self.combobox_node = gui.comboBox(
            self.controlArea, self, "",
            box="Select Input Image:",
            contentsLength=12,
        )

        self.combobox_node.activated.connect(self._show_histogram)
        gui.rubber(self.controlArea)

        self.histogram_box = gui.widgetBox(self.controlArea, " ")
        gui.rubber(self.controlArea)

        self.basic_button = gui.button(
            self.histogram_box, self, "Basic Hist Equalization",
            callback=self.basic_hist_equalize
        )

        self.slider = gui.hSlider(
            self.histogram_box, self, "clip_limit",
            label="Select Clip Limit:", minValue=1, maxValue=100, step=1,
            orientation=Qt.Horizontal,
            width=200,
        )

        self.adaptive_button = gui.button(
            self.histogram_box, self, "Adaptive Hist Equalization",
            callback=self.adaptive_hist_equalize
        )

        self.match_box = gui.widgetBox(self.controlArea, " ")
        gui.rubber(self.controlArea)

        self.combobox_reference = gui.comboBox(
            self.match_box, self, "",
            label="Select Reference Image:",
            contentsLength=12,
        )
        self.combobox_to_match = gui.comboBox(
            self.match_box, self, "",
            label="Select Image to Match:",
            contentsLength=12,
        )

        self.match_button = gui.button(
            self.match_box, self, "Match Histograms",
            callback=self.match_histograms
        )

        gui.rubber(self.controlArea)
        gui.auto_commit(self.buttonsArea, self,
                        "auto_commit", "Send", box=False)

        gui.vBox(self.mainArea)
        self.box_scene = QGraphicsScene(self)
        self.box_view = QGraphicsView(self.box_scene)

        self.layout = self.mainArea.layout()
        self.layout.addWidget(self.box_view)

        self.mainArea.setMinimumWidth(100)

    def match_histograms(self):
        """
        Matches histograms of the images, one is chosen to be reference.
        """
        ds, filename, path = self.__read_image(self.combobox_to_match)
        profile = ds.meta.copy()
        image_to_match = ds.read()
        image_to_match = np.moveaxis(image_to_match, 0, -1)

        ds, x, x = self.__read_image(self.combobox_reference)
        ref_image = ds.read()
        ref_image = np.moveaxis(ref_image, 0, -1)

        matched_image = match_histograms(image_to_match,
                                         ref_image, channel_axis=2)
        # matched_image = rescale_intensity(matched_image, out_range=(1, 255))

        with rasterio.open(os.path.join(
                path + f'/{filename}.tif'), 'w', **profile) as dst:
            dst.write(np.moveaxis(matched_image, -1, 0))

        hist_size = 2 ** 8 - 1
        hist_range = (1, 2 ** 8 - 1)

        h1 = cv2.calcHist([ref_image], [0], None, [hist_size], hist_range)
        h2 = cv2.calcHist([matched_image], [0], None, [hist_size], hist_range)

        self.__plot([h1, h2], path, filename)

        self.output = _load_image(os.path.join(path + f'/{filename}.tif'))
        print(self.output)
        self.commit.deferred()

    def basic_hist_equalize(self):

        ds, filename, path = self.__read_image(self.combobox_node)
        profile = ds.meta.copy()
        image = ds.read()

        # convert image from RGB to HSV
        image = np.moveaxis(image, 0, -1)
        img_hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

        # Histogram equalisation on the V-channel
        img_hsv[:, :, 2] = cv2.equalizeHist(img_hsv[:, :, 2])

        # convert image back from HSV to RGB
        equalized_image = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2RGB)

        with rasterio.open(os.path.join(
                path + f'/{filename}.tif'), 'w', **profile) as dst:
            dst.write(np.moveaxis(equalized_image, -1, 0))

        hist_size = 2 ** 8 - 1
        hist_range = (1, 2 ** 8 - 1)

        h1 = cv2.calcHist([image], [0], None, [hist_size], hist_range)
        h2 = cv2.calcHist([equalized_image], [0], None,
                          [hist_size], hist_range)

        self.__plot([h1, h2], path, filename)

        self.output = _load_image(os.path.join(path + f'/{filename}.tif'))
        self.commit.deferred()

    def adaptive_hist_equalize(self):
        """ CLAHE is a variant of Adaptive histogram
        equalization (AHE) which takes care of over-amplification of
        the contrast. CLAHE operates on small regions in the image,
        called tiles, rather than the entire image.
        The neighboring tiles are then combined using bi-linear
        interpolation to remove the artificial boundaries.
        This algorithm can be applied to improve the contrast of images.
        We can also apply CLAHE to color images, where usually it is
        applied on the luminance channel and the results after equalizing
        only the luminance channel of an HSV image
        are much better than equalizing all the channels of the BGR image """

        ds, filename, path = self.__read_image(self.combobox_node)
        profile = ds.meta.copy()
        image = ds.read()

        # convert image from RGB to LAB
        image = np.moveaxis(image, 0, -1)
        img_lab = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)

        # Applying CLAHE to L-channel
        # the risk is to over-amplify noise in relatively homogeneous
        # regions of the image, by using different values for the
        # contrast limit, the upper limit should be determined
        # and used carefully. From one image to another, this can be variable.
        cl = self.clip_limit
        clahe = cv2.createCLAHE(clipLimit=cl, tileGridSize=(2, 2))
        img_lab[:, :, 0] = clahe.apply(img_lab[:, :, 0])

        img_lab[:, :, 0] = cv2.equalizeHist(img_lab[:, :, 0])

        # convert image back from LAB to RGB
        equalized_image = cv2.cvtColor(img_lab, cv2.COLOR_LAB2RGB)

        with rasterio.open(os.path.join(
                path + f'/{filename}.tif'), 'w', **profile) as dst:
            dst.write(np.moveaxis(equalized_image, -1, 0))

        hist_size = 2 ** 8 - 1
        hist_range = (1, 2 ** 8 - 1)

        h1 = cv2.calcHist([image], [0], None, [hist_size], hist_range)
        h2 = cv2.calcHist([equalized_image],
                          [0], None, [hist_size], hist_range)

        self.__plot([h1, h2], path, filename)

        self.output = _load_image(os.path.join(path + f'/{filename}.tif'))
        self.commit.deferred()

    def _show_histogram(self):

        ds, filename, path = self.__read_image(self.combobox_node)
        image = ds.read()
        image = np.moveaxis(image, 0, -1)

        hist_size = 2 ** 8 - 1
        hist_range = [1, 2 ** 8 - 1]

        hist = cv2.calcHist([image], [0], None, [hist_size], hist_range)
        self.__plot([hist], path, filename)

        self.combobox_reference.clear()
        self.combobox_reference.addItems(
            [node.name for node in self.input_nodes])

        self.combobox_to_match.clear()
        self.combobox_to_match.addItems(
            [node.name for node in self.input_nodes])

    def __read_image(self, combobox):
        idx_node = combobox.currentIndex()
        image_node = self.input_nodes[idx_node]

        path = image_node.path.path
        name = os.path.basename(path)
        filename = os.path.splitext(name)[0]

        path_r = os.path.join(os.path.dirname(path), 'histogram')

        if not os.path.exists(path_r):
            os.mkdir(os.path.join(os.path.dirname(path), 'histogram'))

        ds = image_node.get_impl(rasterio.DatasetReader)

        return ds, filename, path_r

    def __plot(self, hist, path, filename):

        plt.figure()
        for h in hist:
            try:
                plt.plot(h)
            except ValueError:
                plt.plot(h[0])
        plt.xlim([0, 256])
        # plt.show()
        plt.savefig(os.path.join(path + f'/{filename}.png'))

        pic = QGraphicsPixmapItem()
        pic.setPixmap(QPixmap(os.path.join(path + f'/{filename}.png')))
        self.box_scene.addItem(pic)

    @Inputs.data
    def set_data(self, index, node):
        try:
            self.input_nodes[index] = node
        except IndexError:
            self.input_nodes.append(node)

        self.combobox_node.clear()
        self.combobox_node.addItems([node.name for node in self.input_nodes])

    @Inputs.data.insert
    def insert_data(self, index, node: DrbImageBaseNode):

        if index == 0:
            self.input_nodes = []

        self.input_nodes.append(node)
        self.combobox_node.clear()
        self.combobox_node.addItems([node.name for node in self.input_nodes])

    @Inputs.data.remove
    def remove_data(self, index):
        self.input_nodes.pop(index)
        self.combobox_node.clear()
        self.combobox_node.addItems([node.name for node in self.input_nodes])

        if not self.input_nodes:
            self.combobox_node.clear()

    @gui.deferred
    def commit(self):
        """
        Commits the result the next widget in the line.
        """
        self.Outputs.output.send(self.output)


def _load_image(file):
    """
    Loads and create a DrbImageBaseNode from local file.
    Parameters:
        file (str): path to local file
    Returns:
        DrbImageBaseNode: a Drb Node of the TC Image
    """
    base_node = DrbFileFactory().create(file)
    image_node = DrbImageFactory().create(base_node)

    return image_node


if __name__ == "__main__":
    from orangewidget.utils.widgetpreview import WidgetPreview
    WidgetPreview(OWHistogram).run()
