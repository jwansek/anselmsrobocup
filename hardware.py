import RPi.GPIO as GPIO

class DCMotor:
    def __init__(self, p_pwm, p_dir, initpower):
        self._p_pwm = p_pwm
        self._p_dir = p_dir
        self.power = initpower

        GPIO.setup(self._p_pwm, GPIO.OUT)
        GPIO.setup(self._p_dir, GPIO.OUT)

        self._motor = GPIO.PWM(self._p_pwm, self.power)
        self._motor.start(0)

    def __exit__(self):
        self._motor.stop()

    def __del__(self):
        self._motor.stop()

    def forwards(self, power = None):
        GPIO.output(self._p_dir, 0)
        if power is None:
            self._motor.ChangeDutyCycle(self.power)
        else:
            self._motor.ChangeDutyCycle(power)

    def backwards(self, power = None):
        GPIO.output(self._p_dir, 1)
        if power is None:
            self._motor.ChangeDutyCycle(self.power)
        else:
            self._motor.ChangeDutyCycle(power)

        
