from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from rocketScience import Track,Orbit,Interval,goman,Spacecraft
class Stream(QtCore.QThread):

    trigger = pyqtSignal(Track)

    params={}
    list_of_orbits=[]

    def __init__(self,parent=None):
        QtCore.QThread.__init__(self, parent)
        self.flag=True

    def run(self):
        initial_orbit=Orbit(self.params['initial_orbit_p'],self.params['initial_orbit_e'],self.params['initial_orbit_fi'])
        spacecraft = Spacecraft(1e4, initial_orbit)
        orbits=[]
        track = Track()
        track.append_interval(Interval(0, self.params['initial_orbit_duration'], spacecraft))

        for i in range(len(self.list_of_orbits)):

            orbits.append(Orbit(self.list_of_orbits[i]['orbit_p'],self.list_of_orbits[i]['orbit_e'],self.list_of_orbits[i]['orbit_fi']))
            track.append_interval(goman(spacecraft, orbits[i], 20000))
            track.append_interval(Interval(0,self.list_of_orbits[i]['orbit_duration'],spacecraft) )

        while self.flag==True:
            self.trigger.emit(track) #Отправляю запись с передвижениями в основной поток







