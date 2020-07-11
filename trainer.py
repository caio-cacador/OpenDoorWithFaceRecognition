from os import path, listdir
import pickle
import dlib
import cv2
import numpy as np
from OpenDoorWithFaceRecognition.sources.constants import BASE_DIR, MEDIA_ROOT, SOURCES


class Trainer:
    def __init__(self):
        print('[+] Loading files...')
        self.detectorFace = dlib.get_frontal_face_detector()
        self.detectorPontos = dlib.shape_predictor(path.join(SOURCES, "shape_predictor_68_face_landmarks.dat"))
        self.reconhecimentoFacial = dlib.face_recognition_model_v1(
            path.join(SOURCES, "dlib_face_recognition_resnet_model_v1.dat"))
        print('[-] Done.')

    def run(self):
        print('[+] Training...')
        indice = {}
        descritoresFaciais = None
        persons = [dir for dir in listdir(MEDIA_ROOT) if path.isdir(path.join(MEDIA_ROOT, dir))]

        for person in persons:
            entire_path = path.join(MEDIA_ROOT, person)
            print(' - Person: ', person)
            for count, img_path in enumerate(listdir(entire_path)):
                imagem = cv2.imread(path.join(entire_path, img_path))

                facesDetectadas = self.detectorFace(imagem, 1)
                if len(facesDetectadas) != 1:
                    raise ValueError('Foi detectado mais de uma face na foto: ', img_path)

                face = facesDetectadas[0]
                pontosFaciais = self.detectorPontos(imagem, face)
                descritorFacial = self.reconhecimentoFacial.compute_face_descriptor(imagem, pontosFaciais)

                if not descritorFacial:
                    ValueError('Nao foi possivel detectar nenhum ponto facial')

                listaDescritorFacial = [df for df in descritorFacial]
                npArrayDescritorFacial = np.asarray(listaDescritorFacial, dtype=np.float64)
                npArrayDescritorFacial = npArrayDescritorFacial[np.newaxis, :]

                if descritoresFaciais is None:
                    descritoresFaciais = npArrayDescritorFacial
                else:
                    descritoresFaciais = np.concatenate((descritoresFaciais, npArrayDescritorFacial), axis=0)
                indice[count] = person

        np.save(path.join(SOURCES, "descritores_rn.npy"), descritoresFaciais)
        pickle_out = open(path.join(SOURCES, "persons.pickle"), 'wb')
        pickle.dump(indice, pickle_out)
        pickle_out.close()
        print('[-] Done.')


if __name__ == "__main__":
    t = Trainer()
    t.run()
