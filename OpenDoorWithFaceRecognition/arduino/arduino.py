import serial

from OpenDoorWithFaceRecognition.arduino.constants import UNLOCK_DOOR, LOCK_DOOR, TURN_LIGHT_ON, TURN_LIGHT_OFF

DOORS_COMMANDS_MAP = {UNLOCK_DOOR: '1',
                      LOCK_DOOR:   '2'}

LIGHT_COMMANDS_MAP = {TURN_LIGHT_ON:  '1',
                      TURN_LIGHT_OFF: '2'}


class Arduino:

    def __init__(self):
        self.arduino = serial.Serial()
        self.arduino.baudrate = 9600
        self.arduino.port = 'COM3'
        self.arduino.open()

        self.door_status = UNLOCK_DOOR
        self.light_status = TURN_LIGHT_OFF

    def __del__(self):
        self.arduino.close()

    def send_command(self, command: str):
        if DOORS_COMMANDS_MAP.get(command):
            command_value = DOORS_COMMANDS_MAP[command]
            if self.door_status != command_value:
                self.arduino.write(b'{}'.__format__(command_value))
                self.door_status = command_value

        elif LIGHT_COMMANDS_MAP.get(command):
            command_value = LIGHT_COMMANDS_MAP[command]
            if self.light_status != command_value:
                self.arduino.write(b'{}'.__format__(command_value))
                self.light_status = command_value


    # def read_status(self):
    #     self.arduino.read_all()