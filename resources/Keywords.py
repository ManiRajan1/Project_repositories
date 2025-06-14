from robot.api.deco import keyword
import time

class Keywords:
    @keyword("Ignition On")
    def ignition_on(self):
        print("Robot: Ignition turned ON")

    @keyword("Ignition Off")
    def ignition_off(self):
        print("Robot: Ignition turned OFF")

    @keyword ("Signal In")
    def signal_in(self, input_signal):
        print (f"The input signal received is :{input_signal}")
        assert input_signal == "10"