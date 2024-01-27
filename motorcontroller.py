from logger import Logger
from machine import PWM

class MotorController:

    def __init__(self, in1, in2, in3, in4):
        self.logger = Logger()
        self.caller = "MotorController"

        self.FORWARD_BACKWARD_DUTY = int((65536 / 100) * 100)
        self.LEFT_RIGHT_DUTY = int((65536 / 100) * 30)

        self.FORWARD = 1
        self.BACKWARD = 2
        self.STOP = 3
        self.status = self.STOP

        self.in1 = PWM(in1, freq=1000, duty_u16=0)
        self.in2 = PWM(in2, freq=1000, duty_u16=0)
        self.in3 = PWM(in3, freq=1000, duty_u16=0)
        self.in4 = PWM(in4, freq=1000, duty_u16=0)

    def left(self):
        self.logger.debug(self.caller, "left")
        if self.status == self.FORWARD:
            self.in1.duty_u16(self.LEFT_RIGHT_DUTY)
            self.in2.duty_u16(0)
            self.in3.duty_u16(0)
            self.in4.duty_u16(self.FORWARD_BACKWARD_DUTY)
        if self.status == self.BACKWARD:
            self.in1.duty_u16(0)
            self.in2.duty_u16(self.LEFT_RIGHT_DUTY)
            self.in3.duty_u16(self.FORWARD_BACKWARD_DUTY)
            self.in4.duty_u16(0)

    def left_stop(self):
        self.logger.debug(self.caller, "left_stop")
        if self.status == self.FORWARD:
            self.forward()
        elif self.status == self.BACKWARD:
            self.backward()
        else:
            self.stop()

    def right(self):
        self.logger.debug(self.caller, "right")
        if self.status == self.FORWARD:
            self.in1.duty_u16(self.FORWARD_BACKWARD_DUTY)
            self.in2.duty_u16(0)
            self.in3.duty_u16(0)
            self.in4.duty_u16(self.LEFT_RIGHT_DUTY)
        if self.status == self.BACKWARD:
            self.in1.duty_u16(0)
            self.in2.duty_u16(self.FORWARD_BACKWARD_DUTY)
            self.in3.duty_u16(self.LEFT_RIGHT_DUTY)
            self.in4.duty_u16(0)

    def right_stop(self):
        self.logger.debug(self.caller, "right_stop")
        if self.status == self.FORWARD:
            self.forward()
        elif self.status == self.BACKWARD:
            self.backward()
        else:
            self.stop()

    def forward(self):
        self.logger.debug(self.caller, "forward")
        self.status = self.FORWARD
        self.in1.duty_u16(self.FORWARD_BACKWARD_DUTY)
        self.in2.duty_u16(0)
        self.in3.duty_u16(0)
        self.in4.duty_u16(self.FORWARD_BACKWARD_DUTY)

    def backward(self):
        self.logger.debug(self.caller, "backward")
        self.status = self.BACKWARD
        self.in1.duty_u16(0)
        self.in2.duty_u16(self.FORWARD_BACKWARD_DUTY)
        self.in3.duty_u16(self.FORWARD_BACKWARD_DUTY)
        self.in4.duty_u16(0)

    def stop(self):
        self.logger.debug(self.caller, "stop")
        self.status = self.STOP
        self.in1.duty_u16(0)
        self.in2.duty_u16(0)
        self.in3.duty_u16(0)
        self.in4.duty_u16(0)
