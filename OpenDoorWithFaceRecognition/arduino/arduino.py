from pyfirmata import Arduino as PyfirmataArduino, util
from time import sleep


class Arduino():

    _UNLOCK_POSITION = 0
    _LOCK_POSITION = 170

    def __init__(self, configs: dict):
        arduino = PyfirmataArduino(configs['usb_port'])
        print('Arduino is online!')
        it = util.Iterator(arduino)
        it.start()

        self._btn_door = arduino.get_pin('d:6:i')
        self._btn_door.enable_reporting()
        self._btn_outside = arduino.get_pin('d:5:i')
        self._btn_outside.enable_reporting()
        self._btn_inside = arduino.get_pin('d:4:i')
        self._btn_inside.enable_reporting()

        self._servo_motor = arduino.get_pin('d:9:s')
        self._servo_motor.write(0)
        self._servo_position = 0
        self._servo_is_in_use = False

    def get_btn_door_status(self) -> bool:
        return self._btn_door.read()

    def get_btn_outside_status(self) -> bool:
        return self._btn_outside.read()

    def get_btn_inside_status(self) -> bool:
        return self._btn_inside.read()

    def unlock_door(self):
        if self._servo_is_in_use is False:
            self._servo_is_in_use = True
            if self.get_btn_door_status() and self._servo_position > self._UNLOCK_POSITION:
                print('[-] Destrancando a porta')
                while self._servo_position > self._UNLOCK_POSITION:
                    self._servo_position -= 2
                    self._servo_motor.write(self._servo_position)
                    sleep(0.02)
                sleep(3)
            else:
                print('[-] A porta ja esta destrancada')
            self._servo_is_in_use = False

    def lock_door(self):
        if self._servo_is_in_use is False:
            self._servo_is_in_use = True
            if self.get_btn_door_status() and not (self.get_btn_outside_status() or self.get_btn_inside_status())\
                    and self._servo_position < self._LOCK_POSITION:
                print('[-] Trancando a porta')
                while self._servo_position < self._LOCK_POSITION:
                    self._servo_position += 2
                    self._servo_motor.write(self._servo_position)
                    sleep(0.02)
                sleep(1)
            else:
                print('[-] Porta ja esta trancada')
            self._servo_is_in_use = False

# a = Arduino('/dev/ttyUSB0')
# a.run()
