# Youtube Downloader

Youtube Downloader is a simple python script that allows you to download videos from youtube using the pytube library.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install pytube and ffmpeg.

```bash
pip install pytube
```

```bash
pip install ffmpeg
```

You can also install ffmpeg from [here](https://ffmpeg.org/download.html).

## Usage

In order to use this script, you need to place the script inside the folder where you want to download the video and run it.

```python
python youtube_downloader.py
```

Once you have run the script, you will be asked to enter thow many you want to download and the URLs of the videos you want to download (one per line).

After that, the script will download the maximum resolution available for each video and save it in the same folder where the script is located. The video downloaded do not include audio: so, the script will download the audio as a separate file.

Once every file has been downloaded, ffmpeg will merge the video and the audio into a single file and delete the two files that were used to create it.

> NOTE: Keep in mind that every single video will be downloaded twice (one for the video, and one for the audio) so make sure you have enough space on your disk.
>

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Thanks to [pytube](https://github.com/pytube/pytube) and [ffmpeg](https://github.com/kkroening/ffmpeg-python) for their libraries.
