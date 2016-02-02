from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json
import RPi.GPIO as GPIO

class MotorIf(object):
    def __getitem__(self, key):
        return getattr(self, key)
    
    def __setitem__(self, key, value):
        setattr(self, key, value)
    
    def __init__(self, fwdPin, revPin, pwmPin):
        self = {}
        self['fwdPin'] = fwdPin
        self['revPin'] = revPin
        self['pwmPin'] = pwmPin
        self['running'] = False
        GPIO.setup(fwdPin,GPIO.OUT)
        GPIO.setup(revPin,GPIO.OUT)
        GPIO.setup(pwmPin,GPIO.OUT)
        self['pwm'] = GPIO.PWM(pwmPin,100)
        
    def set_speed(self, speed):
        self['speed'] = speed
        if speed == 0:
            GPIO.output(self['revPin'],GPIO.LOW)
            GPIO.output(self['fwdPin'],GPIO.LOW)
            self['pwm'].stop()
            self['running'] = False
        else :
            if not self['running']:
                self['pwm'].start(speed)
                self['running'] = True
            else:
                self['pwm'].ChangeDutyCycle(speed)

    def set_direction(self, dir):
        if dir == 'FORWARD':
            GPIO.output(self['revPin'],GPIO.LOW)
            GPIO.output(self['fwdPin'],GPIO.HIGH)
        elif dir == 'BACKWARD':
            GPIO.output(self['revPin'],GPIO.HIGH)
            GPIO.output(self['fwdPin'],GPIO.LOW)
        
    def stop(self):
        self.set_speed(0)

class SBRHandler(BaseHTTPRequestHandler, object):
    def setup(self):
        GPIO.setmode(GPIO.BOARD)
        self['mL'] = MotorIf(33,35,37)
        self['mR'] = MotorIf(36,38,40)
        self['mR'].set_speed(50)
        self['mL'].set_speed(50)
        self['mL'].set_direction('FORWARD')
        self['mR'].set_direction('FORWARD')

    def __getitem__(self, key):
        return getattr(self, key)
    
    def __setitem__(self, key, value):
        setattr(self, key, value)
        
    def __init__(self, *args, **kwargs):
        self.data = { 'status': 'ok' }
        self.setup()
        super(SBRHandler, self).__init__(*args,**kwargs)

    def do_GET(self):
        self.send_response(200,"OK")
        self.send_header('content-type','text/json')
        self.end_headers()
        self.wfile.write(json.dumps(self.data))
        pass
    
    def do_POST(self):
        pass
    def do_PUT(self):
        pass

try:
    
    serv = HTTPServer(("",8080),SBRHandler)
    serv.serve_forever()
    
except KeyboardInterrupt:
    GPIO.cleanup()
    pass

