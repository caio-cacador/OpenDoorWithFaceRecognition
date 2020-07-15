from os import path, listdir
import pickle
import dlib
import cv2
import numpy as np
from OpenDoorWithFaceRecognition.sources.constants import MEDIA_ROOT, SOURCES


print('[+] Loading files...')
face_detector = dlib.get_frontal_face_detector()
points_detector = dlib.shape_predictor(path.join(SOURCES, "shape_predictor_68_face_landmarks.dat"))
face_recognition = dlib.face_recognition_model_v1(path.join(SOURCES, "dlib_face_recognition_resnet_model_v1.dat"))

print('[-] Done.')

print('[+] Training...')
indices = {}
face_descriptors = None
persons = [dir for dir in listdir(MEDIA_ROOT) if path.isdir(path.join(MEDIA_ROOT, dir))]

for person in persons:
    person_path = path.join(MEDIA_ROOT, person)
    print(' - Person: ', person)
    for count, img_path in enumerate(listdir(person_path)):
        image = cv2.imread(path.join(person_path, img_path))

        detected_faces = face_detector(image)
        if not detected_faces:
            raise ValueError('Nao foi detectado nenhuma face na foto: ', img_path)
        if len(detected_faces) > 1:
            raise ValueError('Foi detectado mais de uma face na foto: ', img_path)

        face = detected_faces[0]
        face_points = points_detector(image, face)
        face_descriptor = face_recognition.compute_face_descriptor(image, face_points)

        if not face_descriptor:
            ValueError('Nao foi possivel detectar nenhum ponto facial')

        np_array_face_descriptor = np.asarray(list(face_descriptor), dtype=np.float64)
        np_array_face_descriptor = np_array_face_descriptor[np.newaxis, :]

        if face_descriptors is None:
            face_descriptors = np_array_face_descriptor
        else:
            face_descriptors = np.concatenate((face_descriptors, np_array_face_descriptor), axis=0)
        indices[count] = person

np.save(path.join(SOURCES, "descriptors_rn.npy"), face_descriptors)
pickle_out = open(path.join(SOURCES, "persons.pickle"), 'wb')
pickle.dump(indices, pickle_out)
pickle_out.close()
print('[-] Done.')
