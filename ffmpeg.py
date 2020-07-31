import os
import shlex
import subprocess
import json

from const import *
from output import write_to_js
from shutil import which


def parse_frame_timestamp(packets):
    """
    Extract frame timestamp from packet data
    :param packets: packet data
    :return: frame timestamp
    """
    data = []
    pre_pts_time = -1
    for packet in packets:
        if packet[codec_type_str] == 'video' and float(packet[pts_time_str]) > pre_pts_time:
            data.append(packet[pts_time_str])
            pre_pts_time = float(packet[pts_time_str])
    return data


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
    output = json.loads(output)[packets_str]
    # output frame timestamps to js
    write_to_js('frame_ts', parse_frame_timestamp(output), data_js_path, 'a')
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
    :param op option of codecview filter (qp, mv, bs, b_type)
    """
    if which('ffmpeg') is None:
        raise Exception('No ffmpeg found in path')
    if op == mv_str:
        cmd = '../FFmpeg/ffmpeg -flags2 +export_mvs -i ' + file_path + ' -vf codecview=mv=pf+bf+bb -y'
    else:
        cmd = '../FFmpeg/ffmpeg -export_side_data +venc_params -i ' + file_path + ' -vf codecview=' + op + '=true -y'
    args = shlex.split(cmd)
    args.append(folder_path + '/report/' + op + '_vis.mp4')
    proc = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    proc.communicate()
    if proc.returncode != 0:
        raise Exception(op + ' video generates failed, please check the version of your ffmpeg')
    print(op + ' visualization video generated')


def get_qp_data(file_path):
    """
    Get basic qp data from ffmpeg using subprocess
    :param file_path input video file path
    :return directory key - pts, value - basic qp
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


def get_side_data_metric(line, name):
    """
    Get side data metric from output line
    :param line: console output line
    :param name: name of metric
    :return: metric value
    """
    start = line.find(name) + len(name) + 1
    end = line.find(';', start)
    return line[start:end]


def get_frame_data(file_path):
    """
    Get frame data from ffprobe using subprocess and store in js file
    :param file_path input video file path
    """
    cmd = 'ffprobe -show_frames -of json'
    args = shlex.split(cmd)
    args.append(file_path)
    output = subprocess.check_output(args, stderr=subprocess.DEVNULL)
    output = json.loads(output)
    frames = output[frames_str]
    data = {}
    f_idx = 0
    for frame in frames:
        if frame[media_type_str] == 'video':
            data[f_idx] = frame
            f_idx += 1
    get_frame_side_data(file_path, data)
    # output frame data to js
    write_to_js('frame_map', data, data_js_path, 'w')


def get_frame_side_data(file_path, data):
    """
    Get side data from ffmpeg using subprocess
    :param file_path input video file path
    :param data (dict) key - frame index, value: frame metrics object
    :return data (dict) with frame side data key - frame index, value: frame metrics object
    """
    cmd = 'ffmpeg -export_side_data +venc_params -i ' + file_path + ' -vf showinfo -f null -'
    args = shlex.split(cmd)
    proc = subprocess.Popen(args, stderr=subprocess.PIPE)
    f_idx = 0
    while True:
        output = proc.stderr.readline().decode('utf-8')
        if output == '' or proc.poll() is not None:
            break
        if output.find(pts_time_str) != -1:
            start = output.find(frame_index_str, output.find(']')) + len(frame_index_str) + 1
            end = output.find(' ', start + 4)
            f_idx = int(output[start:end])
        if output.find(side_data_str) != -1:
            data[f_idx][qp_str] = get_side_data_metric(output, qp_str)
    return data


def parse_block_data(frames):
    """
    Parse block data from frame side data
    :param frames: frames data
    :return: data (dict) key - frame index, value - list of block info
    """
    data = {}
    f_idx = 0
    for frame in frames:
        if frame[media_type_str] != 'video':
            continue
        side_data = None
        for sd in frame[side_data_list_str]:
            if sd[side_data_type_str] == 'Video encoding parameters':
                side_data = sd
                break
        if side_data is not None:
            data[f_idx] = side_data[block_data_list_str]
        f_idx += 1
    return data


def split_data(data):
    """
    Store the block data separately according to the frame index range
    :param data: block data per frame
    """
    block_per_frame = {}
    count = 0
    if not os.path.exists(block_folder_path):
        os.mkdir(block_folder_path)
    for key, value in data.items():
        block_per_frame[key] = value
        count += 1
        if count % 10 == 0:
            file_name = 'block_' + str(count // 10 - 1) + '.js'
            write_to_js('block_per_frame', block_per_frame, block_folder_path + file_name, 'w')
            block_per_frame = {}
    if len(block_per_frame) > 0:
        file_name = 'block_' + str(count // 10) + '.js'
        write_to_js('block_per_frame', block_per_frame, block_folder_path + file_name, 'w')


def get_block_data(file_path):
    """
    Get block data from ffprobe using subprocess and store in js file
    :param file_path: input video file path
    """
    if which('ffprobe') is None:
        raise Exception('No ffprobe found in path')
    cmd = '../FFmpeg/ffprobe -export_side_data +venc_params -show_frames -of json'
    args = shlex.split(cmd)
    args.append(file_path)
    output = subprocess.check_output(args, stderr=subprocess.DEVNULL)
    output = json.loads(output)[frames_str]
    data = parse_block_data(output)
    # output block data to js
    split_data(data)
