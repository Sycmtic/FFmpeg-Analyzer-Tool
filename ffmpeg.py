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
    for packet in packets:
        if packet[codec_type_str] == 'video':
            data.append(packet[pts_time_str])
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


def get_basic_info(file_path):
    """
    Get basic video information using ffprobe
    :param file_path input video file path
    :return information of stream
    """
    cmd = 'ffprobe -show_streams -of json'
    args = shlex.split(cmd)
    args.append(file_path)
    output = subprocess.check_output(args, stderr=subprocess.DEVNULL)
    output = json.loads(output)
    return output[streams_str][0]


def generate_vis_video(file_path, folder_path, op):
    """
    Generate visualization video from ffmpeg codecview filter using subprocess
    :param file_path input video file path
    :param folder_path output folder path
    :param op option of codecview filter (qp, bs, b_type)
    """
    # TODO: change the path to global ffmpeg url
    cmd = '../FFmpeg/ffmpeg -export_side_data +venc_params -i ' + file_path + ' -vf codecview=' + op + '=true -y'
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
            end = start + 4
            f_idx = int(output[start:end])
            if f_idx not in data:
                data[f_idx] = {}

            start = output.find(pts_time_str) + len(pts_time_str) + 1
            end = output.find(' ', output.find(pts_time_str))
            data[f_idx][pts_time_str] = (output[start:end])

            start = output.find(fmt_str) + len(fmt_str) + 1
            end = output.find(' ', start)
            data[f_idx][fmt_str] = output[start:end]

            start = output.find(checksum_str) + len(checksum_str) + 1
            end = output.find(' ', start)
            data[f_idx][checksum_str] = output[start:end]

            start = output.find(plane_checksum_str) + len(plane_checksum_str) + 2
            end = output.find(']', start)
            data[f_idx][plane_checksum_str] = []
            for a in output[start:end].split():
                data[f_idx][plane_checksum_str].append(a)

            start = output.find(mean_str) + len(mean_str) + 2
            end = output.find(']', start)
            data[f_idx][mean_str] = []
            for a in output[start:end].split(' '):
                if a == '\x08':
                    continue
                data[f_idx][mean_str].append(a)

            start = output.find(stdev_str) + len(stdev_str) + 2
            end = output.find(']', start)
            data[f_idx][stdev_str] = []
            for a in output[start:end].split():
                if a == '\x08':
                    continue
                data[f_idx][stdev_str].append(a)
        if output.find(side_data_str) != -1:
            start = output.find(qp_str) + len(qp_str) + 1
            end = output.find(';', start)
            data[f_idx][qp_str] = (output[start:end])
    return data
