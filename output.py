import os
import jinja2
import json

from const import *
from shutil import copy, copyfile, rmtree

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)


def change_js_file_setting(frame_per_file):
    """
    change number of frame stores in a file
    :param frame_per_file: (number)
    :return:
    """
    with open('./js/report.js', 'r') as f:
        lines = f.readlines()
    with open('./js/report.js', 'w') as f:
        for line in lines:
            if line.find('let numFramePerFile') != -1:
                line = 'let numFramePerFile = {};\n'.format(frame_per_file)
            f.write(line)


def create_report_folder(folder_path):
    """
    create report folder struct
    :param folder_path: output report folder path
    """
    if not os.path.exists(folder_path + '/report'):
        os.mkdir(folder_path + '/report')
        os.mkdir(folder_path + '/report/files')
        os.mkdir(folder_path + '/report/files/blocks')


def write_to_report_folder(file_name, folder_path, stream_info, bitrate_div, qp_div, c_plot, ssim_div):
    """
    write to report folder
    :param file_name: name of input video
    :param folder_path: output report folder path
    :param stream_info: stream info dict
    :param bitrate_div: bitrate graph div
    :param qp_div: qp graph div
    """
    write_to_files(folder_path + '/report/files')
    write_to_html(file_name, folder_path, stream_info, bitrate_div, qp_div, c_plot, ssim_div)


def write_to_files(folder_path):
    """
    write the support files to the report folder
    :param folder_path: support file folder path
    """
    copyfile('./styles/report.css', folder_path + '/report.css')
    copyfile('./video.jpg', folder_path + '/video.jpg')
    copyfile('./audio-icon.jpg', folder_path + '/audio-icon.jpg')
    copyfile('./overlay.png', folder_path + '/overlay.png')
    copyfile('./js/report.js', folder_path + '/report.js')
    copyfile('./js/imagemapster.js', folder_path + '/imagemapster.js')
    copyfile('./js/data.js', folder_path + '/data.js')
    os.remove('./js/data.js')
    for file in os.listdir('./js/blocks'):
        file_path = os.path.join('./js/blocks', file)
        if os.path.isfile(file_path):
            copy(file_path, folder_path + '/blocks')
    rmtree('./js/blocks')


def write_to_html(file_name, folder_path, stream_info, bitrate_div, qp_div, c_plot, ssim_div):
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
    overlay_img_url = folder_path + overlay_img_path
    css_url = folder_path + report_css_path
    js_url = folder_path + report_js_path
    mapster_url = folder_path + report_mapster_path
    data_url = folder_path + report_data_js_path
    stream_info[audio_img_url_str] = audio_img_url
    stream_info[video_img_url_str] = video_img_url
    stream_info[overlay_img_url_str] = overlay_img_url
    stream_info[file_name_str] = file_name
    html_string = report.render(css_url=css_url, js_url=js_url, mapster_url=mapster_url, data_js_url=data_url,
                                stream_info=stream_info, bitrate_div=bitrate_div, qp_div=qp_div, c_plot=c_plot, ssim_div=ssim_div)
    f = open(folder_path + report_file_path, 'w')
    f.write(html_string)
    f.close()


def write_to_js(name, data, file_path, mode):
    """
    write data to javascript file
    :param name: var name in javascript
    :param data: input data
    :param file_path: ouput json file path
    :param mode: 'w' overwrite the file, 'a' append to the end of file
    """
    with open(file_path, mode, encoding='utf-8') as f:
        f.write('var ' + name + ' = %s;' % json.dumps(data))
