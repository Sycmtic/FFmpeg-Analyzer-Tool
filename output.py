import os
import jinja2
import json

from const import file_name_str, report_file_path, report_css_path, img_url_str, report_js_path, data_js_path, \
    pts_time_str, codec_type_str

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)


# output to file
def write_to_report_folder(file_name, folder_path, basic_info, bitrate_div, qp_div, c_plot):
    """
    generate report folder
    :param file_name: name of input video
    :param folder_path: output report folder path
    :param basic_info: basic info dict
    :param bitrate_div: bitrate graph div
    :param qp_div: qp graph div
    """
    if not os.path.exists(folder_path + "/report"):
        os.mkdir(folder_path + "/report")
    write_to_html(file_name, folder_path, basic_info, bitrate_div, qp_div, c_plot)


def write_to_html(file_name, folder_path, basic_info, bitrate_div, qp_div, c_plot):
    """
    write the information to HTML report
    :param file_name: name of input video
    :param folder_path: output report folder path
    :param basic_info: video basic info dict
    :param bitrate_div: bitrate graph div
    :param qp_div: qp graph div
    """
    report = jinja_env.get_template('report.html')
    video_img_url = os.getcwd() + '/video.jpg'
    basic_info[img_url_str] = video_img_url
    basic_info[file_name_str] = file_name
    html_string = report.render(css_url=report_css_path, js_url=report_js_path, data_js_url=data_js_path,
                                video=basic_info, bitrate_div=bitrate_div, qp_div=qp_div, c_plot=c_plot)
    f = open(folder_path + report_file_path, 'w')
    f.write(html_string)
    f.close()


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


def write_to_js(data, file_path):
    """
    write data to javascript file
    :param data: dict
    :param file_path: ouput json file path
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('var frame_ts = %s;' % json.dumps(parse_frame_timestamp(data)))
