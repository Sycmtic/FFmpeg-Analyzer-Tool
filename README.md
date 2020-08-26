# FFmpeg-Analyzer-Tool
### How to install
1. clone the repository
```
git clone https://github.com/Sycmtic/FFmpeg-Analyzer-Tool.git
```

2. install dependency
```
pip install -r requirements.txt
```

### Example command:
```
python main.py -i <input_video> -o <output_report_dir>
```
#### Note:
Some of the features haven't been merged to FFmpeg yet. In order to use this tool, please clone a local version of FFmpeg in this Github branch (https://github.com/Sycmtic/FFmpeg/tree/local_env)