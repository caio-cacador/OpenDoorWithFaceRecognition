import pickle, dlib, cv2, os
import numpy as np
from OpenDoorWithFaceRecognition.arduino.arduino import Arduino
from OpenDoorWithFaceRecognition.sources.constants import SOURCES


class Recognition:

    def __init__(self):

        self.face_detector = dlib.get_frontal_face_detector()
        self.points_detector = dlib.shape_predictor(os.path.join(SOURCES, "shape_predictor_68_face_landmarks.dat"))
        self.face_recognition = dlib.face_recognition_model_v1(os.path.join(SOURCES, "dlib_face_recognition_resnet_model_v1.dat"))
        self.indices = pickle.load(open(os.path.join(SOURCES, "persons.pickle"), 'rb'))
        self.face_descriptors = np.load(os.path.join(SOURCES, "descritores_rn.npy"))
        self.limiar = 0.5

    def process_image(self, image):
        if image is not None:
            image_resized = cv2.resize(image, (400, 300))
            detected_faces = self.face_detector(image_resized, 2)
            for face in detected_faces:
                face_points = self.points_detector(image_resized, face)
                face_descriptors = self.face_recognition.compute_face_descriptor(image_resized, face_points)
                np_array_face_descriptor = np.asarray(face_descriptors, dtype=np.float64)
                np_array_face_descriptor = np_array_face_descriptor[np.newaxis, :]

                distancias = np.linalg.norm(np_array_face_descriptor - self.face_descriptors, axis=1)
                minimo = np.argmin(distancias)
                distancia_minima = distancias[minimo]

                if distancia_minima <= self.limiar:
                    nome = self.indices[minimo]
                    return nome

                dist = (str(1.0 - distancia_minima).split('.')[1])[:2]
                print(f'nome: {nome}, %{dist}')
        return None