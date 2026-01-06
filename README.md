# YouTube Video Downloader

A Python script to download YouTube videos in MP4 format and extract audio as MP3.

## Features

- Download YouTube videos in MP4 format
- Extract audio from videos as MP3 files
- Download audio only (as MP3)
- Choose video quality (highest, lowest, or specific resolution)
- Save files to a specified directory

## Requirements

- Python 3.x
- pytube
- moviepy

## Installation

The required packages are already installed in this environment:
```bash
pip install pytube moviepy
```

## Usage

### Basic Usage

```bash
python youtube_downloader.py [URL]
```

### Download Video Only (MP4)

```bash
python youtube_downloader.py [URL] --video
```

### Download Audio Only (MP3)

```bash
python youtube_downloader.py [URL] --audio
```

### Download Both Video and Audio

```bash
python youtube_downloader.py [URL] --both
```

### Specify Video Quality

```bash
# Highest quality (default)
python youtube_downloader.py [URL] --video --quality highest

# Lowest quality
python youtube_downloader.py [URL] --video --quality lowest

# Specific resolution
python youtube_downloader.py [URL] --video --quality 720p
```

### Specify Output Directory

```bash
python youtube_downloader.py [URL] --video --output ./my_videos
```

## Examples

```bash
# Download video in highest quality
python youtube_downloader.py https://www.youtube.com/watch?v=example --video

# Download audio only as MP3
python youtube_downloader.py https://www.youtube.com/watch?v=example --audio

# Download both video and audio
python youtube_downloader.py https://www.youtube.com/watch?v=example --both

# Download 720p video to custom directory
python youtube_downloader.py https://www.youtube.com/watch?v=example --video --quality 720p --output ./videos
```

## Notes

- Downloads are saved to the `./downloads` directory by default
- When downloading both video and audio, the audio file will be extracted from the video file
- The script shows available qualities if the requested quality is not available
- Always respect copyright laws and YouTube's Terms of Service when using this tool