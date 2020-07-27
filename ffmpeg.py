import shlex
import subprocess
import json

from const import qp_str, pts_time_str, y_str, streams_str, x_str, side_data_str, video_stream_str, audio_stream_str, \
    codec_type_str
from shutil import which


def get_packets_info(file_path):
    """
    Get packet data using ffprobe to calculate the bitrate
    :param file_path input video file path
    :return information of packet
    """
    if which('ffprobe') is None:
        raise Exception('No ffprobe found in path')
    cmd = 'ffprobe -show_packets -of json'
    args = shlex.split(cmd)
    args.append(file_path)
    output = subprocess.check_output(args, stderr=subprocess.DEVNULL)
    output = json.loads(output)
    return output


def get_stream_info(file_path):
    """
    Get video stream information using ffprobe
    :param file_path input video file path
    :return information of stream
    """
    if which('ffprobe') is None:
        raise Exception('No ffprobe found in path')
    cmd = 'ffprobe -show_streams -of json'
    args = shlex.split(cmd)
    args.append(file_path)
    output = subprocess.check_output(args, stderr=subprocess.DEVNULL)
    output = json.loads(output)
    streams = output[streams_str]
    data = {video_stream_str: [], audio_stream_str: []}
    for stream in streams:
        data[stream[codec_type_str] + '_stream'].append(stream)
    return data


def generate_vis_video(file_path, folder_path, op):
    """
    Generate visualization video from ffmpeg codecview filter using subprocess
    :param file_path input video file path
    :param folder_path output folder path
    :param op option of codecview filter (qp, bs, b_type)
    """
    if which('ffmpeg') is None:
        raise Exception('No ffmpeg found in path')
    cmd = 'ffmpeg -export_side_data +venc_params -i ' + file_path + ' -vf codecview=' + op + '=true -y'
    args = shlex.split(cmd)
    args.append(folder_path + '/report/' + op + '_vis.mp4')
    proc = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    proc.communicate()
    if proc.returncode != 0:
        raise Exception('No ffmpeg command found, please check the version of your ffmpeg')


def get_qp_data(file_path):
    """
    Get basic qp data from ffmpeg using subprocess
    :param file_path input video file path
    :return basic qp per frame
    """
    if which('ffmpeg') is None:
        raise Exception('No ffmpeg found in path')
    cmd = 'ffmpeg -export_side_data +venc_params -i ' + file_path + ' -vf showinfo -f null -'
    args = shlex.split(cmd)
    proc = subprocess.Popen(args, stderr=subprocess.PIPE)
    data = {x_str: [], y_str: []}
    while True:
        output = proc.stderr.readline().decode('utf-8')
        if output == '' or proc.poll() is not None:
            break
        if output.find(pts_time_str) != -1:
            start = output.find(pts_time_str) + len(pts_time_str) + 1
            end = output.find(' ', output.find(pts_time_str))
            data[x_str].append(output[start:end])
        if output.find(side_data_str) != -1:
            start = output.find(qp_str) + len(qp_str) + 1
            end = output.find(';', start)
            data[y_str].append(output[start:end])
    return data
