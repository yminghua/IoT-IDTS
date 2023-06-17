import pigpio

class Servo():
    MAX_PW = 1250  # 0.5/20*100
    MIN_PW = 250 # 2.5/20*100
    _freq = 50 # 50 Hz, 20ms
 
    def __init__(self, pin, min_angle=-90, max_angle=90):

        self.pi = pigpio.pi()
        self.pin = pin 
        self.pi.set_PWM_frequency(self.pin, self._freq)
        self.pi.set_PWM_range(self.pin, 10000)      
        self.angle = 0
        self.max_angle = max_angle
        self.min_angle = min_angle
        self.pi.set_PWM_dutycycle(self.pin, 0)

    def set_angle(self, angle):
        if angle > self.max_angle:
            angle = self.max_angle
        elif angle < self.min_angle:
            angle = self.min_angle
        self.angle = angle
        duty = self.map(angle, -90, 90, 250, 1250)
        self.pi.set_PWM_dutycycle(self.pin, duty)


    def get_angle(self):
        return self.angle

    # will be called automatically when the object is deleted
    # def __del__(self):
    #     pass

    def map(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    
    
def check_pan_angle(angle):
    if angle >= 90:
        return 90
    elif angle <= -90:
        return -90
    else:
        return angle
    

def check_tilt_angle(angle):
    if angle >= 30:
        return 30
    elif angle <= -30:
        return -30
    else:
        return angle


def calculate_angle(x, y):
    central_x = 320
    central_y = 240
    pan_angle = int((x-central_x)/50)
    tilt_angle = int((y-central_y)/50)
    return pan_angle, tilt_angle
    

if __name__ =='__main__':
    from time import sleep
    
    pan = Servo(pin=12, max_angle=90, min_angle=-90)
    tilt = Servo(pin=13, max_angle=30, min_angle=-30)
    panAngle = 0
    tiltAngle = 0
    pan.set_angle(panAngle)
    tilt.set_angle(tiltAngle)
    sleep(1)

    while True:
        for angle in range(0, 90, 1):
            pan.set_angle(angle)
            tilt.set_angle(angle)
            sleep(.01)
        sleep(.5)
        for angle in range(90, -90, -1):
            pan.set_angle(angle)
            tilt.set_angle(angle)
            sleep(.01)
        sleep(.5)
        for angle in range(-90, 0, 1):
            pan.set_angle(angle)
            tilt.set_angle(angle)
            sleep(.01)
        sleep(.5)

