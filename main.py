from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5 import uic
from PyQt5.QtWidgets import *
from calculating import Stream
from rocketScience import simulation
import sys

flagok=True

( Ui_MainWindow, QMainWindow ) = uic.loadUiType('main_window.ui')


class mywindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.but_start.clicked.connect(self.start)
        self.ui.but_stop.clicked.connect(self.stop)
        self.stream1=Stream()
        #self.stream1.start()


    def start(self):
        orbits=[]


        parameters = {'sc_mass':float(self.ui.spacecraft_mass.text()), 'initial_orbit_p': float(self.ui.initial_orbit_p.text()),
                      'initial_orbit_e': float(self.ui.initial_orbit_e.text()),'initial_orbit_fi': float(self.ui.initial_orbit_fi.text()),
                      'initial_orbit_duration':float(self.ui.initial_orbit_duration.text())
                      }
        if self.ui.orbit1_duration.text()!='0':
            orbits.append({'orbit_p': float(self.ui.orbit1_p.text()),'orbit_e': float(self.ui.orbit1_e.text()),'orbit_fi': float(self.ui.orbit1_fi.text()),
                      'orbit_duration':float(self.ui.orbit1_duration.text())})
        if self.ui.orbit2_duration.text() != '0':
            orbits.append({'orbit_p': float(self.ui.orbit2_p.text()),'orbit_e': float(self.ui.orbit2_e.text()), 'orbit_fi': float(self.ui.orbit2_fi.text()),
                           'orbit_duration': float(self.ui.orbit2_duration.text())})
        if self.ui.orbit3_duration.text() != '0':
            orbits.append({'orbit_p': float(self.ui.orbit3_p.text()),'orbit_e': float(self.ui.orbit3_e.text()), 'orbit_fi': float(self.ui.orbit3_fi.text()),
                           'orbit_duration': float(self.ui.orbit3_duration.text())})

        Stream.params = parameters
        Stream.list_of_orbits = orbits
        self.stream1.start()
        self.stream1.trigger.connect(self.sim)
        #self.stream1.trigger.connect(self.sim)
        #self.ui.txt_1.setText(self.ui.input_1.text('start stream'))


    def stop(self):
        self.stream1.flag=False


    def sim(self,track):
        global flagok
        self.stream1.flag = False

        if flagok:
            simulation(track)
        flagok=False




app = QtWidgets.QApplication([])


application = mywindow()
application.show()

sys._excepthook = sys.excepthook

def my_exception_hook(exctype, value, traceback): #ошибки из потока
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


sys.excepthook = my_exception_hook


sys.exit(app.exec())


