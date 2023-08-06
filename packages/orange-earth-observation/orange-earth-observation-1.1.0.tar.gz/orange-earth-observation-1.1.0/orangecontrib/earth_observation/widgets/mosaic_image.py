import os
import rasterio
from rasterio.crs import CRS
from rasterio.merge import merge
from Orange.widgets import widget, gui, settings
from Orange.widgets.widget import Output, MultiInput
from drb.core import DrbNode
from drb.drivers.file import DrbFileFactory
from drb.drivers.image import DrbImageFactory, DrbImageBaseNode


class OWMosaicImage(widget.OWWidget):
    name = "EO Mosaic Image"
    description = "Creates a mosaic image of sentinel 2 parts," \
                  " corresponding to a predefined NUTS shape"
    icon = "icons/mosaic.svg"
    priority = 30

    epsg = settings.Setting([CRS.from_epsg(4326)])
    want_main_area = False
    graph_name = "thumbnailView"
    auto_commit = settings.Setting(True)

    class Inputs:
        data = MultiInput("List[DrbImageBaseNode]",
                          DrbImageBaseNode, auto_summary=False)

    class Outputs:
        output = Output("DrbImageBaseNode", DrbNode,
                        auto_summary=False)

    def __init__(self):
        super().__init__()
        self.nodes = []
        self.output = None

        self.combobox_epsg = gui.comboBox(
            self.controlArea, self, "", items=self.epsg,
            box="Input/Output CRS:",
            contentsLength=12,
        )

        gui.rubber(self.controlArea)
        box = gui.widgetBox(self.controlArea)
        self.button = gui.button(
            box, self, "Create Mosaic Image",
            callback=self.create_mosaic_image
        )

        gui.rubber(self.controlArea)
        gui.auto_commit(self.buttonsArea, self,
                        "auto_commit", "Send", box=False)

    def create_mosaic_image(self):

        path = os.path.splitext(self.nodes[0].path.path)[0]

        if not os.path.exists(path):
            os.mkdir(path)

        mosaics = []

        ds = self.nodes[0].get_impl(rasterio.DatasetReader)
        profile = ds.meta.copy()

        for image_node in self.nodes:
            ds = image_node.get_impl(rasterio.DatasetReader)
            mosaics.append(ds)

        mosaic, transform = merge(mosaics)
        profile.update({'height': mosaic.shape[1],
                        'width': mosaic.shape[2],
                        'transform': transform,
                        })

        with rasterio.open(os.path.join(path +
                                        '-mosaic-image_4326.tif'),
                           'w', **profile) as dst:
            dst.write(mosaic)

        self.output = _load_image(os.path.join(path +
                                               '-mosaic-image_4326.tif'))
        self.commit.deferred()

    @Inputs.data
    def set_data(self, index, node):

        if index == 0:
            if _check_crs_nuts_region(node):
                self.nodes = [node]

        else:
            if _check_crs_nuts_region(node):
                try:
                    self.nodes[index] = node
                except IndexError:
                    self.nodes.append(node)

    @Inputs.data.insert
    def insert_data(self, index, node: DrbImageBaseNode):
        if index == 0:
            if _check_crs_nuts_region(node):
                self.nodes = [node]

        else:
            if _check_crs_nuts_region(node):
                self.nodes.append(node)

    @Inputs.data.remove
    def remove_data(self, index):
        self.nodes.pop(index)

        if not self.nodes:
            self.combobox_node.clear()

    @gui.deferred
    def commit(self):
        """
        Commits the result the next widget in the line.
        """
        self.Outputs.output.send(self.output)


def _check_crs_nuts_region(node):
    """
    Checks if input images have identical CRS projection.
    Parameters:
        node (DrbImageBaseNode): Drb node to check
    Returns:
        bool: True if identical CRS with the previous node
    """

    ds = node.get_impl(rasterio.DatasetReader)
    if ds.crs == CRS.from_epsg(4326):
        return True

    return False


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
    WidgetPreview(OWMosaicImage).run()
