from threading import Thread

import cv2


class Video:

    def __init__(self, cam_configs: dict):
        self.cam = cv2.VideoCapture(cam_configs['address'])
        self.frame = None

    def update_cam_attr(self):
        while True:
            if self.cam.isOpened():
                self.cam.grab()
                (cam_status, self.frame) = self.cam.retrieve()

    def run(self, stream_video: bool = False):
        thread_update_cam = Thread(target=self.update_cam_attr, args=())
        thread_update_cam.start()

        if stream_video:
            thread3 = Thread(target=self.stream_video, args=())
            thread3.start()

    def stream_video(self):
        while True:
            if self.frame is not None:
                cv2.imshow('frame', self.frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.cam.release()
                    break
