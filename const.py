import os

# ffmpeg command
qp_str = 'qp'
mv_str = 'mv'
bs_str = 'bs'
b_type_str = 'mb_type'
video_stream_str = 'video_stream'
audio_stream_str = 'audio_stream'

# tool attributes
working_dict_path = os.getcwd()
data_str = 'data'
x_str = 'x'
y_str = 'y'
video_img_url_str = 'video_img_url'
audio_img_url_str = 'audio_img_url'
file_name_str = 'file_name'
report_file_path = '/report/report.html'
report_css_path = working_dict_path + '/styles/report.css'
report_js_path = working_dict_path + '/js/report.js'
data_js_path = working_dict_path + '/js/data.js'
combined_graph_opacity = 0.7

# ffmpeg attributes
packets_str = 'packets'
pts_time_str = 'pts_time'
dts_time_str = 'dts_time'
duration_time_str = 'duration_time'
size_str = 'size'
streams_str = 'streams'
side_data_str = 'side data'
codec_type_str = 'codec_type'
frame_index_str = 'n'
fmt_str = 'fmt'
type_str = 'type'
is_key_str = 'iskey'
checksum_str = 'checksum'
plane_checksum_str = 'plane_checksum'
mean_str = 'mean'
stdev_str = 'stdev'
