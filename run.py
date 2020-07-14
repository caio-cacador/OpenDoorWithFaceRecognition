import ujson as ujson
from OpenDoorWithFaceRecognition.arduino.arduino import Arduino
from OpenDoorWithFaceRecognition.face_recognition.recognition import Recognition
from time import sleep

from OpenDoorWithFaceRecognition.telegram.telegram import Telegram
from OpenDoorWithFaceRecognition.video.video import Video

if __name__ == "__main__":

    configs = ujson.load(open('configs.json', 'r'))

    recognition = Recognition()
    arduino = Arduino(configs=configs['arduino_configs'])
    telegram = Telegram(configs=configs['telegram_configs'])
    video = Video(cam_configs=configs['cam_configs'])
    video.run()

    print('[+] Online.')
    telegram.send_message(text='[+] Online.')
    while True:

        if arduino.get_btn_door_status():

            if recognition.process_image(video.frame):
                arduino.unlock_door()

            elif arduino.get_btn_inside_status():
                arduino.unlock_door()

            elif arduino.get_btn_outside_status():
                telegram.send_photo(video.frame)
                response = telegram.send_bool_question("Posso destrancar a porta para esta pessoa?")
                if response is True:
                    telegram.send_message(text='Ok, abrindo...')
                    arduino.unlock_door()
                else:
                    telegram.send_message(text='Tudo bem, não vou destrancar.')

            else:
                arduino.lock_door()

        sleep(0.3)
