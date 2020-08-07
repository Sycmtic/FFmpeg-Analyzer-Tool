import argparse

from compute import generate_bitrate_qp_graph, generate_ssim_graph
from const import qp_str, bs_str, b_type_str, mv_str
from ffmpeg import get_stream_info, generate_vis_video, get_frame_data, get_block_data, get_ssim_psnr_data
from output import write_to_report_folder, create_report_folder, change_js_file_setting
import multiprocessing as mp
import logging


def main():
    args = create_arg_parser()
    file_name = args.infile[args.infile.rfind('/') + 1:]
    change_js_file_setting(args.frame_per_file)
    create_report_folder(args.outfile)
    vis_video_exe(args.infile, args.outfile, args.frame_per_file)
    report_exe(file_name, args.infile, args.outfile, args.ref)


def vis_video_exe(file_path, folder_path, frame_per_file):
    """
    Generate visualization videos
    :param file_path: input video path
    :param folder_path: output folder path
    :param frame_per_file: number of frame stores in a file
    """
    pool = mp.Pool(processes=mp.cpu_count())
    res1 = pool.starmap_async(get_frame_data, [(file_path, )])
    res2 = pool.starmap_async(get_block_data, [(file_path, frame_per_file)])
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


def report_exe(file_name, file_path, folder_path, ref_file_path=None):
    """
    Generate HTML report
    :param file_name: name of input video
    :param file_path: input video path
    :param ref_file_path: reference video path, None if doesn't exist
    :param folder_path: output folder path
    """
    stream_info = get_stream_info(file_path)
    bitrate_plot, qp_plot, combined_graph = generate_bitrate_qp_graph(file_path)
    ssim_graph = None
    if ref_file_path is not None:
        ssim_graph = generate_ssim_graph(file_path, ref_file_path)
    write_to_report_folder(file_name, folder_path, stream_info, bitrate_plot, qp_plot, c_plot=combined_graph, ssim_div=ssim_graph)


def frame_per_file_type(x):
    x = int(x)
    if x < 5 or x > 50:
        raise argparse.ArgumentTypeError("frame per file should be in range [5, 50]")
    return x


def create_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '-input', help='input video file path', dest='infile', action='store', required=True)
    # TODO: add option for user to choose metrics when more graph added
    parser.add_argument('-s', '-show', help='show specific graph metrics', dest='show', action='store')
    parser.add_argument('-o', '-output', help="output report directory path", dest='outfile', action="store", required=True)
    parser.add_argument('-f', '-frameperfile', help="number of frame block data store in a file", dest='frame_per_file', type=frame_per_file_type, action="store", default=10)
    parser.add_argument('-r', '-ref', help="enable ssim/psnr with ref video", dest='ref', action="store")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()
