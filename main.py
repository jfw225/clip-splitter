import cv2

import core.config as cfg
from core.controller import Controller

PATH = "test.mp4"


def main():
    c = Controller(PATH)

    while True:
        c.get_input()
        for _ in c:
            pass

    # cap = cv2.VideoCapture(PATH)

    # while cap.isOpened():
    #     ret, frame = cap.read()
    #     if not ret:
    #         break

    #     cv2.imshow("Video", frame)
    #     cv2.waitKey(cfg.VIDEO.FPS)

    # cap.release()


if __name__ == '__main__':
    main()
