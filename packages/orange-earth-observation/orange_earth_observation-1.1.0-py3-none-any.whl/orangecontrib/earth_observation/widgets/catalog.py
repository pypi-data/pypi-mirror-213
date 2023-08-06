import os
import io
from Orange.widgets import widget, gui, settings
from Orange.widgets.utils.signals import Output
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QPalette, QColor, QTextCharFormat
from PyQt5.QtWidgets import QAction, QPushButton, \
    QFileDialog, QCalendarWidget, QHBoxLayout
from drb.core import DrbNode
from drb.utils.keyringconnection import kr_add
from drb.drivers.odata import ODataQueryPredicate, OdataFactory
import drb.topics.resolver as resolver
import datetime


class CalendarStateMachine:
    def __init__(self, calendar):
        self.calendar = calendar
        self.palette = self.calendar.palette()
        self.first_date = None
        self.second_date = None
        self.calendar.clicked[QDate].connect(self.handle_clicked)

    def set_selected_style(self):
        self.palette.setColor(QPalette.Highlight, QColor("#007acc"))
        self.palette.setColor(QPalette.HighlightedText, Qt.white)
        self.calendar.setPalette(self.palette)

        if self.first_date is not None and self.second_date is not None:
            fmt = QTextCharFormat()
            fmt.setBackground(self.palette.color(QPalette.Highlight))
            fmt.setForeground(self.palette.color(QPalette.HighlightedText))
            start_date = self.first_date
            while start_date <= self.second_date:
                self.calendar.setDateTextFormat(start_date, fmt)
                start_date = start_date.addDays(1)

    def reset_calendar_style(self):
        # Reset the calendar's palette to the default palette
        self.calendar.setPalette(self.calendar.style().standardPalette())

        # Remove any custom date text formats that were applied
        if self.first_date is not None and self.second_date is not None:
            fmt = QTextCharFormat()
            start_date = self.first_date
            while start_date <= self.second_date:
                self.calendar.setDateTextFormat(start_date, fmt)
                start_date = start_date.addDays(1)

    def handle_clicked(self, date):
        if self.first_date is None:
            self.first_date = date
            self.set_selected_style()
        elif self.second_date is None:
            if self.first_date < date:
                self.second_date = date
                self.set_selected_style()
            elif self.first_date == date:
                self.reset_calendar_style()
                self.first_date = None

        else:
            if self.first_date <= date <= self.second_date:
                self.reset_calendar_style()

                self.first_date = None
                self.second_date = None
            elif self.first_date > date:
                self.first_date = date
                self.set_selected_style()
            elif self.second_date < date:
                self.second_date = date
                self.set_selected_style()


