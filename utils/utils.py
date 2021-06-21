import cv2


def set_saved_video(input_video, output_video, size):
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    fps = int(input_video.get(cv2.CAP_PROP_FPS))
    video = cv2.VideoWriter(output_video, fourcc, fps, size)

    return video


def save_video(input_video, output_path, frames):
    video = set_saved_video(input_video, output_path,
                            frames[0].shape[:-1][::-1])
    for frame in frames:
        video.write(frame)

    video.release()


def draw_text(image, text, pos):
    pass
