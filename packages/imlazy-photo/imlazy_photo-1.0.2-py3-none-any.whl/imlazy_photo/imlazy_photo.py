import os
import time
import shutil


IMG_FORMAT = ['jpg', 'jpeg', 'gif', 'heic']
VIDEO_FORMAT = ['mp4', 'avi']
VALID_FORMAT = IMG_FORMAT + VIDEO_FORMAT


def sort_photo():
    c_path = os.getcwd()
    file_list = os.listdir(c_path)
    result = {}

    for file_name in file_list:
        if os.path.isdir(file_name) or file_name.split('.')[1].lower() not in VALID_FORMAT:
            continue
            
        etime = os.path.getmtime(file_name)
        created = f"{c_path}/{time.strftime('%Y%m%d', time.localtime(etime))}"

        if created in result.keys():
            result[created].append(file_name)
        else:
            result[created] = []
            result[created].append(file_name)

    return result
    

def make_dir_move_file(path_dict):
    for path, file_list in path_dict.items():
        try:
            if not os.path.exists(path):
                os.makedirs(path)
                _move_file(file_list, path)
        except OSError as e:
            _move_file(file_list, path)

def _move_file(file_list, path):
    has_video_dir = False if not os.path.exists(f'{path}/video_clips') else True


    for file_name in file_list:
        if file_name.split('.')[1].lower() in IMG_FORMAT:
            pass
            shutil.move(file_name, f'{path}/{file_name}')
        elif file_name.split('.')[1].lower() in VIDEO_FORMAT:

            if not has_video_dir:
                os.makedirs(f'{path}/video_clips')
                has_video_dir = True

            shutil.move(file_name, f'{path}/video_clips/{file_name}')
