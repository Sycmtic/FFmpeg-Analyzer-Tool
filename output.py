import os
import jinja2

from const import file_name_str, report_file_path, report_css_path, img_url_str

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
    css_url = os.getcwd() + report_css_path
    basic_info[img_url_str] = video_img_url
    basic_info[file_name_str] = file_name
    html_string = report.render(css_url=css_url, video=basic_info, bitrate_div=bitrate_div, qp_div=qp_div, c_plot=c_plot)
    f = open(folder_path + report_file_path, 'w')
    f.write(html_string)
    f.close()
