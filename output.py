import os
import jinja2

from const import file_name_str, report_file_path, report_css_path, audio_img_path, video_img_path, audio_img_url_str, \
    video_img_url_str
from shutil import copyfile

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)


def write_to_report_folder(file_name, folder_path, stream_info, bitrate_div, qp_div, c_plot):
    """
    generate report folder
    :param file_name: name of input video
    :param folder_path: output report folder path
    :param stream_info: stream info dict
    :param bitrate_div: bitrate graph div
    :param qp_div: qp graph div
    """
    if not os.path.exists(folder_path + '/report'):
        os.mkdir(folder_path + '/report')
        os.mkdir(folder_path + '/report/files')
    write_to_files(folder_path + '/report/files')
    write_to_html(file_name, folder_path, stream_info, bitrate_div, qp_div, c_plot)


def write_to_files(folder_path):
    """
    write the support files to the report folder
    :param folder_path: support file folder path
    """
    copyfile('./styles/report.css', folder_path + '/report.css')
    copyfile('./video.jpg', folder_path + '/video.jpg')
    copyfile('./audio-icon.jpg', folder_path + '/audio-icon.jpg')


def write_to_html(file_name, folder_path, stream_info, bitrate_div, qp_div, c_plot):
    """
    write the information to HTML report
    :param file_name: name of input video
    :param folder_path: output report folder path
    :param stream_info: video stream info dict
    :param bitrate_div: bitrate graph div
    :param qp_div: qp graph div
    """
    report = jinja_env.get_template('report.html')
    audio_img_url = folder_path + audio_img_path
    video_img_url = folder_path + video_img_path
    css_url = folder_path + report_css_path
    stream_info[audio_img_url_str] = audio_img_url
    stream_info[video_img_url_str] = video_img_url
    stream_info[file_name_str] = file_name
    html_string = report.render(css_url=css_url, stream_info=stream_info, bitrate_div=bitrate_div, qp_div=qp_div, c_plot=c_plot)
    f = open(folder_path + report_file_path, 'w')
    f.write(html_string)
    f.close()
