import logging
import os
from geo.Geoserver import Geoserver, GeoserverException
from typing import List, Optional, Iterable
from Orange.widgets import widget, gui, settings
from Orange.widgets.widget import Input, Output
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QFileDialog, QAction, QPushButton

from drb.drivers.file import DrbFileFactory, DrbFileNode
from drb.drivers.image import DrbImageFactory, DrbImageBaseNode
import configparser

from .manifest import ManifestData
import re


class OWGeo(widget.OWWidget):
    name = "Push to Geoserver"
    description = "Commits data to Geoserver"
    icon = "icons/geoserver.svg"
    priority = 120

    files = []
    input_nodes = []

    workspace_name = ""

    want_main_area = False
    auto_commit = settings.Setting(True)

    class Inputs:
        dir = Input("Dir", str, auto_summary=False)

    class Outputs:
        output = Output("ManifestData", ManifestData, auto_summary=False)

    def __init__(self):
        super().__init__()
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
        hbox.layout().addWidget(QLabel("Select Config File: "))
        hbox.layout().addWidget(browse_button)
        gui.rubber(self.controlArea)

        self.box = gui.widgetBox(self.controlArea, " ")
        gui.rubber(self.controlArea)

        self.workspace_line = gui.lineEdit(
            self.box, self, "workspace_name",
            label="Workspace Name:",
            orientation=Qt.Horizontal,
            controlWidth=200,
        )

        self.workspace_button = gui.button(
            self.box, self, "Create",
            autoDefault=False,
            callback=self.create_workspace
        )

        self.data_box = gui.widgetBox(self.controlArea, " ")
        gui.rubber(self.controlArea)

        self.data_button = gui.button(
            self.data_box, self, "Publish to Geo",
            autoDefault=False,
            callback=self.publish_to_geo
        )

        gui.rubber(self.controlArea)
        gui.auto_commit(self.buttonsArea, self,
                        "auto_commit", "Send", box=False)

    def create_workspace(self):
        workspaces = self.geo.get_workspaces()

        name = self.workspace_line.text()

        if not any(wsp['name'] == name for wsp in workspaces[
                'workspaces']['workspace']):
            self.geo.create_workspace(workspace=name)

        return name

    def publish_to_geo(self):
        dico = {}
        name = self.create_workspace()

        for node in self.input_nodes:

            if node.name.endswith("tif.aux.xml"):
                self.input_nodes.pop(self.input_nodes.index(node))
                continue

            try:
                self.geo.delete_coveragestore(
                    coveragestore_name=f'{self.workspace_name}_'
                                       f'{os.path.splitext(node.name)[0]}',
                    workspace=name)
            except Exception:
                logging.Logger(f'coveragestore: {node.name} does not exist')

            self.geo.create_coveragestore(
                layer_name=f'{self.workspace_name}_'
                           f'{os.path.splitext(node.name)[0]}',
                path=node.path.path, workspace=name)

        layergroups = self.geo.get_layergroups(workspace=name)
        css = self.geo.get_coveragestores(workspace=name)
        css_names = [cs['name'] for cs in css[
            'coverageStores']['coverageStore']]

        try:
            if not any(
                    lgrp['name'] == f'{name}_lG' for lgrp in layergroups[
                        'layerGroups']['layerGroup']):
                raise TypeError

            for cs_name in css_names:
                self.geo.add_layer_to_layergroup(
                    layergroup_name=f'{name}_lG',
                    layergroup_workspace=name,
                    layer_name=cs_name,
                    layer_workspace=name
                )

        except TypeError:
            self.geo.create_layergroup(
                name=f'{name}_lG',
                mode="single",
                layers=css_names,
                workspace=name  # None if you want to
                # create a layergroup outside the workspace
            )

        dico['title'] = name
        dico['url'] = f'{self.geo.service_url}/{name}/wms'
        dico['layer'] = f'{name}:{name}_lG'

        oldest_date = None
        newest_date = None

        for cs_name in css_names:
            # Extract the date using regular expression
            match = re.search(r"\d{8}", cs_name)
            if match:
                date_part = match.group()

                # Convert the date to the desired format
                formatted_date = f"{date_part[:4]}-" \
                                 f"{date_part[4:6]}-" \
                                 f"{date_part[6:8]}"

                # Update the oldest and newest dates
                if oldest_date is None or formatted_date < oldest_date:
                    oldest_date = formatted_date
                if newest_date is None or formatted_date > newest_date:
                    newest_date = formatted_date

        dico['startDate'] = oldest_date
        dico['stopDate'] = newest_date

        self.output = ManifestData(dico)
        self.commit.deferred()

        # Add legend style
        self.geo.create_coveragestyle(
            raster_path=self.input_nodes[0].path.path,
            style_name=f'{name}_style', workspace=name,
            color_ramp='RdYlGn')
        self.geo.publish_style(
            layer_name=f'{self.workspace_name}_'
                       f'{os.path.splitext(node.name)[0]}',
            style_name=f'{name}_style', workspace=name)

    @Inputs.dir
    def set_dir(self, dir):
        self.workspace_name = os.path.basename(dir)
        self.files = [os.path.join(dir, file) for file in os.listdir(dir)]
        self.input_nodes = [_load_image(file) for file in self.files]

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
                                  '(*.ini *.yml *.json)')

        config = configparser.ConfigParser()
        config.read(self.current_path)

        url = config['GeoserverNode']['url']
        username = config['GeoserverNode']['username']
        password = config['GeoserverNode']['password']

        self.geo = Geoserver(url, username=username, password=password)


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
    WidgetPreview(OWGeo).run()
