import numpy as np

TPS = 60  # Ticks Per Second

class SimulationAgent:
    def calc_step(self):
        raise NotImplementedError()

class UAV(SimulationAgent):
    location = np.array([0., 0., 0.])
    rotationY = 0.
    speed = np.array([0., 0., 0.])
    acceleration = np.array([0., 0., 0.])
    mass = 1
    cross_sectional_area = 0.1
    drag_coefficient = 1.2

    def apply_force(self, F):
        self.acceleration = F / self.mass # Newton's Second law of motion
        return self

    def calc_step(self):
        # Calculate Speed
        self.speed += self.acceleration/TPS
        # Calculate location
        self.location += self.speed/TPS
        return self

class Force(SimulationAgent):
    directional_force = np.array([0., 0., 0.])

class Wind(Force):
    wind_strength = 10
    rate_of_change = 0.1 # Rate at which wind changes
    max_wind_force = 1

    def calc_step(self):
        """Change the direction and strength of Wind on each tick"""
        self.directional_force += np.random.uniform(-0.1 * self.rate_of_change * self.wind_strength,
                                                    0.1 * self.rate_of_change * self.wind_strength, 3)
        self.directional_force.clip(-self.max_wind_force, self.max_wind_force)
        return self

class AirFriction(Force):
    p = 1.225 # Air density in kg/m^3

    def calc_step(self, A, V, C):
        """Calculate air friction, where:
        A: crossectional area of the object
        V: object's speed relative to the fluid
        C: drag coefficient of the object"""
        self.directional_force = .5 * self.p * V * np.absolute(V) * C * A * 50000
        # It's always positive. Make it opposite to speed
        return self

class Controls(Force):
    """General class for any control type that may be used in the future"""
    directional_engine_strength = np.array([1, 1.3, 1])*1000  # Force of controls in Newtons

import keyboard
class KeyboardControls(Controls):

    def calc_step(self):
        """Read the pressed buttons and set the directional_force accordingly"""
        # Left/Right
        X = 0.
        if keyboard.is_pressed("d"): X = 1.
        if keyboard.is_pressed("a"): X = -1.
        if keyboard.is_pressed("d") and keyboard.is_pressed("a"): X = 0.
        # Upward/Downward
        Y = 0.
        if keyboard.is_pressed("space"): Y = 1.
        if keyboard.is_pressed("c"): Y = -1.
        if keyboard.is_pressed("space") and keyboard.is_pressed("c"): Y = 0.
        # Forward/Backward
        Z = 0.
        if keyboard.is_pressed("w"): Z = 1.
        if keyboard.is_pressed("s"): Z = -1.
        if keyboard.is_pressed("w") and keyboard.is_pressed("s"): Z = 0.

        # Set the control direction
        self.directional_force[0] = X * self.directional_engine_strength[0]
        self.directional_force[1] = Y * self.directional_engine_strength[1]
        self.directional_force[2] = Z * self.directional_engine_strength[2]
        return self



def tick(uav, wind, air_friction, controls, TPS):
    # collective_force_at_tick = wind.calc_step().directional_force + controls.calc_step().directional_force
    collective_force_at_tick = wind.calc_step().directional_force + controls.calc_step().directional_force - \
                               air_friction.calc_step(uav.cross_sectional_area, uav.speed, uav.drag_coefficient).\
                               directional_force
    # print(air_friction.directional_force / TPS)
    uav.apply_force(collective_force_at_tick / TPS)
    uav.calc_step()
    return True

import time
import os
def simulate():
    uav1 = UAV()
    wind = Wind()
    keys = KeyboardControls()
    air_friction = AirFriction()
    while (True):
        tick(uav1, wind, air_friction, keys, TPS)
        time.sleep(1 / TPS)
        os.system('cls')
        print(uav1.speed.round(3))

        # print(uav1.location.round(3))

simulate()




