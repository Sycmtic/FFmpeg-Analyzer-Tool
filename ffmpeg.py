import shlex
import subprocess
import json

from const import *
from output import write_to_js


def parse_frame_timestamp(packets):
    """
    Extract frame timestamp from packet data
    :param packets: packet data
    :return: frame timestamp
    """
    data = []
    pre_pts_time = 0
    for packet in packets:
        if packet[codec_type_str] == 'video' and float(packet[pts_time_str]) > pre_pts_time:
            data.append(packet[pts_time_str])
            pre_pts_time = float(packet[pts_time_str])
    return data


# query data
def get_packets_info(file_path):
    """
    Get packet data using ffprobe to calculate the bitrate
    :param file_path input video file path
    :return information of packet
    """
    cmd = 'ffprobe -show_packets -of json'
    args = shlex.split(cmd)
    args.append(file_path)
    output = subprocess.check_output(args, stderr=subprocess.DEVNULL)
    output = json.loads(output)[packets_str]
    # output frame timestamps to js
    write_to_js('frame_ts', parse_frame_timestamp(output), data_js_path, 'w')
    return output


def get_stream_info(file_path):
    """
    Get video stream information using ffprobe
    :param file_path input video file path
    :return information of stream
    """
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
    if op == mv_str:
        cmd = '../FFmpeg/ffmpeg -flags2 +export_mvs -i ' + file_path + ' -vf codecview=mv=pf+bf+bb -y'
    else:
        # TODO: change the path to global ffmpeg url
        cmd = '../FFmpeg/ffmpeg -export_side_data +venc_params -i ' + file_path + ' -vf codecview=' + op + '=true -y'
    args = shlex.split(cmd)
    args.append(folder_path + '/report/' + op + '_vis.mp4')
    proc = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    proc.communicate()
    print(op + ' visualization video generated')
    if proc.returncode != 0:
        raise Exception('No ffmpeg command found, please check the version of your ffmpeg')


def get_qp_data(file_path):
    """
    Get basic qp data from ffmpeg using subprocess
    :param file_path input video file path
    :return directory key - pts, value - basic qp
    """
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
    end = line.find(' ', start)
    return line[start:end]


def get_frame_data(file_path):
    """
    Get side data from ffmpeg using subprocess
    :param file_path input video file path
    :return directory key - frame index, value: frame metrics
    """
    cmd = 'ffmpeg -export_side_data +venc_params -i ' + file_path + ' -vf showinfo -f null -'
    args = shlex.split(cmd)
    proc = subprocess.Popen(args, stderr=subprocess.PIPE)
    data = {}
    f_idx = 0
    while True:
        output = proc.stderr.readline().decode('utf-8')
        if output == '' or proc.poll() is not None:
            break
        if output.find(pts_time_str) != -1:
            start = output.find(frame_index_str, output.find(']')) + len(frame_index_str) + 1
            end = output.find(' ', start + 4)
            f_idx = int(output[start:end])
            if f_idx not in data:
                data[f_idx] = {}

            data[f_idx][pts_time_str] = get_side_data_metric(output, pts_time_str)
            data[f_idx][fmt_str] = get_side_data_metric(output, fmt_str)
            data[f_idx][type_str] = get_side_data_metric(output, type_str)
            data[f_idx][is_key_str] = get_side_data_metric(output, is_key_str)
            data[f_idx][checksum_str] = get_side_data_metric(output, checksum_str)
        if output.find(side_data_str) != -1:
            data[f_idx][qp_str] = get_side_data_metric(output, qp_str)
    return data
