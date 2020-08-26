"""
Copyright 2020 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from const import size_str, dts_time_str, duration_time_str, x_str, y_str, ssim_all_str
from ffmpeg import get_packets_info, get_qp_data, get_ssim_data
from graph import generate_line_graph


def generate_bitrate_qp_graph(file_path):
    """
    Call ffprobe to get packets info and generate bitrate graph
    Call ffmpeg to get qp data and generate the qp graph
    :param file_path: input video file path
    :return: <div> bitrate graph, <div> qp graph, <div> combined graph
    """
    packets_info = get_packets_info(file_path)
    b_data = compute_bitrate(packets_info)
    qp_data = get_qp_data(file_path)
    bitrate_graph = generate_line_graph(b_data)
    qp_graph = generate_line_graph(qp_data)
    c_graph = generate_line_graph(b_data, qp_data)
    return bitrate_graph, qp_graph, c_graph


def generate_ssim_graph(main_file_path, ref_file_path):
    """
    Call ffmpeg to get ssim per frame and generate ssim graph
    :param main_file_path: main video file path
    :param ref_file_path: ref video file path
    :return: <div> ssim graph
    """
    ssim_data = get_ssim_data(main_file_path, ref_file_path)
    ssim_graph = generate_line_graph(compute_ssim(ssim_data))
    return ssim_graph


def compute_bitrate(packets):
    """
    Calculate the bitrate per frame
    :param packets: packet info from ffprobe
    :return: bitrate data
    """
    data = {x_str: [], y_str: []}
    for packet in packets:
        bitrate = float(packet[size_str]) / float(packet[duration_time_str])
        # TODO: replace with frame index
        dts = packet[dts_time_str]
        data[x_str].append(dts)
        data[y_str].append(bitrate)
    return data


def compute_ssim(frame_ssim):
    """
    Parse SSIM data to an appropriate format
    :param frame_ssim: SSIM per frame dict
    :return: data (dict)
    """
    data = {x_str: [], y_str: []}
    for f_idx, ssim in frame_ssim.items():
        data[x_str].append(f_idx)
        data[y_str].append(ssim[ssim_all_str])
    return data
