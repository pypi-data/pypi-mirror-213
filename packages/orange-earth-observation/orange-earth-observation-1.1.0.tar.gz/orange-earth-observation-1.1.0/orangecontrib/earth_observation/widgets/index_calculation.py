import os
import shapefile
import rasterio
import numpy as np
import xarray as xr
from matplotlib import pyplot as plt
from rasterio.mask import mask
from rasterio.crs import CRS
from rasterio.warp import transform_bounds, calculate_default_transform, \
    reproject, Resampling
from Orange.widgets import widget, gui, settings
from Orange.widgets.utils.signals import Input, Output
from PyQt5.QtCore import Qt
from AnyQt.QtWidgets import QAction, QFileDialog, QPushButton
from drb.core import DrbNode
from drb.drivers.file import DrbFileFactory, DrbFileNode
from drb.drivers.zip import DrbBaseZipNode
from drb.drivers.image import DrbImageFactory, DrbImageBaseNode
from .utils import RegexNamePredicate
import drb.topics.resolver as resolver


class OWIndexCalculation(widget.OWWidget):
    name = "EO Index Calculation"
    description = "Calculates a selected index from" \
                  " Sentinel 2 band composition"

    icon = "icons/calculate.svg"
    priority = 100

    indices = ["NDVI", "NDMI", "NDWI", "NBR"]
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
            label="Choose Index:",
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

            b1 = b2 = []
            # NDVI
            if idx == 0:
                b1 = self.node[0]['GRANULE'][0]['IMG_DATA'][
                    'R20m'][RegexNamePredicate(".*B8A*")]
                b2 = self.node[0]['GRANULE'][0]['IMG_DATA'][
                    'R20m'][RegexNamePredicate(".*B04*")]
            # NDMI
            elif idx == 1:
                b1 = self.node[0]['GRANULE'][0]['IMG_DATA'][
                    'R20m'][RegexNamePredicate(".*B8A*")]
                b2 = self.node[0]['GRANULE'][0]['IMG_DATA'][
                    'R20m'][RegexNamePredicate(".*B11*")]
            # NDWI
            elif idx == 2:
                b1 = self.node[0]['GRANULE'][0]['IMG_DATA'][
                    'R20m'][RegexNamePredicate(".*B03*")]
                b2 = self.node[0]['GRANULE'][0]['IMG_DATA'][
                    'R20m'][RegexNamePredicate(".*B8A*")]
            # NBR
            elif idx == 3:
                b1 = self.node[0]['GRANULE'][0]['IMG_DATA'][
                    'R20m'][RegexNamePredicate(".*B12*")]
                b2 = self.node[0]['GRANULE'][0]['IMG_DATA'][
                    'R20m'][RegexNamePredicate(".*B8A*")]

            b1_ds = b1[0].get_impl(rasterio.DatasetReader)
            b2_ds = b2[0].get_impl(rasterio.DatasetReader)
            profile = b1_ds.meta.copy()

            b1_img = b1_ds.read().astype(np.float32)
            b2_img = b2_ds.read().astype(np.float32)

            # Small constant value to prevent division by zero
            epsilon = 0.0001
            out_image = (b1_img - b2_img) / (b1_img + b2_img + epsilon)

            profile.update({
                "driver": 'GTiff',
                "dtype": 'float32',
                "count": 1,
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
    WidgetPreview(OWIndexCalculation).run()
