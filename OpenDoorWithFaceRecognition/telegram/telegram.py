from collections import namedtuple
from telepot import Bot, exception
from telepot.loop import MessageLoop
import cv2

LastMassageNamedtuple = namedtuple('LastMassage', ['chat_id', 'text'])


class BuffImage:

    def __init__(self, _type, image):
        self._type = _type
        self._image = image

    def read(self):
        s, img = cv2.imencode(self._type, self._image)
        return img.tobytes()


class Telegram:

    def __init__(self, configs: dict):
        self.bot = Bot(configs['token'])
        self._default_chat_id = configs['default_chat_id']
        self._accepted_names = configs['accepted_names']
        self._bot_name = configs['bot_name']

        self._last_message = None

        MessageLoop(self.bot, self._handle).run_as_thread()

    @property
    def get_last_message(self):
        return self._last_message.text if self._last_message else ''

    def _handle(self, msg):
        if msg:
            chat_id = msg['chat']['id']
            first_name = msg['from']['first_name']
            message = str(msg.get('text', ''))
            first_world = message[:len(self._bot_name)] if len(message) > (len(self._bot_name)+1) else None

            print(f"[-] ({chat_id}: ') >> {first_name} sent: {message}")

            print(f'first_world >> {first_world}')

            if first_world and first_world.lower() in self._accepted_names:
                message = message[len(self._bot_name)+1:]
                print(f'message >> {message}')
                self._last_message = LastMassageNamedtuple(chat_id=chat_id, text=message.lower())

    def send_photo(self, image, name: str = 'photo.png', _type: str = '.PNG', chat_id: int = None):
        if not chat_id:
            chat_id = self._default_chat_id
        self.bot.sendPhoto(chat_id, (name, BuffImage(_type=_type, image=image)))

    def send_message(self, text: str, chat_id: int = None):
        if not chat_id:
            chat_id = self._default_chat_id
        try:
            self.bot.sendMessage(chat_id, text)
        except exception.TelegramError:
            print(f'[-] Chat not found: {chat_id}')

    def send_bool_question(self, question: str, chat_id: int = None):
        attempts = 3
        self._last_message = None
        self.send_message(text=question, chat_id=chat_id)
        while attempts > 0:
            if self.get_last_message:
                attempts -= 1
                if self.get_last_message in ['sim', 'pode']:
                    return True
                elif self.get_last_message in ['nao', 'não', 'nao pode', 'não pode']:
                    return False
                else:
                    self.send_message(text="Por favor, responda com 'sim' ou 'não'.", chat_id=chat_id)
                    self._last_message = None
        return False

#
# TOKEN = "891967726:AAF4iR0AknoObf_L-rwKIwjIxzeGtYdeTM4"
#
# bot = telepot.Bot(TOKEN)
#
# chat_id = -1001318092698
#
#
#
# cam = cv2.VideoCapture('rtsp://admin:XTKDRI@192.168.0.163/')
# cam.grab()
# (cam_status, frame) = cam.retrieve()
# frame = cv2.resize(frame, (400, 300))
#
