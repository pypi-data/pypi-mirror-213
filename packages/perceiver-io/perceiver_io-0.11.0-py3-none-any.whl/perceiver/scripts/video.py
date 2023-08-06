import numpy as np
from PIL import Image

from perceiver.data.vision import video_utils


def create_side_by_side_video(video_1, video_2, max_size=500, axis=0):
    frames_video_1 = video_utils.read_video_frames(video_1)
    frames_video_2 = video_utils.read_video_frames(video_2)

    print(len(frames_video_1))
    print(len(frames_video_2))

    out_frames = []

    for f1, f2 in zip(frames_video_1, frames_video_2):
        tmp_1 = Image.fromarray(f1)
        tmp_2 = Image.fromarray(f2)

        tmp_1.thumbnail((max_size, max_size))
        tmp_2.thumbnail((max_size, max_size))

        f1 = np.array(tmp_1)
        f2 = np.array(tmp_2)

        out_frames.append(np.concatenate([f1, f2], axis=axis))

    video_utils.write_video("examples/sintel_clip_cave_dragon_fight_sbs.mp4", out_frames, fps=24)


if __name__ == "__main__":
    create_side_by_side_video(
        video_1="examples/sintel_clip_cave_dragon_fight.mp4",
        video_2="examples/sintel_clip_cave_dragon_fight_output.mp4",
        axis=1,
    )

    # Then run "ffmpeg -i sintel_clip_cave_dragon_fight_sbs.mp4 sintel_clip_cave_dragon_fight_sbs.gif"
