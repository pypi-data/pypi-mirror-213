import os
import shapefile
import rasterio
from rasterio.mask import mask
from rasterio.crs import CRS
from rasterio.warp import transform_bounds, calculate_default_transform, \
    reproject, Resampling
from Orange.widgets import widget, gui, settings
from Orange.widgets.utils.signals import Input, Output
from PyQt5.QtWidgets import QAction, QFileDialog, QPushButton
from drb.core import DrbNode
from drb.drivers.file import DrbFileFactory
from drb.drivers.image import DrbImageFactory, DrbImageBaseNode
from .utils import RegexNamePredicate


class OWNUTSShape(widget.OWWidget):
    name = "EO NUTS Shape"
    description = "Applies on the given Sentinel 2 True Color image, " \
                  "a given mask corresponding to NUTS shape"
    icon = "icons/nuts.svg"
    priority = 20

    shape_recs = []
    nuts_available = []
    nodes = []

    want_main_area = False
    graph_name = "thumbnailView"
    auto_commit = settings.Setting(True)
    nuts_url = "https://gisco-services.ec.europa.eu/distribution/v2/nuts/" \
               "shp/NUTS_RG_20M_2021_4326.shp.zip"

    class Inputs:
        data = Input("DrbNode", DrbNode, auto_summary=False)

    class Outputs:
        output = Output("DrbImageBaseNode",
                        DrbImageBaseNode, auto_summary=False)

    def __init__(self):
        super().__init__()
        self.output = None

        self.combobox_node = gui.comboBox(
            self.controlArea, self, "", items=self.nodes,
            box="Select Node:",
            contentsLength=12,
        )
        self.combobox_node.activated.connect(self.__add_nuts_options)
        gui.rubber(self.controlArea)

        self.box = gui.widgetBox(self.controlArea, "Select NUTS Region:")
        self.combobox_nuts = gui.comboBox(
            self.box, self, "", items=self.nuts_available,
            contentsLength=12,
        )

        self.button = gui.button(
            self.box, self, "Apply NUTS Shape",
            callback=self.apply_nuts_shape
        )

        gui.rubber(self.controlArea)
        gui.auto_commit(self.buttonsArea, self,
                        "auto_commit", "Send", box=False)

    def apply_nuts_shape(self):

        if self.nodes:
            idx_nuts = self.combobox_nuts.currentIndex()

            shp = shapefile.Reader(self.nuts_url)
            shape_rec = self.shape_recs[idx_nuts]
            polygon = shape_rec[0]
            filename = shape_rec[1]
            shape = shp.shape(polygon)

            idx_node = self.combobox_node.currentIndex()
            node = self.nodes[idx_node]

            path = os.path.splitext(node.path.path)[0]

            if not os.path.exists(path):
                os.mkdir(path)

            if isinstance(node, DrbImageBaseNode):
                image_node = node
                ds = image_node.get_impl(rasterio.DatasetReader)

            else:
                bands = node[0]['GRANULE'][0]['IMG_DATA']['R60m']
                image_node = bands[RegexNamePredicate(".*TCI*")]
                ds = image_node[0].get_impl(rasterio.DatasetReader)

            if ds.crs == CRS.from_epsg(4326):
                image = ds
            else:
                image = self._reproject_image(ds, path)

            out_image, out_transform = mask(image, [shape], crop=True)

            out_meta = ({"height": out_image.shape[1],
                         "width": out_image.shape[2],
                         "transform": out_transform,
                         "driver": 'GTiff',
                         "dtype": 'uint8',
                         "count": 3,
                         "crs": CRS.from_epsg(4326)
                         })
            with rasterio.open(os.path.join(
                    path + f'/{filename}.tif'), "w", **out_meta) as dst:
                dst.write(out_image)

            self.output = _load_image(os.path.join(path + f'/{filename}.tif'))
            self.commit.deferred()

    @staticmethod
    def _reproject_image(ds, path):
        """
        Re-projects an image from a CRS to the (4326) CRS
        corresponding to the NUTS shapefile's projection.
        """
        crs_4326 = CRS.from_epsg(4326)

        src = ds
        transform, width, height = calculate_default_transform(
            src.crs, crs_4326, src.width, src.height, *src.bounds)
        kwargs = src.meta.copy()
        kwargs.update({
            'crs': crs_4326,
            'transform': transform,
            'width': width,
            'height': height,
            'driver': 'GTiff'
        })

        with rasterio.open(os.path.join(
                path, 'TCI_4326.tif'), 'w', **kwargs) as dst:

            for i in range(1, src.count + 1):
                reproject(
                    source=rasterio.band(src, i),
                    destination=rasterio.band(dst, i),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=transform,
                    dst_crs=crs_4326,
                    resampling=Resampling.nearest)

        reprojected_image = rasterio.open(os.path.join(
            path + '/TCI_4326.tif'))
        return reprojected_image

    def __add_nuts_options(self):
        """
        Adds a list of all available NUTS regions to
        the combobox for user to choose.
        """
        if self.nodes:
            idx = self.combobox_node.currentIndex()
            node = self.nodes[idx]

            if isinstance(node, DrbImageBaseNode):
                image_node = node
                ds = image_node.get_impl(rasterio.DatasetReader)

            else:
                bands = node[0]['GRANULE'][0]['IMG_DATA']['R60m']
                image_node = bands[RegexNamePredicate(".*TCI*")]
                ds = image_node[0].get_impl(rasterio.DatasetReader)

            if ds.crs == CRS.from_epsg(4326):
                bounds = ds.bounds
            else:
                bounds = transform_bounds(
                    ds.crs, CRS.from_epsg(4326), ds.bounds.left,
                    ds.bounds.bottom, ds.bounds.right, ds.bounds.top)
            shp = shapefile.Reader(self.nuts_url)

            self.shape_recs = [(shapeRec.record.oid,
                                f'NUTS {shapeRec.record[1]}'
                                f' - {shapeRec.record[3]}')
                               for shapeRec in
                               shp.iterShapeRecords(bbox=bounds)]

            self.nuts_available = [shapeRec[1] for shapeRec in self.shape_recs]

            self.combobox_nuts.clear()
            self.combobox_nuts.addItems(self.nuts_available)

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
    WidgetPreview(OWNUTSShape).run()
