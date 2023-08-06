import numpy as np
import os
import rasterio
from Orange.widgets import widget, gui
from Orange.widgets.utils.signals import Input, Output
from Orange.widgets import settings
from PyQt5.QtCore import Qt
from drb.core import DrbNode
from drb.drivers.file import DrbFileFactory
from drb.drivers.image import DrbImageFactory, DrbImageBaseNode
from .utils import RegexNamePredicate


class OWCloudMask(widget.OWWidget):
    name = "EO Cloud Mask"
    description = "Applies on the given Sentinel 2 True Color image, " \
                  "a given clouds, shadows, water or snow-ice mask"
    icon = "icons/cloud.svg"
    priority = 50

    mask_options = ["Clouds", 'Clouds and Shadow', "Water", "Snow--Ice"]
    nodes = []

    want_main_area = False
    graph_name = "thumbnailView"
    auto_commit = settings.Setting(True)

    class Inputs:
        data = Input("DrbNode", DrbNode, auto_summary=False)

    class Outputs:
        output = Output("DrbImageBaseNode",
                        DrbImageBaseNode, auto_summary=False)

    def __init__(self):
        super().__init__()
        self.output = None

        self.node_box = gui.widgetBox(self.controlArea, "Select Node: ")

        self.combobox_node = gui.comboBox(
            self.node_box, self, "",
            contentsLength=12,
        )

        gui.rubber(self.controlArea)
        self.mask_box = gui.widgetBox(self.controlArea, "Select Mask: ")

        self.combobox_masks = gui.comboBox(
            self.mask_box, self, "", items=self.mask_options,
            contentsLength=12,
        )

        self.button = gui.button(
            self.mask_box, self, "Apply Mask",
            callback=self.apply_mask
        )

        gui.rubber(self.controlArea)
        gui.auto_commit(self.buttonsArea, self,
                        "auto_commit", "Send", box=False)

    def apply_mask(self):

        if self.nodes:
            idx_node = self.combobox_node.currentIndex()
            node = self.nodes[idx_node]

            path = os.path.splitext(node.path.path)[0]

            if not os.path.exists(path):
                os.mkdir(path)

            bands = node[0]['GRANULE'][0]['IMG_DATA']['R60m']

            mask_node = bands[RegexNamePredicate(".*SCL*")]
            ds_mask = mask_node[0].get_impl(rasterio.DatasetReader)
            mask = ds_mask.read()

            image_node = bands[RegexNamePredicate(".*TCI*")]
            ds_image = image_node[0].get_impl(rasterio.DatasetReader)
            image = ds_image.read()
            profile = ds_image.meta.copy()

            idx = self.combobox_masks.currentIndex()
            mask_name = self.mask_options[idx]

            # preparing mask based on user selection
            if idx == 0:  # Clouds

                mask1 = (mask != 8).astype(int)
                mask2 = (mask != 9).astype(int)
                mask3 = (mask != 10).astype(int)

                prep_mask = np.logical_and(mask1, mask2).astype(int)
                prep_mask = np.logical_and(prep_mask, mask3).astype(int)

            if idx == 1:  # Shadows

                mask1 = (mask != 8).astype(int)
                mask2 = (mask != 9).astype(int)
                mask3 = (mask != 3).astype(int)
                mask4 = (mask != 10).astype(int)

                prep_mask = np.logical_and(mask1, mask2).astype(int)
                prep_mask = np.logical_and(prep_mask, mask3).astype(int)
                prep_mask = np.logical_and(prep_mask, mask4).astype(int)

            if idx == 2:  # Water
                prep_mask = (mask != 6).astype(int)

            if idx == 3:  # Snow/Ice
                prep_mask = (mask != 11).astype(int)

            prep_mask = np.moveaxis(prep_mask, 0, -1)
            image = np.moveaxis(image, 0, -1)
            result_image = image * prep_mask
            result_image = np.moveaxis(result_image, -1, 0)

            profile.update({
                'driver': 'GTiff',
            })

            with rasterio.open(os.path.join(
                    path + f'/TCI-without-{mask_name}.tif'),
                    'w', **profile) as dst:
                dst.write(result_image)

            self.output = _load_image(os.path.join(
                path + f'/TCI-without-{mask_name}.tif'))
            self.commit.deferred()

    @Inputs.data
    def set_data(self, nodes):
        if not isinstance(nodes, list):
            self.nodes = [nodes]
        elif isinstance(nodes, list):
            self.nodes = nodes

        self.combobox_node.clear()
        self.combobox_node.addItems([node.name for node in self.nodes])

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
    WidgetPreview(OWCloudMask).run()
