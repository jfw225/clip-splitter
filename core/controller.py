import os
import cv2
from collections import deque

import core.config as cfg
from utils.utils import draw_recording, save_video, draw_info, draw_recording
from utils.input_map import KeyInputs


class Controller(dict):
    def __init__(self, path):
        mappings = [(val, getattr(self, key))
                    for key, val in KeyInputs.__dict__.items()
                    if not key.startswith("__")]

        super().__init__(mappings)

        os.makedirs(cfg.DIR.OUTPUT, exist_ok=True)

        self.path = path
        self.reset()

    def reset(self):
        self.cap = None
        self.fps = 0
        self.fps_save = cfg.VIDEO.FPS
        self.frames = deque(maxlen=cfg.VIDEO.CACHE_SIZE)
        self.current_frame = 0
        self.total_frames = 0

        self.clip_frame = None
        self.num_clips = 0

    def get_input(self):
        inp = input(
            "\nPlease provide the path to the video that you would like to clip: ")
        self.path = inp.replace("'", "").replace('"', "")

    def __iter__(self):
        return self.generator()

    def generator(self):
        """ Yields the video playback. """

        self.cap = cv2.VideoCapture(self.path)
        MAX_FRAMES = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

        while self.cap.isOpened():
            print(
                f"Current Frame: {self.current_frame} | Speed: {self.fps} ms per frame")

            if self.current_frame >= self.total_frames:
                ret, frame = self.cap.read()

                if not ret:
                    if self.clip_frame is not None:
                        self.TOGGLE_CLIP()

                    self.cap.release()
                    cv2.destroyAllWindows()
                    self.reset()

                    return

                self.frames.append(frame)

                self.total_frames += 1
            else:
                frame_number = self.get_frame_number(self.current_frame)
                frame = self.frames[frame_number]

            frame = frame.copy()

            draw_info(frame, self.current_frame, self.fps, MAX_FRAMES)

            if self.clip_frame is not None:
                draw_recording(frame)

            cv2.imshow(self.path, frame)

            while not self.map_input(cv2.waitKeyEx(self.fps)):
                pass

            self.current_frame += 1
            yield None

    def get_frame_number(self, cf):

        return max(0, len(self.frames) - (self.total_frames - cf))

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
            # Allow frames to grow unrestricted
            self.frames = deque(self.frames)
            self.clip_frame = self.current_frame
        else:
            fni = self.get_frame_number(self.clip_frame)
            fnf = self.get_frame_number(self.current_frame)
            output_frames = [self.frames[i] for i in range(fni, fnf)]
            self.frames = deque(self.frames, maxlen=cfg.VIDEO.CACHE_SIZE)
            basename = os.path.splitext(os.path.basename(self.path))[0]
            clip_name = basename + "_clip_" + str(self.num_clips) + ".mp4"
            output_path = os.path.join(cfg.DIR.OUTPUT, clip_name)
            print("Writing clip to: " + output_path)
            save_video(self.cap, output_path, output_frames)

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
