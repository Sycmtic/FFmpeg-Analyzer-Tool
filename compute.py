from const import packets_str, size_str, dts_time_str, duration_time_str, x_str, y_str, codec_type_str, pts_time_str
from ffmpeg import get_packets_info, get_qp_data
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
