import os
import rasterio
import numpy as np
from Orange.widgets import widget, gui, settings
from Orange.widgets.utils.signals import Input, Output
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAction, QFileDialog, QPushButton
from drb.core import DrbNode
from drb.drivers.file import DrbFileFactory, DrbFileNode
from drb.drivers.zip import DrbBaseZipNode
from drb.drivers.image import DrbImageFactory, DrbImageBaseNode
from .utils import RegexNamePredicate
import drb.topics.resolver as resolver
from rasterio.crs import CRS


class OWRGBCalculation(widget.OWWidget):
    name = "EO RGB Calculation"
    description = "Calculates a RGB color composition from" \
                  " Sentinel 2 band composition"

    icon = "icons/calculate.svg"
    priority = 110

    indices = ["TCI", "Burnt_composition"]
    node = None
    nodes = []
    files = []

    want_main_area = False
    graph_name = "thumbnailView"
    auto_commit = settings.Setting(True)

    class Inputs:
        dir = Input("Dir", str, auto_summary=False)
        data = Input("DrbNode", DrbNode, auto_summary=False)

    class Outputs:
        output = Output("Dir", str, auto_summary=False)

    def __init__(self):
        super().__init__()
        self.output = None

        self.combobox_node = gui.comboBox(
            self.controlArea, self, "", items=self.nodes,
            box="Select Node:",
            contentsLength=12,
        )
        self.combobox_node.activated.connect(self._select_node)
        gui.rubber(self.controlArea)

        self.box = gui.widgetBox(self.controlArea, " ")
        self.combobox_index = gui.comboBox(
            self.box, self, "", items=self.indices,
            label="Choose RGB composition:",
            orientation=Qt.Horizontal,
            contentsLength=12,
        )

        self.button = gui.button(
            self.box, self, "Calculate",
            callback=self.calculate
        )

        gui.rubber(self.controlArea)
        self.button_for_all = gui.button(
            self.controlArea, self, "Calculate for All",
            callback=self.calculate_for_all
        )

        gui.rubber(self.controlArea)
        gui.auto_commit(self.buttonsArea, self,
                        "auto_commit", "Send", box=False)

    def calculate(self):
        if self.nodes:
            idx = self.combobox_index.currentIndex()
            idx_name = self.indices[idx]

            dirname = os.path.dirname(self.node.path.path)
            filename = os.path.splitext(
                os.path.basename(self.node.path.path))[0]
            path = os.path.join(dirname + f'/{idx_name}')

            if not os.path.exists(path):
                os.mkdir(path)

            # TCI
            if idx == 0:
                btci = self.node[0]['GRANULE'][0]['IMG_DATA'][
                    'R10m'][RegexNamePredicate(".*TCI*")]
                btci_ds = btci[0].get_impl(rasterio.DatasetReader)
                profile = btci_ds.meta.copy()
                print(profile)
                out_image = btci_ds.read().astype(np.uint8)

            # Burnt Color
            elif idx == 1:
                red = self.node[0]['GRANULE'][0]['IMG_DATA'][
                    'R20m'][RegexNamePredicate(".*B12*")]
                green = self.node[0]['GRANULE'][0]['IMG_DATA'][
                    'R20m'][RegexNamePredicate(".*B11*")]
                blue = self.node[0]['GRANULE'][0]['IMG_DATA'][
                    'R20m'][RegexNamePredicate(".*B8A*")]

                red_ds = red[0].get_impl(rasterio.DatasetReader)
                green_ds = green[0].get_impl(rasterio.DatasetReader)
                blue_ds = blue[0].get_impl(rasterio.DatasetReader)

                profile = red_ds.meta.copy()
                print(profile)

                ratio14to8 = (2 ** 8 - 1) / (2 ** 14 - 1)

                min2 = (2 ** 14 - 1)
                max2 = 0

                red_image = red_ds.read().astype(np.float32)
                m2 = np.mean(red_image[red_image > 0])
                sig2 = np.std(red_image[red_image > 0])
                if (m2 - 2 * sig2) < min2:
                    min2 = (m2 - 2 * sig2)
                if (m2 + 2 * sig2) > max2:
                    max2 = (m2 + 2 * sig2)

                green_image = green_ds.read().astype(np.float32)
                m2 = np.mean(green_image[green_image > 0])
                sig2 = np.std(green_image[green_image > 0])
                if (m2 - 2 * sig2) < min2:
                    min2 = (m2 - 2 * sig2)
                if (m2 + 2 * sig2) > max2:
                    max2 = (m2 + 2 * sig2)

                blue_image = blue_ds.read().astype(np.float32)
                m2 = np.mean(blue_image[blue_image > 0])
                sig2 = np.std(blue_image[blue_image > 0])
                if (m2 - 2 * sig2) < min2:
                    min2 = (m2 - 2 * sig2)
                if (m2 + 2 * sig2) > max2:
                    max2 = (m2 + 2 * sig2)

                ratio14to8 = (2 ** 8 - 1) / (max2 - min2)

                red_image = (red_image - min2) * ratio14to8
                green_image = (green_image - min2) * ratio14to8
                blue_image = (blue_image - min2) * ratio14to8

                (z, w, h) = red_image.shape
                out_image = np.zeros((3, w, h), np.uint8)
                out_image[0] = red_image.astype(np.uint8)
                out_image[1] = green_image.astype(np.uint8)
                out_image[2] = blue_image.astype(np.uint8)
            profile.update({
                "driver": 'GTiff',
                "dtype": 'uint8',
                "count": 3,
            })

            with rasterio.open(os.path.join(
                    path + f'/{filename}.tif'), "w", **profile) as dst:
                dst.write(out_image)

            self.output = path
            self.commit.deferred()

    def calculate_for_all(self):
        for node in self.nodes:
            self.node = node
            self.calculate()

    def _select_node(self):
        idx_node = self.combobox_node.currentIndex()
        self.node = self.nodes[idx_node]

    @Inputs.data
    def set_data(self, nodes):
        if not isinstance(nodes, list):
            self.nodes = [nodes]
            self.node = self.nodes[0]
        elif isinstance(nodes, list):
            self.nodes = nodes
            self.node = self.nodes[0]

        self.combobox_node.clear()
        self.combobox_node.addItems([node.name for node in self.nodes])

    @Inputs.dir
    def set_dir(self, dir):
        self.files = [os.path.join(dir, file) for file in os.listdir(dir)]
        nodes = [_load_file(file) for file in self.files]
        self.nodes = []
        for node in nodes:
            if isinstance(node, DrbBaseZipNode):
                self.nodes.append(node)
        self.combobox_node.clear()
        self.combobox_node.addItems([node.name for node in self.nodes])

    @gui.deferred
    def commit(self):
        """
        Commits the result the next widget in the line.
        """
        self.Outputs.output.send(self.output)


def _load_file(file):
    topic, file_node = resolver.resolve(file)

    return file_node


if __name__ == "__main__":
    from orangewidget.utils.widgetpreview import WidgetPreview
    WidgetPreview(OWRGBCalculation).run()