class OWDataCatalog(widget.OWWidget):
    name = "EO Data Catalog"
    description = "Access and retrieve data from " \
                  "different services using Odata protocol"
    icon = "icons/catalog.svg"
    priority = 10

    services = ["CSC Service", "DHuS Service", "Dias Service", "Drive"]
    missions = ["S1", "S2", "S3",
                "S5p", "EN1", "LC08"]
    platforms = []
    product_types = []
    sensors = []
    nodes = []
    output_nodes = []

    cloud_cover_value = 20
    latitude_min = 41.5
    longitude_min = -4.6
    latitude_max = 51.34
    longitude_max = 8.8

    modality = Qt.ApplicationModal
    dir = os.getcwd()
    recent_paths = settings.Setting([])

    want_main_area = False
    graph_name = "thumbnailView"
    auto_commit = settings.Setting(True)

    class Outputs:
        output = Output("DrbNode", DrbNode, auto_summary=False)
        dir = Output("Dir", str, auto_summary=False)

    def __init__(self):
        super().__init__()
        self.data = None
        self.username = None
        self.password = None
        self.service = None
        self.service_node = None
        self.output = None

        # GUI Commands
        self.combobox_service = gui.comboBox(
            self.controlArea, self, "", items=self.services,
            label="Choose Service: ",
            orientation=Qt.Horizontal,
            contentsLength=8,
        )
        self.combobox_service.activated.connect(self.choose_datasource)

        gui.rubber(self.controlArea)

        self.authentication_box = gui.widgetBox(
            self.controlArea, "Authentication: ")
        gui.rubber(self.controlArea)

        self.username_line = gui.lineEdit(
            self.authentication_box, self, "",
            label="Enter username:",
            orientation=Qt.Horizontal,
            controlWidth=400,
        )
        self.password_line = gui.lineEdit(
            self.authentication_box, self, "",
            label="Enter password:",
            orientation=Qt.Horizontal,
            controlWidth=400,
        )

        self.query_button = gui.button(
            self.authentication_box, self, "Query Service",
            autoDefault=False,
            callback=self.query_service
        )

        self.calendar = QCalendarWidget()
        self.calendar.setGeometry(0, 0, 100, 80)
        self.statemachine = CalendarStateMachine(self.calendar)
        self.controlArea.layout().addWidget(self.calendar)

        self.predicate_box = gui.widgetBox(self.controlArea, " ")
        gui.rubber(self.controlArea)

        self.combobox_mission = gui.comboBox(
            self.predicate_box, self, "", items=self.missions,
            label="Select Mission:",
            orientation=Qt.Horizontal,
            contentsLength=12,
        )
        self.combobox_mission.activated.connect(self.choose_mission)

        self.combobox_platform = gui.comboBox(
            self.predicate_box, self, "", items=self.platforms,
            label="Select Platform:",
            orientation=Qt.Horizontal,
            contentsLength=12,
        )

        self.combobox_product_type = gui.comboBox(
            self.predicate_box, self, "", items=self.product_types,
            label="Select Product Type:",
            orientation=Qt.Horizontal,
            contentsLength=12,
        )

        self.combobox_sensor = gui.comboBox(
            self.predicate_box, self, "", items=self.sensors,
            label="Select Sensor:",
            orientation=Qt.Horizontal,
            contentsLength=12,
        )

        self.slider_cc_value = gui.hSlider(
            self.predicate_box, self, "cloud_cover_value",
            label="Cloud Cover Value %:", minValue=0, maxValue=100, step=1,
            width=400,
            createLabel=True
        )

        self.lat_min_spinbox = gui.doubleSpin(
            self.predicate_box, self, "latitude_min", -90, 90,
            label="Min. Latitude:",
            orientation=Qt.Horizontal,
            decimals=2
        )
        self.lon_min_spinbox = gui.doubleSpin(
            self.predicate_box, self, "longitude_min", -180, 180,
            label="Min. Longitude:",
            orientation=Qt.Horizontal,
            decimals=2
        )

        self.lat_max_spinbox = gui.doubleSpin(
            self.predicate_box, self, "latitude_max", -90, 90,
            label="Max. Latitude:",
            orientation=Qt.Horizontal,
            decimals=2
        )
        self.lon_max_spinbox = gui.doubleSpin(
            self.predicate_box, self, "longitude_max", -180, 180,
            label="Max. Longitude:",
            orientation=Qt.Horizontal,
            decimals=2
        )

        self.filter_button = gui.button(
            self.predicate_box, self, "Apply Predicate",
            callback=self.apply_filter
        )

        self.selection_box = gui.widgetBox(
            self.controlArea, "Select Node(s):")
        gui.rubber(self.controlArea)

        self.combobox_node_selection = gui.comboBox(
            self.selection_box, self, "", items=self.nodes,
            contentsLength=12,
        )
        self.combobox_node_selection.activated.connect(
            self.send_node)

        self.selection_button = gui.button(
            self.selection_box, self, "Select All",
            callback=self.send_all
        )

        browse_action = QAction(
            self,
            text="\N{HORIZONTAL ELLIPSIS}",
        )

        browse_action.triggered.connect(self.__open_dialog)
        browse_button = QPushButton(
            browse_action.iconText(),
            clicked=browse_action.trigger
        )

        vbox = gui.vBox(self.controlArea, box="Select Directory to:")
        hbox = gui.hBox(vbox)
        self.output_dir = gui.lineEdit(
            hbox, self, value="", label="Output Dir:"
        )

        hbox.layout().addWidget(self.output_dir)
        hbox.layout().addWidget(browse_button)

        self.download_button = gui.button(
            vbox, self, "Download Selection",
            callback=self.download
        )

        gui.rubber(self.controlArea)
        gui.auto_commit(self.buttonsArea, self,
                        "auto_commit", "Send", box=False)

    def _EnableGUI(self, bActivate):
        self.username_line.setEnabled(bActivate)
        self.password_line.setEnabled(bActivate)
        self.query_button.setEnabled(bActivate)

        self.calendar.setEnabled(bActivate)
        self.predicate_box.setEnabled(bActivate)

        self.selection_box.setEnabled(bActivate)
        self.download_button.setEnabled(bActivate)

    def query_service(self):

        self.choose_service()

        self.username = self.username_line.text()
        self.username_line.clear()
        self.password = self.password_line.text()
        self.password_line.clear()

        kr_add(service=self.service,
               username=self.username,
               password=self.password)

        self.service_node = OdataFactory().create(self.service)
        gui.label(
            self.authentication_box, self,
            f'{len(self.service_node.children)} results found')

    def choose_datasource(self):
        idx = self.combobox_service.currentIndex()

        if idx == 3:
            self.__open_dialog()
            self.service = ''
            self._EnableGUI(False)
        else:
            self._EnableGUI(True)

    def choose_service(self):
        idx = self.combobox_service.currentIndex()
        # CSC
        if idx == 0:
            self.service = 'https://demo1.databridge.gael.fr/gss-catalogue'

        # DHuS
        elif idx == 1:
            self.service = 'https://apihub.copernicus.eu/apihub/odata/v2'

            # DIAS
        elif idx == 2:
            self.service = 'https://catalogue.onda-dias.eu/dias-catalogue'

            # drive path
        elif idx == 3:
            self.__open_dialog()
            self.service = ''

    def choose_mission(self):
        idx = self.combobox_mission.currentIndex()

        # Sentinel1
        if idx == 0:

            self.platforms = ["", "A", "B"]
            self.combobox_platform.clear()
            self.combobox_platform.addItems([p for p in self.platforms])

            self.product_types = ["", "_SLC_", "_GRD_",
                                  "_OCN_", "_RAW_"]
            self.combobox_product_type.clear()
            self.combobox_product_type.addItems(
                [pt for pt in self.product_types])

            self.sensors = ["", "SW", "IW", "EW", "WV"]
            self.combobox_sensor.clear()
            self.combobox_sensor.addItems([s for s in self.sensors])

        # Sentinel2
        elif idx == 1:

            self.platforms = ["", "A", "B"]
            self.combobox_platform.clear()
            self.combobox_platform.addItems([p for p in self.platforms])

            self.product_types = ["", "_MSIL1C_", "_MSIL2A_"]
            self.combobox_product_type.clear()
            self.combobox_product_type.addItems(
                [pt for pt in self.product_types])
            self.combobox_sensor.clear()

        # Sentinel3
        elif idx == 2:

            self.platforms = ["", "A", "B"]
            self.combobox_platform.clear()
            self.combobox_platform.addItems(
                [p for p in self.platforms])

            self.product_types = ["", "_SR_1_SRA___", "_SR_1_SRA_A_",
                                  "_SR_1_SRA_BS",
                                  "_SR_2_LAN___", "_OL_1_EFR___",
                                  "_OL_1_ERR___",
                                  "_SL_1_RBT___", "_OL_2_LFR___",
                                  "_OL_2_LRR___",
                                  "_SL_2_LST___", "_OL_2_WFR___",
                                  "_OL_2_WRR___",
                                  "_SL_2_WST___", "_SR_2_WAT___",
                                  "_SY_2_SYN___",
                                  "_SY_2_V10___", "_SY_2_VG1___",
                                  "_SY_2_VGP___"]
            self.combobox_product_type.clear()
            self.combobox_product_type.addItems(
                [pt for pt in self.product_types])
            self.combobox_sensor.clear()

        # Sentinel5p
        elif idx == 3:

            self.platforms = ["", "_OFFL_", "_NRTI_"]
            self.combobox_platform.clear()
            self.combobox_platform.addItems([p for p in self.platforms])

            self.product_types = ["", "L1B_IR_SIR", "L1B_IR_UVN", "L1B_RA_BD1",
                                  "L1B_RA_BD2", "L1B_RA_BD3", "L1B_RA_BD4",
                                  "L1B_RA_BD5", "L1B_RA_BD6", "L1B_RA_BD7",
                                  "L1B_RA_BD8", "L2__AER_AI", "L2__CH4___",
                                  "L2__CLOUD_", "L2__SO2___", "L2__CO____",
                                  "L2__HCHO__", "L2__NO2___", "L2__O3____",
                                  "L2__O3_TCL_"]
            self.combobox_product_type.clear()
            self.combobox_product_type.addItems(
                [pt for pt in self.product_types])
            self.combobox_sensor.clear()

        # EnviSat
        elif idx == 4:

            self.platforms = ["", "_SPDK_", "_SPDE_"]
            self.combobox_platform.clear()
            self.combobox_platform.addItems([p for p in self.platforms])

            self.product_types = ["", "ASA_IM__OP", "ASA_WS__OP"]
            self.combobox_product_type.clear()
            self.combobox_product_type.addItems(
                [pt for pt in self.product_types])
            self.combobox_sensor.clear()

        # Landsat8
        elif idx == 5:

            self.platforms = [""]
            self.combobox_platform.clear()
            self.combobox_platform.addItems([p for p in self.platforms])

            self.product_types = ["", "_L1TP_"]
            self.combobox_product_type.clear()
            self.combobox_product_type.addItems(
                [pt for pt in self.product_types])
            self.combobox_sensor.clear()

    def apply_filter(self):

        idx_service = self.combobox_service.currentIndex()
        idx_mission = self.combobox_mission.currentIndex()
        mission = self.missions[idx_mission]

        idx_platform = self.combobox_platform.currentIndex()
        platform = self.platforms[idx_platform]

        idx_type = self.combobox_product_type.currentIndex()
        pt = self.product_types[idx_type]

        if idx_mission == 0:
            idx_sensor = self.combobox_sensor.currentIndex()
            sensor = self.sensors[idx_sensor]
        else:
            sensor = ""

        predicate = f"startswith("f"Name, '{mission}{platform}{sensor}{pt}')"

        # cloud coverage
        if idx_mission == 1 or idx_mission == 5:
            cc = self.cloud_cover_value
            predicate = predicate + \
                f" and Attributes/OData.CSC.DoubleAttribute/any(" \
                f"att:att/Name eq 'cloudCover' and " \
                f"att/OData.CSC.DoubleAttribute/Value lt {cc})"

        lat_min = self.latitude_min
        lon_min = self.longitude_min
        lat_max = self.latitude_max
        lon_max = self.longitude_max

        WTK_area = f"Polygon(({lon_min} {lat_max}," \
                   f"{lon_max} {lat_max},{lon_max} {lat_min}," \
                   f"{lon_min} {lat_min},{lon_min} {lat_max}))"
        predicate = predicate + f" and OData.CSC.Intersects(" \
                                f"location=Footprint," \
                                f"area=geography'SRID=4326;" \
                                f"{WTK_area}')"

        start_date = self.statemachine.first_date
        end_date = self.statemachine.second_date

        if start_date is not None:
            if end_date is None:
                date = datetime.datetime(start_date.year(),
                                         start_date.month(), start_date.day())
                iso_date = date.isoformat() + "Z"
                predicate = predicate + f" and ContentDate/Start gt {iso_date}"
            else:
                qdate = datetime.datetime(start_date.year(),
                                          start_date.month(), start_date.day())
                iso_start_date = qdate.isoformat() + "Z"
                zdate = datetime.datetime(end_date.year(),
                                          end_date.month(), end_date.day())
                iso_end_date = zdate.isoformat() + "Z"

                predicate = predicate + \
                    f" and ContentDate/Start gt {iso_start_date} " \
                    f"and ContentDate/Start lt {iso_end_date}"

        if idx_service == 2:
            filtered_children = ODataQueryPredicate(search=predicate)
        else:
            filtered_children = ODataQueryPredicate(filter=predicate)

        children = self.service_node[filtered_children]
        gui.label(
            self.predicate_box, self, f'{len(children)} results found')

        self.nodes = []

        if idx_mission == 1 or idx_mission == 2:
            if len(children) < 100:
                for i in range(len(children)):
                    self.nodes.append(children[i].name)

                self.combobox_node_selection.clear()
                self.combobox_node_selection.addItems(
                    [node for node in self.nodes])

    def send_node(self):

        idx = self.combobox_node_selection.currentIndex()
        product_name = self.nodes[idx]
        product_node = self.service_node[product_name]
        self.output = product_node
        self.commit.deferred()

    def send_all(self):

        for product_node in self.service_node.children:
            self.output_nodes.append(product_node)

        self.output = self.output_nodes
        self.output_nodes = []
        self.commit.deferred()

    def download(self):

        idx = self.combobox_node_selection.currentIndex()
        product_name = self.nodes[idx]
        product_node = self.service_node[product_name]

        with product_node.get_impl(io.BytesIO) as stream:
            with open(os.path.join(
                    self.dir + f'/{product_name}'), 'wb') as f:
                f.write(stream.read())
            f.close()

    @gui.deferred
    def commit(self):
        """
        Commits the result the next widget in the line.
        """
        self.Outputs.dir.send(self.dir)
        self.Outputs.output.send(self.output)

    def __open_dialog(self):
        start_dir = os.path.expanduser("~/")
        if self.recent_paths:
            start_dir = os.path.dirname(self.recent_paths[0].abspath)

        if OWDataCatalog.modality == Qt.WindowModal:
            dlg = QFileDialog(
                self, "Select Directory to Download to", start_dir,
                acceptMode=QFileDialog.AcceptOpen,
                modal=True,
            )
            dlg.setFileMode(QFileDialog.Directory)
            dlg.setOption(QFileDialog.ShowDirsOnly)
            dlg.setDirectory(start_dir)
            dlg.setAttribute(Qt.WA_DeleteOnClose)

            @dlg.accepted.connect
            def on_accepted():
                path_dir = dlg.selectedFiles()
                if dir_path:
                    self.setCurrentPath(path_dir[0])
                    self.start()
            dlg.open()
        else:
            dir_path = QFileDialog.getExistingDirectory(
                self, "Select Directory to Download to", start_dir
            )
            if dir_path:
                self.dir = dir_path
                self.commit.deferred()

                self.output_dir.setText(self.dir)

    def handleClicked(self, qDate):
        if self.calendar.selectedDate() == self.startDate:
            # If the selected date is the start date, update the end date
            self.endDate = qDate
        elif self.calendar.selectedDate() == self.endDate:
            # If the selected date is the end date, update the start date
            self.startDate = qDate
        else:
            # If the selected date is not the start or end date,
            # reset the range
            self.startDate = qDate
            self.endDate = qDate

        # Select the range of dates
        self.calendar.setMaximumDate(self.startDate)
        self.calendar.setMaximumDate(self.endDate)


if __name__ == "__main__":
    from orangewidget.utils.widgetpreview import WidgetPreview
    WidgetPreview(OWDataCatalog).run()
