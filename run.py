from OpenDoorWithFaceRecognition.face_recognition.recognition import Recognition

if __name__ == "__main__":
    recognize = Recognition()
    recognize.run(cam_address='rtsp://admin:XTKDRI@192.168.0.163/')
