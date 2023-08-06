import os
import rasterio
from rasterio.crs import CRS
from rasterio.warp import calculate_default_transform, reproject, Resampling
from Orange.widgets import widget, gui, settings
from Orange.widgets.utils.signals import Input, Output
from drb.drivers.file import DrbFileFactory
from drb.drivers.image import DrbImageFactory, DrbImageBaseNode


class OWReprojectImage(widget.OWWidget):
    name = "EO Reproject Image"
    description = "Projects an image into a different CRS"
    icon = "icons/projection.svg"
    priority = 40

    epsg = []
    output_epsg = settings.Setting(4326)
    node = None

    want_main_area = False
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
        self.output = None

        self.combobox = gui.comboBox(
            self.controlArea, self, "", items=self.epsg,
            box="Selected Input CRS:",
            contentsLength=12,
        )

        box1 = gui.vBox(self.controlArea, 'Select Output CRS:')
        gui.spin(box1, self, 'output_epsg', 1, 100000,
                 label='                       EPSG:')

        gui.rubber(self.controlArea)

        box2 = gui.widgetBox(self.controlArea)
        self.button = gui.button(
            box2, self, "Reproject Image", callback=self.reproject_image
        )

        gui.rubber(self.controlArea)
        gui.auto_commit(self.buttonsArea, self,
                        "auto_commit", "Send", box=False)

    def reproject_image(self):

        path = self.node.path.path
        output_crs = CRS.from_epsg(self.output_epsg)

        image_node = self.node
        name = os.path.basename(path)
        filename = os.path.splitext(name)[0]
        filename = filename.split('_')[0] + f'_{output_crs}'

        src = image_node.get_impl(rasterio.DatasetReader)

        transform, width, height = calculate_default_transform(
            src.crs, output_crs, src.width, src.height, *src.bounds)
        kwargs = src.meta.copy()
        kwargs.update({

            'driver': 'GTiff',
            'crs': output_crs,
            'transform': transform,
            'width': width,
            'height': height
        })

        with rasterio.open(os.path.join(os.path.dirname(
                path) + f'/{filename}.tif'), 'w', **kwargs) as dst:
            for i in range(1, src.count + 1):
                reproject(
                    source=rasterio.band(src, i),
                    destination=rasterio.band(dst, i),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=transform,
                    dst_crs=output_crs,
                    resampling=Resampling.nearest)

        self.output = _load_image(os.path.join(
            os.path.dirname(path) + f'/{filename}.tif'))
        self.commit.deferred()

    @Inputs.data
    def set_data(self, node):

        self.node = node
        if self.node:
            ds = self.node.get_impl(rasterio.DatasetReader)
            self.epsg = [CRS.to_epsg(ds.crs)]

            self.combobox.clear()  # delete all items from comboBox
            self.combobox.addItems([f'EPSG: {epsg}' for epsg in self.epsg])

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
    WidgetPreview(OWReprojectImage).run()
