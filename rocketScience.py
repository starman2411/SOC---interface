from vpython import scene,vector,sphere,color,rate
from math import cos,sin,sqrt,radians,pi
from matplotlib.pyplot import *

G = 6.674e-11 # Newton gravitational constant
dt=1
earth_mass=5.9722e24
grav_param=(earth_mass+1e4)*G

class Orbit:
    def __init__(self,param,e,fi=0):
        self.p=param
        self.e=e
        self.fi=fi
        if self.e !=0:
            self.a=self.p/(1-self.e**2)
            self.b=sqrt(self.a*self.p)
        else:
            self.a=self.p
            self.b=self.p

    def draw_orbit(self):
        t=np.linspace(0,360,360)
        x=[(self.p/(1+self.e*cos(radians(i))))*cos(radians(i)) for i in t]
        y=[(self.p/(1+self.e*cos(radians(i))))*sin(radians(i)) for i in t]
        plot(x,y)
        show()


class Spacecraft:
    def __init__(self, mass, orbit, fi=0):
        self.mass = mass
        self.orbit = orbit
        self.r = np.array([orbit.p * cos(radians(fi)) / (1 + orbit.e * cos(radians(fi))),
                           orbit.p * sin(radians(fi)) / (1 + orbit.e * cos(radians(fi))), 0])
        self.v_n = sqrt(grav_param / orbit.p) * (1 + orbit.e * cos(radians(fi)))
        self.v_r = sqrt(grav_param / orbit.p) * orbit.e * sin(radians(fi))
        self.velocity = np.array([self.v_r * cos(radians(fi)) + self.v_n * cos(radians(fi + 90)),
                                  self.v_r * sin(radians(fi)) + self.v_n * sin(radians(fi + 90)), 0])
        self.h = np.linalg.norm(self.velocity) ** 2 - 2 * grav_param / np.linalg.norm(self.r)

    def get_momentum(self, delta):
        self.velocity = delta / self.mass + self.velocity

    def goman(self, new_orbit):
        pass


class Interval:
    def __init__(self, start_time, duration, spacecraft):
        self.interval = []
        self.speeds = []
        self.start_r = spacecraft.r
        self.start_time = start_time
        self.end_time = start_time + duration
        self.start_momentum = spacecraft.velocity * spacecraft.mass
        self.start_velocity = spacecraft.velocity
        spacecraft_p = spacecraft.velocity * spacecraft.mass
        spacecraft_pos = spacecraft.r
        for i in range(int(duration / dt)):
            F = -G * earth_mass * spacecraft.mass * spacecraft_pos / np.linalg.norm(spacecraft_pos) ** 3
            spacecraft_p = spacecraft_p + F * dt
            spacecraft_pos = spacecraft_pos + (spacecraft_p / spacecraft.mass) * dt
            self.interval.append(spacecraft_pos)
            self.speeds.append(spacecraft_p / spacecraft.mass)
        spacecraft.r = spacecraft_pos
        spacecraft.velocity = spacecraft_p / spacecraft.mass


def goman(spacecraft, target_orbit, start_time):
    if spacecraft.orbit.e != 0:
        print('Не круговые орбиты не поддерживаются')
        return (0, 0)
    if target_orbit.e != 0:
        print('Не круговые орбиты не поддерживаются')
        return (0, 0)
    r1 = spacecraft.orbit.a
    r2 = target_orbit.a
    if r1 < r2:
        k = 1
    else:
        k = -1

    v1 = spacecraft.velocity
    v2 = -sqrt(grav_param / r2) * v1 // np.linalg.norm(v1)
    delta_V_A = sqrt(grav_param / r1) * (sqrt(2 * r2 / (r1 + r2)) - 1) * v1 / np.linalg.norm(v1)
    delta_V_B = sqrt(grav_param / r2) * (1 - sqrt(2 * r1 / (r1 + r2))) * v1 // np.linalg.norm(v1)
    transfer_orbit = Orbit(np.linalg.norm(np.cross(spacecraft.r, v1 + delta_V_A)) ** 2 / grav_param,
                           (r2 - r1) / (r2 + r1))
    # transfer_orbit.draw_orbit()
    T_transfer = pi * sqrt(((0.5 * (r1 + r2)) ** 3) / grav_param)
    spacecraft.velocity = v1 + delta_V_A
    interval_A = Interval(start_time, T_transfer, spacecraft)
    spacecraft.velocity = v2
    spacecraft.orbit = target_orbit
    return (interval_A)

def simulation(track):
    scene.forward = vector(0,0,-1)
    earth = sphere(pos=vector(0,0,0), radius=6.4e6, color=color.blue)
    earth.mass = earth_mass
    colors=[color.red,color.cyan,color.purple,color.green,color.orange,color.white]
    l=0
    for i in track.track_list:
        spacecraft = sphere(pos=vector(i.start_r[0],i.start_r[1],i.start_r[2]), radius=5e5, color=colors[l],
                make_trail=True, interval=10, retain=100000)
        l+=1
        for k in i.interval:
            rate(6000)
            spacecraft.pos = vector(k[0],k[1],k[2])

class Track:
    def __init__(self):
        self.track_list = []

    def append_interval(self, interval):
        self.track_list.append(interval)

    def get_track_list(self):
        return (self.track_list)

    def load_from_file(self):
        pass


