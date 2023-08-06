import logging
import os
from geo.Geoserver import Geoserver, GeoserverException
from typing import List, Dict, Optional, Iterable
from Orange.widgets import widget, gui, settings
from Orange.widgets.widget import Input
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QFileDialog, QAction, QPushButton

from drb.drivers.file import DrbFileFactory, DrbFileNode
from drb.drivers.image import DrbImageFactory, DrbImageBaseNode
import json


class ManifestData:
    def __init__(self, dico: Dict):
        self.start_date = dico['startDate']
        self.stop_date = dico['stopDate']
        self.title = dico['title']
        self.url = dico['url']
        self.layer = dico['layer']


class OWManifest(widget.OWWidget):
    name = "Manifest Update"
    description = "Updates manifest exchange file" \
                  " with URL(s) of data published to Geoserver"
    icon = "icons/manifest.svg"
    priority = 130

    want_main_area = False
    auto_commit = settings.Setting(True)

    class Inputs:
        data = Input("ManifestData", ManifestData, auto_summary=False)

    def __init__(self):
        super().__init__()
        self.data = None
        self.output = None

        browse_action = QAction(
            self,
            text="\N{HORIZONTAL ELLIPSIS}",
        )

        browse_action.triggered.connect(self.__show_open_dialog_file)
        browse_button = QPushButton(
            browse_action.iconText(),
            clicked=browse_action.trigger
        )

        hbox = gui.hBox(self.controlArea,
                        box=" "
                        )
        hbox.layout().addWidget(QLabel("Select Manifest File: "))
        hbox.layout().addWidget(browse_button)
        gui.rubber(self.controlArea)

        self.box = gui.widgetBox(self.controlArea, " ")
        gui.rubber(self.controlArea)

        self.button = gui.button(
            self.box, self, "Update",
            autoDefault=False,
            callback=self.update_manifest
        )

        gui.rubber(self.controlArea)
        gui.auto_commit(self.buttonsArea, self,
                        "auto_commit", "Send", box=False)

    def update_manifest(self):
        # Read the JSON file
        with open(self.current_path, 'r') as file:
            data = json.load(file)

        data['startDateTime'] = self.data.start_date
        data['stopDateTime'] = self.data.stop_date

        workspaces = data['ndLayers']
        if self.data:
            if self.data.title not in workspaces:
                data['ndLayers'].append(
                    {'tilte': self.data.title,
                     'url': self.data.url,
                     'layer': self.data.layer})

        # Write the updated dictionary back to the JSON file
        with open(self.current_path, 'w') as file:
            json.dump(data, file, indent=4)
        print("ok")

    @Inputs.data
    def set_data(self, data):
        self.data = data

    @gui.deferred
    def commit(self):
        """
         Commits the result the next widget in the line.
         """
        if self.output:
            self.Outputs.output.send(self.output)

        else:
            self.Outputs.output.send(None)

    def __show_open_dialog_file(self):
        self.current_path, f = QFileDialog.getOpenFileName(
            self, 'Select directory/file',
            'some/default/path/', 'Product files'
                                  '(*.json)')


if __name__ == "__main__":
    from orangewidget.utils.widgetpreview import WidgetPreview
    WidgetPreview(OWGeo).run()
