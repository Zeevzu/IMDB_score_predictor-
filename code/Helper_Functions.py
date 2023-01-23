import os
from pytube import YouTube
import cv2 as cv
import numpy as np
import pickle


def youtube_to_mp4(url, path, name):
    """
    Creates an MP4 file in @path, with the file name @name.
    The video is Downloaded from Youtube in @url

    Parameters
    url : string
        trailer's url in youtube
    path : string
        the path in which you save the file
    name : string
        the wanted file name

    Returns
    -------
    new_path string
        the path where the file is located

    """
#link of the video to be downloaded
    new_path = path + name + '.mp4'
    if os.path.isfile(new_path):
      print('file ' + new_path + ' already exsists')
    else:
      old_path = YouTube(url).streams.filter(progressive=True, file_extension='mp4').order_by('resolution').first().download(path)
      os.rename(old_path, new_path)
    return new_path


def create_dir(video_path, dir_path):
    """
        Creates a dir in @dir_path, with the dir name of the the video name extracted from @dir_path.

        Parameters
        video_path : string
            the path for the video
        dir_path : string
            the path in which you create the dir

        Returns
        -------
        dir_name string
            the dir name
        video_name string
            the video name
        directory_already_exist bool
            state if there is already a dir with the wanted name

        """
    video_name = video_path.split('/')[-1].split('.mp4')[0]
    dir_name = f'{dir_path}/{video_name}/' .replace('\xa0','')
    try:
        os.makedirs(dir_name)
        directory_already_exist = False
    except:
        directory_already_exist = True
    return dir_name, video_name, directory_already_exist


def take_random_frames(video_path, frames_to_save):
    """
    takes randomly selected frames from a video trailer

    Parameters
    video_path : string
        path to the video file we take frames from
    frames_to_save : int
        approximate number of frames we take from the video before preprocessing

    Returns
    -------
    nd array
        a list of rgb frames from trailer

    """
    cam = cv.VideoCapture(video_path)
    frames_in_video = cam.get(cv.CAP_PROP_FRAME_COUNT)
    frame_list = []
    for i in range(frames_to_save):
        frame_index = np.random.randint(frames_in_video)
        cam.set(cv.CAP_PROP_POS_FRAMES, frame_index)
        ret, frame = cam.read()
        if ret:
            if np.median(frame) != 0:
                frame_list.append(frame)
    return np.unique(np.array(frame_list), axis=0)


def deleate_booring_frames(frame_list, percentage_to_clean):
    """
    deleates not intresting frames from an array of movie frames

    Parameters
    ----------
    frame_list : numpy nd array
        a "list" of rgb frames
     percentage_to_clean : flout
        approximate persentage of frames from randomly chosen frames to not save
        due to luck of intrest

    Returns
    -------
    frame_list : numpy nd array
        a "list" of rgb frames that are intersting (not a black screen, not text, ect"")

    """
    try:
        mean_list = np.mean(frame_list, axis=(1, 2, 3))
        std_list = np.std(frame_list[:, :, :, 0], axis=(1, 2))
        mean_threshold = np.percentile(mean_list, percentage_to_clean)
        std_threshold = np.percentile(std_list, percentage_to_clean)
        indices_to_save = (mean_list > mean_threshold) * (std_list > std_threshold)
        return frame_list[indices_to_save, :, :, :]
    except:
        return frame_list


def save_intresting_frames(video_path, frames_to_save, percentage_to_clean):
    """
    saves a few intresting frames from a movie trailer video

    Parameters
    ----------
    video_path : string
        path to the video file we take frames from
    frames_to_save : int
        approximate number of frames we take from the video before preprocessing
    percentage_to_clean : flout
        approximate persentage of frames from randomly chosen frames to not save
        due to luck of intrest

    Returns
    -------
    bool
        True if pictures are saved, false if the pictures were already saved in previes run

    """
    dir_name, video_name, directory_already_exist = create_dir(video_path, 'drive/MyDrive/DL project/final/images/' )
    if directory_already_exist:
        return False
    frame_list = take_random_frames(video_path, frames_to_save)
    frame_list = deleate_booring_frames(frame_list, percentage_to_clean)
    for index, frame in enumerate(frame_list):
        frame_file_name = f'{dir_name}{index}.jpg'
        # print(frame_file_name)
        # pdb.set_trace()
        cv.imwrite(frame_file_name, frame)
    return True


