import RPi.GPIO as GPIO
from time import sleep

class DCMotor:
    def __init__(self, p_pwm, p_dir, initpower, inversed = False):
        '''A class for communicating with an Ardumoto motor controller.
        remember to call GPIO.setmode(GPIO.BOARD) or
        GPIO.setmode(GPIO.BCM) before initalising this class. This
        changes the pin naming scheme. TBH, you probably just want to
        use GPIO.BOARD. This class takes three arguments: the pin
        connected to the pwm input on the ardumoto, the dir input on the
        ardumoto, and an initial power to use. Power is a percentage, but
        on the lower end there may not be much difference. No motors
        will fire until you want them to do. You can control the motors in
        three ways, forwards, backwards and stop. forwards and backwards
        have an optional argument, the power to use. This will change the
        power attribute. Else the method will use the current value of the
        power attribute. You can also change the power by changing the
        value of the power attribute. Remember to cleanup by deleting the
        object by using the 'del' keyword.

        Arguments:
            p_pwm {int} -- pin connected to the pwm input on the
            motor controller
            p_dir {int} -- pin connected to the dir input on the
            motor controller
            initpower {int} -- an initial power to use
            inversed {bool} -- inverses the direction. (default: {None})
        '''
        
        self._p_pwm = p_pwm
        self._p_dir = p_dir
        self.power = initpower
        self.inversed = inversed

        GPIO.setup(self._p_pwm, GPIO.OUT)
        GPIO.setup(self._p_dir, GPIO.OUT)

        self._motor = GPIO.PWM(self._p_pwm, self.power)
        self._motor.start(initpower)
        self.stop()

    def __exit__(self):
        self.__del__()

    def __del__(self):
        self._motor.stop()

    def forwards(self, power = None):
        '''Moves the rotation in a forwards direction.
        
        Keyword Arguments:
            power {int} -- Optional argument that changes the 
            power attribute to this (default: {None})
        '''
        
        if power is not None:
            self.power = power

        if not self.inversed:
            GPIO.output(self._p_dir, 0)
        else:
            GPIO.output(self._p_dir, 1)
            
        self._motor.ChangeDutyCycle(self.power)

    def backwards(self, power = None):
        '''Moves the rotation in a backwards direction.
        
        Keyword Arguments:
            power {int} -- Optional argument that changes the 
            power attribute to this (default: {None})
        '''
        
        if power is not None:
            self.power = power

        if not self.inversed:
            GPIO.output(self._p_dir, 1)
        else:
            GPIO.output(self._p_dir, 0)
            
        self._motor.ChangeDutyCycle(self.power)

    def stop(self):
        '''Stops the motor from any sort of rotation. Does
        not change the value of the power attribute.
        '''
        
        self._motor.ChangeDutyCycle(0)

#this will only get called when this program is run (not as an import)
#so its used for testing
if __name__ == "__main__":
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)

    a = DCMotor(15, 13, 100)
    a.forwards()
    sleep(5)
    a.power = 50
    a.backwards()
    sleep(5)
    a.stop()
    sleep(1)
    a.forwards(25)
    sleep(5)
    a.stop()
    del a

        
