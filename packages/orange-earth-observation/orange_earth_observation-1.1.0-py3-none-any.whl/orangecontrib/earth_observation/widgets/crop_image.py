import cv2
import os
import rasterio
from Orange.widgets import widget, gui
from Orange.widgets.utils.signals import Input, Output
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtWidgets import (QGraphicsScene, QGraphicsView,
                             QGraphicsPixmapItem,
                             QGraphicsRectItem, QGraphicsItem)
from Orange.widgets import settings
from drb.drivers.file import DrbFileFactory
from drb.drivers.image import DrbImageFactory, DrbImageBaseNode


class OWCropImage(widget.OWWidget):
    name = "EO Crop Image"
    description = "Crops the image into a selected area"
    icon = "icons/crop.svg"
    priority = 70

    rectangle = None
    output_image = None

    reduction_value = settings.Setting(1)
    crop_size = 100
    x = 10
    y = 10

    want_main_area = True
    graph_name = "thumbnailView"
    auto_commit = settings.Setting(True)

    class Inputs:
        data = Input("DrbImageBaseNode",
                     DrbImageBaseNode, auto_summary=False)

    class Outputs:
        output = Output("DrbImageBaseNode",
                        DrbImageBaseNode, auto_summary=False)

    def __init__(self):
        super().__init__()
        self.node = None
        self.output = None

        slider1 = gui.hSlider(
            self.controlArea, self, "crop_size",
            box="Select Crop Size:", minValue=10, maxValue=100, step=10,
            callback=self._update_rect_size,
            width=200,
        )
        slider1.sliderReleased.connect(self._on_slider_release)

        slider2 = gui.hSlider(
            self.controlArea, self, "x",
            box="Horizontal Range X: ", minValue=0, maxValue=512, step=10,
            callback=self._update_rect_size,
            width=200,
        )
        slider2.sliderReleased.connect(self._on_slider_release)

        slider3 = gui.hSlider(
            self.controlArea, self, "y",
            box="Vertical Range Y:", minValue=0, maxValue=512, step=10,
            callback=self._update_rect_size,
            width=200,
        )
        slider3.sliderReleased.connect(self._on_slider_release)

        gui.rubber(self.controlArea)

        box = gui.widgetBox(self.controlArea)
        self.button = gui.button(
            box, self, "Crop Image",
            callback=self.crop_image
        )

        gui.rubber(self.controlArea)
        gui.auto_commit(self.buttonsArea, self,
                        "auto_commit", "Send", box=False)

        # Main area box
        gui.vBox(self.mainArea)
        self.main_box_scene = QGraphicsScene(self)
        self.main_box_view = QGraphicsView(self.main_box_scene)

        self.main_layout = self.mainArea.layout()
        self.main_layout.addWidget(self.main_box_view)

        self.crop_box_scene = QGraphicsScene(self)
        self.crop_box_view = QGraphicsView(self.crop_box_scene)

        self.crop_layout = self.mainArea.layout()
        self.crop_layout.addWidget(self.crop_box_view)

        self.mainArea.setMinimumWidth(100)

    def crop_image(self):
        """
        On slider release, shows a miniature of the cropped image.
        """
        with rasterio.open(os.path.join(os.path.dirname(
                self.path) + f'/{self.filename}.tif'), 'w',
                           **self.profile) as dst:
            dst.write(self.output_image)

        self.output = _load_image(os.path.dirname(
            self.path) + f'/{self.filename}.tif')
        self.commit.deferred()

    def _on_slider_release(self):
        """
        On slider release, shows a miniature of the cropped image.
        This function calculates the crop window in the original image.
        """
        self.path = self.node.path.path
        name = os.path.basename(self.path)
        self.filename = os.path.splitext(name)[0] + '-crop-image'

        ds = self.node.get_impl(rasterio.DatasetReader)
        self.profile = ds.meta.copy()

        # height and width in the original image
        h = self.y / self.reduction_h
        w = self.x / self.reduction_w

        h_n = (self.y + self.crop_size) / self.reduction_h
        w_n = (self.x + self.crop_size) / self.reduction_w

        h_p = (self.y - self.crop_size) / self.reduction_h
        w_p = (self.x - self.crop_size) / self.reduction_w

        if h_n > ds.shape[0] and w_n > ds.shape[1]:
            crop_image = ds.read(window=((h_p, h), (w_p, w)))

        elif h_n > ds.shape[0] and w_n < ds.shape[1]:
            crop_image = ds.read(window=((h_p, h), (w, w_n)))

        elif h_n < ds.shape[0] and w_n > ds.shape[1]:
            crop_image = ds.read(window=((h, h_n), (w_p, w)))

        else:
            crop_image = ds.read(window=((h, h_n), (w, w_n)))

        self.output_image = crop_image

        # show a PNG thumbnail of the cropped image
        crop_image = cv2.resize(crop_image[1, :, :], (256, 256))

        cv2.imwrite(os.path.join(os.path.dirname(
            self.path) + f'/{self.filename}.png'), crop_image)
        pic = QGraphicsPixmapItem()
        pic.setPixmap(QPixmap(os.path.join(os.path.dirname(
            self.path) + f'/{self.filename}.png')))
        self.crop_box_scene.addItem(pic)

    def _update_rect_size(self):
        """
        Modifies the size of the ROI rectangle upon slider modification.
        """
        if self.rectangle is not None:
            self.main_box_scene.removeItem(self.rectangle)
        if self.x + self.crop_size > 512 and self.y + self.crop_size > 512:
            self.rectangle = QGraphicsRectItem(
                QRectF(self.x - self.crop_size, self.y -
                       self.crop_size, self.crop_size, self.crop_size))
            self.rectangle.setPen(Qt.red)

        elif self.x + self.crop_size > 512 > self.y + self.crop_size:
            self.rectangle = QGraphicsRectItem(
                QRectF(self.x - self.crop_size, self.y,
                       self.crop_size, self.crop_size))
            self.rectangle.setPen(Qt.red)
        elif self.x + self.crop_size < 512 < self.y + self.crop_size:
            self.rectangle = QGraphicsRectItem(
                QRectF(self.x, self.y - self.crop_size,
                       self.crop_size, self.crop_size))
            self.rectangle.setPen(Qt.red)
        else:
            self.rectangle = QGraphicsRectItem(
                QRectF(self.x, self.y, self.crop_size, self.crop_size))
            self.rectangle.setPen(Qt.red)

        # self.rectangle.setFlag(QGraphicsItem.ItemIsMovable)
        self.main_box_scene.addItem(self.rectangle)

    def _show_image(self):
        """
        Show the original image in a reduced (512,512) size.
        This function initializes variables corresponding to height's
        and width's reduction rate.
        """
        ds = self.node.get_impl(rasterio.DatasetReader)
        full_image = ds.read(1)

        image = cv2.resize(full_image, (512, 512))

        # height's and width's reduction rate
        self.reduction_h = 512 / full_image.shape[0]
        self.reduction_w = 512 / full_image.shape[1]

        path = self.node.path.path
        name = os.path.basename(path)
        filename = os.path.splitext(name)[0]

        cv2.imwrite(os.path.join(os.path.dirname(path) +
                                 f'/{filename}.png'), image)

        # show a PNG thumbnail of the original image
        pic = QGraphicsPixmapItem()
        pic.setPixmap(QPixmap(os.path.join(
            os.path.dirname(path) + f'/{filename}.png')))
        self.main_box_scene.addItem(pic)

    @Inputs.data
    def set_data(self, node):

        self.node = node
        if self.node:
            self._show_image()
        self.commit.now()

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
        DrbImageBaseNode: a Drb Node of the TC Image.
    """
    base_node = DrbFileFactory().create(file)
    image_node = DrbImageFactory().create(base_node)

    return image_node


if __name__ == "__main__":
    from orangewidget.utils.widgetpreview import WidgetPreview
    WidgetPreview(OWCropImage).run()
