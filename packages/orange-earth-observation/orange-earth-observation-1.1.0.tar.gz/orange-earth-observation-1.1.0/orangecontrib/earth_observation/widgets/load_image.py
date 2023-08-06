from Orange.widgets import widget, gui, settings
from Orange.widgets.widget import Output
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QStyle
from PyQt5.QtWidgets import QAction, QFileDialog, QPushButton
from drb.drivers.file import DrbFileFactory
from drb.drivers.image import DrbImageFactory, DrbImageBaseNode
import os
import drb.topics.resolver as resolver


class OWLoadImage(widget.OWWidget):
    name = "EO Load Image"
    description = "Loads image(s) from the directory structure"
    icon = "icons/load.svg"
    priority = 90

    current_path = None
    file = []
    image = []
    want_main_area = False
    graph_name = "thumbnailView"
    auto_commit = settings.Setting(True)

    class Outputs:
        output = Output("DrbImageBaseNode",
                        DrbImageBaseNode, auto_summary=False)

    def __init__(self):
        super().__init__()
        self.output = None

        browse_action_file = QAction(
            self,
            text="\N{HORIZONTAL ELLIPSIS}",
        )

        browse_action_file.triggered.connect(self.__show_open_dialog_file)
        browse_button_file = QPushButton(
            browse_action_file.iconText(),
            clicked=browse_action_file.trigger
        )

        vbox = gui.vBox(self.controlArea, box="Select product file:")
        hbox = gui.hBox(vbox)
        hbox.layout().addWidget(browse_button_file)

        gui.rubber(self.controlArea)
        self.combobox_file = gui.comboBox(
            vbox, self, "", items=self.file,
            contentsLength=12,
        )

        browse_action = QAction(
            self,
            text="\N{HORIZONTAL ELLIPSIS}",
        )

        browse_action.triggered.connect(self.__show_open_dialog_image)
        browse_button = QPushButton(
            browse_action.iconText(),
            clicked=browse_action.trigger
        )

        vbox = gui.vBox(self.controlArea, box="Load image:")
        hbox = gui.hBox(vbox)
        hbox.layout().addWidget(browse_button)

        gui.rubber(self.controlArea)
        self.combobox_image = gui.comboBox(
            vbox, self, "", items=self.image,
            contentsLength=12,
        )

        gui.rubber(self.controlArea)
        gui.auto_commit(self.buttonsArea, self,
                        "auto_commit", "Send", box=False)

    @gui.deferred
    def commit(self):
        """
        Commits the result the next widget in the line.
        """
        if self.current_path:
            self.Outputs.output.send(self.output)

        else:
            self.Outputs.output.send(None)

    def __show_open_dialog_image(self):
        image, f = QFileDialog.getOpenFileName(
            self, 'Select directory/file', 'some/default/path/',
            'Image files(*.tif *.tiff *.image '
            '*.jp2 *.png *.gif *.webp *.bmp *.jpeg *.jpg *.blx '
            ' *.kap *.dt0 *.dt1 *.bin *.gpkg *.mem)')

        self.current_path = image
        self.image = [os.path.basename(image)]
        self.combobox_image.clear()
        self.combobox_image.addItems([image for image in self.image])
        if self.current_path:
            self.output = _load_image(self.current_path)
            self.commit.deferred()

    def __show_open_dialog_file(self):
        filename, f = QFileDialog.getOpenFileName(
            self, 'Select directory/file', 'some/default/path/',
            'Product files(*.safe *.zip *.tar)')

        self.current_path = filename
        self.file = [os.path.basename(filename)]
        self.combobox_file.clear()
        self.combobox_file.addItems([file for file in self.file])
        if self.current_path:
            self.output = _load_file(self.current_path)
            self.commit.deferred()


def _load_image(file):
    base_node = DrbFileFactory().create(file)
    image_node = DrbImageFactory().create(base_node)

    return image_node


def _load_file(file):

    topic, file_node = resolver.resolve(file)

    return file_node


if __name__ == "__main__":
    from orangewidget.utils.widgetpreview import WidgetPreview
    WidgetPreview(OWLoadImage).run()
