import argparse

from compute import generate_bitrate_qp_graph
from const import qp_str, bs_str, b_type_str, data_js_path, mv_str
from ffmpeg import get_basic_info, generate_vis_video, get_frame_data
from output import write_to_report_folder, write_to_js


def main():
    args = create_arg_parser()
    file_name = args.infile[args.infile.rfind('/') + 1:]
    report_exe(file_name, args.infile, args.outfile)
    vis_video_exe(args.infile, args.outfile)


def report_exe(file_name, file_path, folder_path):
    """
    Generate HTML report
    :param file_name: name of input video
    :param file_path: input video path
    :param folder_path: output folder path
    """
    basic_info = get_basic_info(file_path)
    bitrate_plot, qp_plot, combined_graph = generate_bitrate_qp_graph(file_path)
    write_to_report_folder(file_name, folder_path, basic_info, bitrate_plot, qp_plot, c_plot=combined_graph)


def vis_video_exe(file_path, folder_path):
    """
    Generate visualization videos
    :param file_path: input video path
    :param folder_path: output folder path
    """
    data = get_frame_data(file_path)
    write_to_js('frame_map', data, data_js_path, 'a')

    try:
        generate_vis_video(file_path, folder_path, qp_str)
        generate_vis_video(file_path, folder_path, mv_str)
        generate_vis_video(file_path, folder_path, bs_str)
        generate_vis_video(file_path, folder_path, b_type_str)
    except Exception as e:
        print(e)


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
