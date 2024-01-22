# Youtube Downloader

Youtube Downloader is a simple python script that allows you to download videos from youtube using the pytube library.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install pytube and ffmpeg.

```bash
pip install pytube
```

> NOTE: If you have trouble with youtube age restriction, go to the pytube folder and open the `__main__.py` and change the line 253 from `client='ANDROID_EMBED'` to `client='ANDROID'. You should have something like this:
>
> ```python
> def bypass_age_gate(self):
>        """Attempt to update the vid_info by bypassing the age gate."""
>        innertube = InnerTube(
>            client='ANDROID', # <--- Change this line
>            use_oauth=self.use_oauth,
>            allow_cache=self.allow_oauth_cache
>        )
>        innertube_response = innertube.player(self.video_id)
>
>        playability_status = innertube_response['playabilityStatus'].get('status', None)
>
>        # If we still can't access the video, raise an exception
>        # (tier 3 age restriction)
>        if playability_status == 'UNPLAYABLE':
>            raise exceptions.AgeRestrictedError(self.video_id)
>
>        self._vid_info = innertube_response
> ```

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
