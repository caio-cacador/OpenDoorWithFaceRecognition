import pickle, dlib, cv2, os
from time import sleep

import numpy as np
from datetime import datetime
from threading import Thread
from OpenDoorWithFaceRecognition.arduino.arduino import Arduino
from OpenDoorWithFaceRecognition.sources.constants import BASE_DIR, SOURCES

IA_DIR = os.path.join(BASE_DIR, 'controleDeAcesso', 'core', 'static', 'ia')
path_write = IA_DIR + '\\dlib.jpeg'
path_read = IA_DIR + '\\original.jpeg'


class Recognition:

    def __init__(self, cam_configs: dict, arduino: Arduino):
        self.arduino = arduino

        self.face_detector = dlib.get_frontal_face_detector()
        self.points_detector = dlib.shape_predictor(os.path.join(SOURCES, "shape_predictor_68_face_landmarks.dat"))
        self.face_recognition = dlib.face_recognition_model_v1(os.path.join(SOURCES, "dlib_face_recognition_resnet_model_v1.dat"))
        self.indices = pickle.load(open(os.path.join(SOURCES, "persons.pickle"), 'rb'))
        self.descritoresFaciais = np.load(os.path.join(SOURCES, "descritores_rn.npy"))
        self.limiar = 0.5

        self.cam = cv2.VideoCapture(cam_configs['address'])
        self.cam_status = True
        self.frame = None

    def process_image(self):
        print('Thread of processing is ON')
        while True:
            if self.frame is not None:
                imagem = cv2.resize(self.frame, (400, 300))

                faces_detectadas = self.face_detector(imagem, 2)
                if faces_detectadas:
                    face = faces_detectadas[0]
                    # e, t, d, b = (int(face.left()), int(face.top()), int(face.right()), int(face.bottom()))
                    pontos_faciais = self.points_detector(imagem, face)
                    descritor_facial = self.face_recognition.compute_face_descriptor(imagem, pontos_faciais)
                    lista_descritor_facial = [fd for fd in descritor_facial]
                    np_array_descritor_facial = np.asarray(lista_descritor_facial, dtype=np.float64)
                    np_array_descritor_facial = np_array_descritor_facial[np.newaxis, :]

                    distancias = np.linalg.norm(np_array_descritor_facial - self.descritoresFaciais, axis=1)
                    minimo = np.argmin(distancias)
                    distancia_minima = distancias[minimo]

                    nome = 'Desconh1ecido(a)'
                    if distancia_minima <= self.limiar:
                        nome = self.indices[minimo]
                        self.arduino.unlock_door()

                    dist = (str(1.0 - distancia_minima).split('.')[1])[:2]
                    print(f'nome: {nome}, %{dist}')
                    # cv2.rectangle(imagem, (e, t), (d, b), (255, 0, 0), 2)
                    # texto = "{} {}%".format(nome, dist)
                    # cv2.putText(imagem, texto, (d, t), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (255, 0, 0))

                sleep(0.5)

    def stream_video(self):
        print('Thread of streaming is ON')
        while True:
            if self.frame is not None:
                cv2.imshow('frame', self.frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.cam.release()
                    # break
                    pass

    def update_cam_attr(self):
        print('Thread of update cam attr is ON')
        last_frame = 0
        fps = 0
        while True:
            if self.cam.isOpened():
                self.cam.grab()
                (self.cam_status, frame) = self.cam.retrieve()
                self.frame = cv2.resize(frame, (400, 300))
                # if datetime.now().time().second == last_frame:
                    # fps += 1
                # else:
                    # print('[-] Fps: ', fps)
                    # last_frame = datetime.now().time().second
                    # fps = 0

    def run(self, stream_video: bool = False):
        print('[+] Running...')
        fps = 0
        last_frame = datetime.now().time().second

        thread_update_cam = Thread(target=self.update_cam_attr, args=())
        thread_update_cam.daemon = True
        thread_update_cam.start()

        thread2 = Thread(target=self.process_image, args=())
        thread2.daemon = True
        thread2.start()

        if stream_video:
            thread3 = Thread(target=self.stream_video, args=())
            # thread1.daemon = True
            thread3.start()

        # try:
        #     while True:
        #         if self.frame is not None:
        #             image = cv2.resize(self.frame, (400, 300))
        #             Thread(name="Thread", target=self.process_image(imagem)).start()
        #             self.process_image(image)
        #
        #             if datetime.now().time().second == last_frame:
        #                 fps += 1
        #             else:
        #                 print('[-] Fps: ', fps)
        #                 last_frame = datetime.now().time().second
        #                 fps = 0

        # try:
        #     while True:
        #         pass
        # except Exception as ex:
        #     print(ex)
        #     self.cam.release()
        #     cv2.destroyAllWindows()
        #     pass
        #
        # self.cam.release()
        # cv2.destroyAllWindows()
        # print('finished...')
