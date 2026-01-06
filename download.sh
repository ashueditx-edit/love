#!/bin/bash

# YouTube Downloader Script
# Makes it easier to use the YouTube downloader

echo "YouTube Video/Audio Downloader"
echo "==============================="

if [ $# -eq 0 ]; then
    echo "Usage: $0 [YOUTUBE_URL] [FORMAT]"
    echo ""
    echo "Formats:"
    echo "  -v, --video    Download MP4 video (default)"
    echo "  -a, --audio    Download MP3 audio"
    echo "  -b, --both     Download both MP4 video and MP3 audio"
    echo ""
    echo "Examples:"
    echo "  $0 https://www.youtube.com/watch?v=example"
    echo "  $0 https://www.youtube.com/watch?v=example -v"
    echo "  $0 https://www.youtube.com/watch?v=example -a"
    echo "  $0 https://www.youtube.com/watch?v=example -b"
    echo ""
    exit 1
fi

URL="$1"
FORMAT="${2:-"-v"}"

# Create downloads directory
mkdir -p downloads

case $FORMAT in
    -v|--video)
        echo "Downloading video in MP4 format..."
        python youtube_downloader.py "$URL" --video
        ;;
    -a|--audio)
        echo "Downloading audio in MP3 format..."
        python youtube_downloader.py "$URL" --audio
        ;;
    -b|--both)
        echo "Downloading both video (MP4) and audio (MP3)..."
        python youtube_downloader.py "$URL" --both
        ;;
    *)
        echo "Unknown format: $FORMAT"
        echo "Use -v, -a, or -b for video, audio, or both"
        exit 1
        ;;
esac

echo "Download completed!"