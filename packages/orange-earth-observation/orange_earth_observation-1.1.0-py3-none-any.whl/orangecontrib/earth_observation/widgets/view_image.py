import os
from typing import List, Optional, Iterable
from Orange.widgets import widget, gui, settings
from Orange.widgets.widget import Input, Output, MultiInput
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import pyqtSlot as Slot
from PyQt5.QtWidgets import QWidget, QListWidget, QListWidgetItem, QListView
from drb.drivers.file import DrbFileFactory, DrbFileNode
from drb.drivers.image import DrbImageFactory, DrbImageBaseNode


class IconView(QListWidget):
    """
    A list view (in QListView.IconMode).
    """

    def __init__(
            self, parent: Optional[QWidget] = None,
            icon_size=QSize(80, 80),
            word_wrap=True,
            **kwargs
    ) -> None:
        super().__init__(parent, wordWrap=word_wrap, **kwargs)
        self.setViewMode(QListView.IconMode)
        self.setEditTriggers(QListView.NoEditTriggers)
        self.setMovement(QListView.Static)
        self.setSelectionMode(QListView.ExtendedSelection)
        self.setIconSize(icon_size)


class OWViewImage(widget.OWWidget):
    name = "EO View Image"
    description = "Views image(s), also can be used to save an" \
                  " image in the directory structure"
    icon = "icons/view.svg"
    priority = 80

    files = []
    input_nodes = []
    selection = None

    want_main_area = True
    graph_name = "thumbnailView"
    image_size = settings.Setting(100)
    auto_commit = settings.Setting(True)

    class Inputs:
        dir = Input("Dir", str, auto_summary=False)
        data = MultiInput("List[DrbImageBaseNode]",
                          DrbImageBaseNode, auto_summary=False)

    class Outputs:
        output = Output("Selected[DrbImageBaseNode]",
                        DrbImageBaseNode, auto_summary=False)

    def __init__(self):
        super().__init__()
        self.nodes = []
        self.output = None

        gui.hSlider(
            self.controlArea, self, "image_size",
            box="Image Size", minValue=32, maxValue=1024, step=16,
            callback=self._update_size,
            createLabel=False
        )
        gui.rubber(self.controlArea)
        gui.auto_commit(self.buttonsArea, self,
                        "auto_commit", "Send", box=False)

        self.thumbnailView = IconView(
            resizeMode=IconView.Adjust,
            iconSize=QSize(self.image_size, self.image_size),
        )
        self.thumbnailView.itemClicked.connect(self._change_selection)

        self.main_scene = self.mainArea.layout()
        self.mainArea.setMinimumWidth(200)

    def view_image(self):

        self.thumbnailView.clear()
        if self.input_nodes:
            for image_node in self.input_nodes:
                path = image_node.path.path
                print(path)

                item = QListWidgetItem()
                icon = QIcon()
                icon.addPixmap(QPixmap(path))
                item.setIcon(icon)
                self.thumbnailView.addItem(item)

            self.main_scene.addWidget(self.thumbnailView)

    def _update_size(self):
        self.thumbnailView.setIconSize(QSize(self.image_size, self.image_size))

    @Slot()
    def _change_selection(self):

        self.selection = self.thumbnailView.currentRow()
        self.commit.deferred()

    @Inputs.data
    def set_data(self, index, image: DrbImageBaseNode):
        try:
            self.input_nodes[index] = image
        except IndexError:
            self.input_nodes.append(image)

        self.view_image()

    @Inputs.data.insert
    def insert_data(self, index, image: DrbImageBaseNode):

        if index == 0:
            self.input_nodes = [image]

        else:
            self.input_nodes.append(image)

        self.view_image()

    @Inputs.data.remove
    def remove_data(self, index):
        self.input_nodes.pop(index)

        if not self.input_nodes:
            self.combobox_image.clear()

        self.view_image()

    @Inputs.dir
    def set_dir(self, dir):
        self.files = [os.path.join(dir, file) for file in os.listdir(dir)]
        self.input_nodes = [_load_image(file) for file in self.files]
        self.view_image()

    @gui.deferred
    def commit(self):
        """
        Commits the result the next widget in the line.
        """

        if self.input_nodes:
            if self.selection is not None:
                self.output = self.input_nodes[self.selection]
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
    WidgetPreview(OWViewImage).run()
