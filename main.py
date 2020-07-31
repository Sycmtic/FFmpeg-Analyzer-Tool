import argparse

from compute import generate_bitrate_qp_graph
from const import qp_str, bs_str, b_type_str, data_js_path, mv_str
from ffmpeg import get_stream_info, generate_vis_video, get_frame_data, get_block_data
from output import write_to_report_folder, write_to_js, create_report_folder
import multiprocessing as mp
import logging


def main():
    args = create_arg_parser()
    file_name = args.infile[args.infile.rfind('/') + 1:]
    create_report_folder(args.outfile)
    vis_video_exe(args.infile, args.outfile)
    report_exe(file_name, args.infile, args.outfile)


def vis_video_exe(file_path, folder_path):
    """
    Generate visualization videos
    :param file_path: input video path
    :param folder_path: output folder path
    """
    pool = mp.Pool(processes=mp.cpu_count())
    res1 = pool.starmap_async(get_frame_data, [(file_path, )])
    res2 = pool.starmap_async(get_block_data, [(file_path, )])
    res3 = pool.starmap_async(generate_vis_video, [(file_path, folder_path, qp_str), (file_path, folder_path, mv_str),
                                                   (file_path, folder_path, bs_str), (file_path, folder_path, b_type_str)])
    try:
        res1.get()
        res2.get()
        res3.get()
    except Exception as e:
        logging.error(e)
    pool.close()
    pool.join()


def report_exe(file_name, file_path, folder_path):
    """
    Generate HTML report
    :param file_name: name of input video
    :param file_path: input video path
    :param folder_path: output folder path
    """
    stream_info = get_stream_info(file_path)
    bitrate_plot, qp_plot, combined_graph = generate_bitrate_qp_graph(file_path)
    write_to_report_folder(file_name, folder_path, stream_info, bitrate_plot, qp_plot, c_plot=combined_graph)


def create_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '-input', help='input video file path', dest='infile', action='store', required=True)
    # TODO: add option for user to choose metrics when more graph added
    parser.add_argument('-s', '-show', help='show specific graph metrics', dest='show', action='store')
    parser.add_argument('-o', '-output', help="output report directory path", dest='outfile', action="store", required=True)
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()
