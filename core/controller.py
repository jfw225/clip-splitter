import cv2

import core.config as cfg
from utils.utils import save_video
from utils.input_map import KeyInputs


class Controller(dict):
    def __init__(self, path):
        mappings = [(val, getattr(self, key))
                    for key, val in KeyInputs.__dict__.items()
                    if not key.startswith("__")]

        super().__init__(mappings)

        self.path = path
        self.reset()

    def reset(self):
        self.cap = None
        self.fps = 0
        self.fps_save = cfg.VIDEO.FPS
        self.frames = list()
        self.current_frame = 0

        self.clip_frame = None
        self.num_clips = 0

    def get_input(self):
        inp = input(
            "\nPlease provide the path to the video that you would like to clip: ")
        self.path = inp

    def __iter__(self):
        return self.generator()

    def generator(self):
        """ Yields the video playback. """

        self.cap = cv2.VideoCapture(self.path)

        num_frames = 0

        while self.cap.isOpened():
            self.current_frame += 1

            print(
                f"Current Frame: {self.current_frame} | Speed: {self.fps} ms per frame")

            if self.current_frame >= num_frames:
                ret, frame = self.cap.read()

                if not ret:
                    if self.clip_frame is not None:
                        self.TOGGLE_CLIP()

                    self.cap.release()
                    cv2.destroyAllWindows()
                    self.reset()

                    return

                self.frames.append(frame)

                num_frames += 1
            else:
                frame = self.frames[self.current_frame]

            cv2.imshow(self.path, frame)

            while not self.map_input(cv2.waitKeyEx(self.fps)):
                pass

            yield None

    def map_input(self, raw_input):
        # print("Raw Input: " + str(raw_input))
        func = self.get(raw_input)
        if func:
            func()

            return True

        return False

    def NOP(self):
        pass

    def EXIT(self):
        print("Exiting...")
        exit()

    def TOGGLE_CLIP(self):
        if self.clip_frame is None:
            self.clip_frame = self.current_frame
        else:
            output_frames = self.frames[self.clip_frame:self.current_frame]
            clip_name = self.path + "_clip_" + str(self.num_clips) + ".mp4"
            print("Writing clip to: " + clip_name)
            save_video(self.cap, clip_name, output_frames)

            self.clip_frame = None
            self.num_clips += 1

    def TOGGLE_PLAYBACK(self):
        if self.fps:
            self.fps_save = self.fps
            self.fps = 0
        else:
            self.fps = self.fps_save

    def NEXT_FRAME(self):
        if self.fps:
            self.fps = 0

    def PREVIOUS_FRAME(self):
        if self.fps:
            self.fps = 0

        self.current_frame -= 2

    def UP_FPS(self):
        self.fps = max(self.fps - 1, 1)

    def DOWN_FPS(self):
        self.fps = self.fps + 1
