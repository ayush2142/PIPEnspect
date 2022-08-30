import os
import shutil
import glob


def delete_video_files():
    file = glob.glob('temporary_data/frame_split/*')
    for f in file:
        os.remove(f)

    file = glob.glob('temporary_data/video_output_images/*')
    for f in file:
        os.remove(f)

    # file = glob.glob('temporary_data/videos/*')
    # for f in file:
    #     os.remove(f)


def delete_image_files():
    shutil.rmtree('runs/detect/exp')
    file = glob.glob('temporary_data/images/*')
    for f in file:
        os.remove(f)


def delete_exp_files():
    shutil.rmtree('runs/detect/exp')
