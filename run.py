import ujson as ujson
from OpenDoorWithFaceRecognition.arduino.arduino import Arduino
from OpenDoorWithFaceRecognition.face_recognition.recognition import Recognition
from time import sleep

from OpenDoorWithFaceRecognition.telegram.telegram import Telegram
from OpenDoorWithFaceRecognition.video.camera import Camera

if __name__ == "__main__":

    configs = ujson.load(open('configs.json', 'r'))

    recognition = Recognition(configs=configs['recognition_configs'])
    arduino = Arduino(configs=configs['arduino_configs'])
    telegram = Telegram(configs=configs['telegram_configs'])
    camera = Camera(cam_configs=configs['cam_configs'])
    camera.start_update()

    print('[+] Online.')
    telegram.send_message(text='[+] Online.')
    while True:

        if arduino.get_btn_door_status():

            if recognition.process_image(camera.frame):
                arduino.unlock_door()

            elif arduino.get_btn_inside_status():
                arduino.unlock_door()

            elif arduino.get_btn_outside_status():
                telegram.send_photo(camera.frame)
                response = telegram.send_bool_question("Posso destrancar a porta para esta pessoa?")
                if response is True:
                    telegram.send_message(text='Ok, destrancando...')
                    arduino.unlock_door()
                else:
                    telegram.send_message(text='Tudo bem, não vou destrancar.')

            else:
                arduino.lock_door()

        sleep(0.3)
