from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import rcParams

import serial
import serial.tools.list_ports
import sys
import os
import time
import numpy as np

sys.path.append("../pyB12SPS/")
dir_path = os.path.dirname(os.path.realpath(__file__))
uiFile = dir_path + "/pyB12SPSGUI.ui"
import pyB12SPS as sps

# 4k display
if hasattr(QtCore.Qt, "AA_EnableHighDpiScaling"):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, "AA_UseHighDpiPixmaps"):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


spinBoxLabelsAlias = ["Z0", "Z1", "Z2", "X", "Y", "B0", "CH6", "CH7"]


class pyB12SPSGUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(pyB12SPSGUI, self).__init__()
        uic.loadUi(uiFile, self)
        self.setWindowTitle("Bridge12 Shim Power Supply GUI")

        self.set_variables()
        self.set_label_alias()
        self.init_shim()
        self.setup_connections()
        self.set_step_size()
        self.set_read_shim_values()

        self.show()

    def init_shim(self):
        self.shim = sps.Shim()

    def set_variables(self):
        self.labels = [
            self.label_0,
            self.label_1,
            self.label_2,
            self.label_3,
            self.label_4,
            self.label_5,
            self.label_6,
            self.label_7,
        ]
        self.spinBoxes = [
            self.spinBox_0,
            self.spinBox_1,
            self.spinBox_2,
            self.spinBox_3,
            self.spinBox_4,
            self.spinBox_5,
            self.spinBox_6,
            self.spinBox_7,
        ]

    def set_read_shim_values(self):
        out = self.shim.status()
        current_data = out.strip().split(",")
        current_shim_values = list(map(int, current_data))

        for ix, spinBox in enumerate(self.spinBoxes):
            shim_value = current_shim_values[ix]
            spinBox.setValue(shim_value)

    def set_label_alias(self):
        for ix, label in enumerate(self.labels):
            text = spinBoxLabelsAlias[ix]
            label.setText(text)

    def set_step_size(self):
        self.step_size = self.spinBox_StepSize.value()

        for ix, spinBox in enumerate(self.spinBoxes):
            spinBox.setSingleStep(self.step_size)

    def set_CH0(self):
        self.shim.sch(0, int(self.spinBox_0.value()))

    def set_CH1(self):
        self.shim.sch(1, int(self.spinBox_1.value()))

    def set_CH2(self):
        self.shim.sch(2, int(self.spinBox_2.value()))

    def set_CH3(self):
        self.shim.sch(3, int(self.spinBox_3.value()))

    def set_CH4(self):
        self.shim.sch(4, int(self.spinBox_4.value()))

    def set_CH5(self):
        self.shim.sch(5, int(self.spinBox_5.value()))

    def set_CH6(self):
        self.shim.sch(6, int(self.spinBox_6.value()))

    def set_CH7(self):
        self.shim.sch(7, int(self.spinBox_7.value()))

    def setup_connections(self):
        self.spinBox_StepSize.valueChanged.connect(self.set_step_size)
        self.spinBox_0.valueChanged.connect(self.set_CH0)
        self.spinBox_1.valueChanged.connect(self.set_CH1)
        self.spinBox_2.valueChanged.connect(self.set_CH2)
        self.spinBox_3.valueChanged.connect(self.set_CH3)
        self.spinBox_4.valueChanged.connect(self.set_CH4)
        self.spinBox_5.valueChanged.connect(self.set_CH5)
        self.spinBox_6.valueChanged.connect(self.set_CH6)
        self.spinBox_7.valueChanged.connect(self.set_CH7)

        self.actionSaveShimValues.triggered.connect(self.save_shim_values)
        self.actionLoadShimValues.triggered.connect(self.load_shim_values)

    def save_shim_values(self):
        shim_values = []

        for ix, spinBox in enumerate(self.spinBoxes):
            shim_values.append(int(spinBox.value()))

        shim_values = np.array(shim_values).reshape(-1, 1)

        filename, ext = QFileDialog.getSaveFileName(self, "Save File", filter="*.csv")
        if filename != "":
            try:
                np.savetxt(filename, shim_values, fmt="%i", delimiter=",")
                self.statusBar().showMessage("Saved shim values to file: %s" % filename)
            except:
                self.statusBar().showMessage("Unable to save parameters")

    def load_shim_values(self):
        filename, ext = QFileDialog.getOpenFileName(self, "Import File", filter="*.csv")

        load_shim_values = np.loadtxt(filename, dtype=int, delimiter=",")

        load_shim_values = list(load_shim_values.reshape(-1))

        for ix, spinBox in enumerate(self.spinBoxes):
            spinBox.setValue(load_shim_values[ix])

        self.statusBar().showMessage("Loaded shim values from file: %s" % filename)


def main_func():
    app = QtWidgets.QApplication(sys.argv)
    window = pyB12SPSGUI()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main_func()
