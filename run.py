import ujson as ujson
from OpenDoorWithFaceRecognition.arduino.arduino import Arduino
from OpenDoorWithFaceRecognition.face_recognition.recognition import Recognition
from time import sleep

from OpenDoorWithFaceRecognition.telegram.telegram import Telegram

if __name__ == "__main__":

    configs = ujson.load(open('configs.json', 'r'))

    arduino = Arduino(configs=configs['arduino_configs'])
    telegram = Telegram(configs=configs['telegram_configs'])

    recognition = Recognition(cam_configs=configs['cam_configs'], arduino=arduino)
    recognition.run()

    while True:

        print('[+] Online.')
        if arduino.get_btn_door_status():
            arduino.lock_door()

        if arduino.get_btn_inside_status():
            arduino.unlock_door()

        if arduino.get_btn_outside_status(): # and bt door is true
            telegram.send_photo(recognition.frame)
            response = telegram.send_bool_question("Posso abrir a porta para esta pessoa?")
            if response is True:
                telegram.send_message(text='Ok, abrindo...')
                arduino.unlock_door()
            else:
                telegram.send_message(text='Tudo bem, nao vou abrir.')

        sleep(0.5)
