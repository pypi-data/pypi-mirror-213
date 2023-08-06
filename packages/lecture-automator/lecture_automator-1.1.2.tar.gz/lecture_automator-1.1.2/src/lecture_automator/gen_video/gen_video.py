from typing import List

from moviepy.editor import AudioFileClip, ImageClip, concatenate


def generate_video(path_images: List[str], path_wavs: List[str],
                   output_name: str) -> None:
    """Генерация видео на основе изображений и звука к каждому из них.

    Args:
        path_images (List[str]): список путей к изображениям в файловой системе.
        path_wavs (List[str]): список путей к звукам в файловой системе (каждый звук
        соответствует изображению с таким же индексом).
        output_name (str): название выходного видео.
    """

    clips = []
    for path_image, path_wav in zip(path_images, path_wavs):
        image_clip = ImageClip(path_image)
        audio = AudioFileClip(path_wav)
        image_clip = image_clip.set_audio(audio).set_duration(audio.duration)
        clips.append(image_clip)

    video = concatenate(clips)

    video.write_videofile(
        output_name, fps=24, logger=None)
