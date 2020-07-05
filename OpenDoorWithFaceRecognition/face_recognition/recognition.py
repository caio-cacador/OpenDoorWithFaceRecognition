import pickle, dlib, cv2, os
import numpy as np
from datetime import datetime
from threading import Thread
from OpenDoorWithFaceRecognition.arduino.arduino import Arduino
from OpenDoorWithFaceRecognition.arduino.constants import UNLOCK_DOOR, LOCK_DOOR
# from sqlite_manager import Manager

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCES_DIR = os.path.join(BASE_DIR, 'sources')
IA_DIR = os.path.join(BASE_DIR, 'controleDeAcesso', 'core', 'static', 'ia')
path_write = IA_DIR + '\\dlib.jpeg'
path_read = IA_DIR + '\\original.jpeg'


class Recognition:

    def __init__(self):
        self.face_detector = dlib.get_frontal_face_detector()
        self.points_detector = dlib.shape_predictor(SOURCES_DIR + "\\shape_predictor_68_face_landmarks.dat")
        self.face_recognition = dlib.face_recognition_model_v1(SOURCES_DIR + "\\dlib_face_recognition_resnet_model_v1.dat")
        self.indices = pickle.load(open(SOURCES_DIR + "\\categories.pickle", 'rb'))
        self.descritoresFaciais = np.load(SOURCES_DIR + "\\descritores_rn.npy")
        self.limiar = 0.5
        self.arduino = Arduino()

    def process_image(self, imagem):
        faces_detectadas = self.face_detector(imagem, 2)
        if faces_detectadas:
            face = faces_detectadas[0]
            e, t, d, b = (int(face.left()), int(face.top()), int(face.right()), int(face.bottom()))
            pontos_faciais = self.points_detector(imagem, face)
            descritor_facial = self.face_recognition.compute_face_descriptor(imagem, pontos_faciais)
            lista_descritor_facial = [fd for fd in descritor_facial]
            np_array_descritor_facial = np.asarray(lista_descritor_facial, dtype=np.float64)
            np_array_descritor_facial = np_array_descritor_facial[np.newaxis, :]

            distancias = np.linalg.norm(np_array_descritor_facial - self.descritoresFaciais, axis=1)
            minimo = np.argmin(distancias)
            distancia_minima = distancias[minimo]

            if distancia_minima <= self.limiar:
                # nome = self.indices[minimo]
                self.arduino.send_command(UNLOCK_DOOR)

            # else:
                # nome = 'Desconhecido(a)'

            # dist = (str(1.0 - distancia_minima).split('.')[1])[:2]
            # cv2.rectangle(imagem, (e, t), (d, b), (255, 0, 0), 2)
            # texto = "{} {}%".format(nome, dist)
            # cv2.putText(imagem, texto, (d, t), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (255, 0, 0))

    def run(self, cam_address):
        print('[+] Running...')
        fps = 0
        last_frame = datetime.now().time().second
        cap = cv2.VideoCapture(cam_address)

        while True:
            frame = cv2.imread(path_read)
            if frame is not None:
                imagem = cv2.resize(frame, (400, 300))
                # Thread(name="Thread", target=self.process_image(imagem)).start()
                self.process_image(imagem)

                if datetime.now().time().second == last_frame:
                    fps += 1
                else:
                    print('[-] Fps: ', fps)
                    last_frame = datetime.now().time().second
                    fps = 0
            else:
                pass

        cv2.destroyAllWindows()
        print('finished...')
