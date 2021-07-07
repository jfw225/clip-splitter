import cv2

from core.config import VIDEO


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


def draw_text(image, text, size, color, pos):
    cv2.putText(image, text, pos, cv2.FONT_HERSHEY_SIMPLEX, size, color,
                VIDEO.FONT_THICK, lineType=cv2.LINE_AA)


def draw_info(image, cf, fps, max_frames):
    cf_text = f"Current Frame: {cf}/{max_frames}"
    fps_text = f"Current Speed: {1000//fps if fps else 0} fps"

    (tw, th), _ = cv2.getTextSize(cf_text, 0, VIDEO.FONT_SCALE, VIDEO.FONT_THICK)
    ih, iw, _ = image.shape
    pos = [iw - tw - 400, th]
    draw_text(image, cf_text, VIDEO.FONT_SCALE, (0, 0, 255), pos)
    pos[1] += th + 15
    draw_text(image, fps_text, VIDEO.FONT_SCALE, (0, 0, 255), pos)


def draw_recording(image):
    text = "Recording..."

    (tw, th), _ = cv2.getTextSize(text, 0, VIDEO.FONT_SCALE, VIDEO.FONT_THICK)
    pos = [5, th + 5]
    draw_text(image, text, VIDEO.FONT_SCALE, (0, 0, 255), pos)
