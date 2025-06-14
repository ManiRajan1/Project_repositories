from robot.api.deco import keyword
import time

class Keywords:
    @keyword("Ignition On")
    def ignition_on(self):
        print("Robot: Ignition turned ON")

    @keyword("Ignition Off")
    def ignition_off(self):
        print("Robot: Ignition turned OFF")