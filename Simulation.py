import numpy as np

class SimulationAgent:
    def calc_step(self):
        raise NotImplementedError()

class UAV(SimulationAgent):
    location = np.array([0., 0., 0.])
    rotationY = 0.
    speed = np.array([0., 0., 0.])
    acceleration = np.array([0., 0., 0.])
    mass = 1
    # ctrl_direct = np.array([0., 0., 0.]) # Where the pilot drives it at the moment (tick) using a joystick

    def apply_force(self, F):
        self.acceleration += F / self.mass # Newton's Second law of motion
        return self

    def calc_step(self):
        # Calculate Speed
        self.speed += self.acceleration
        # Calculate location
        self.location += self.speed
        return self

class Wind(SimulationAgent):
    directional_force = np.array([0., 0., 0.])
    wind_strength = 10
    rate_of_change = 0.1 # Rate at which wind changes
    max_wind_force = 1

    def calc_step(self):
        """Change the direction and strength of Wind on each tick"""
        self.directional_force += np.random.uniform(-0.1 * self.rate_of_change * self.wind_strength,
                                                    0.1 * self.rate_of_change * self.wind_strength, 3)
        self.directional_force.clip(-self.max_wind_force, self.max_wind_force)
        return self

class Controls(SimulationAgent):
    """General class for any control type that may be used in the future"""
    directional_force = np.array([0, 0, 0])

import keyboard
class KeyboardControls(Controls):
    directional_engine_strength = np.array([1, 2, 1]) # Force of controls in newtons

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

def tick(uav, wind, controls, TPS):
    collective_force_at_tick = wind.calc_step().directional_force + controls.directional_force
    uav.apply_force(collective_force_at_tick / TPS)
    uav.calc_step()
    return True

import time
def simulate():
    uav1 = UAV()
    wind = Wind()
    keys = KeyboardControls()
    TPS = 60 # Ticks Per Second
    while (True):
        tick(uav1, wind, keys, TPS)
        time.sleep(1 / TPS)
        print(uav1.location)

simulate()




