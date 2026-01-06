#!/usr/bin/env python3
"""
YouTube Video Downloader
Downloads videos in MP4 format and extracts audio as MP3
"""

import os
import sys
from pytube import YouTube
from moviepy.editor import VideoFileClip
import argparse


def download_video(youtube_url, output_path="./downloads", quality="highest"):
    """
    Download YouTube video in MP4 format
    
    Args:
        youtube_url (str): URL of the YouTube video
        output_path (str): Path to save the downloaded video
        quality (str): Quality of the video ("highest", "lowest", or specific resolution)
    
    Returns:
        str: Path to the downloaded video file
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_path, exist_ok=True)
        
        # Create YouTube object
        yt = YouTube(youtube_url)
        
        print(f"Title: {yt.title}")
        print(f"Author: {yt.author}")
        print(f"Duration: {yt.length} seconds")
        
        # Get video stream
        if quality == "highest":
            video_stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        elif quality == "lowest":
            video_stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').asc().first()
        else:
            # Specific resolution
            video_stream = yt.streams.filter(progressive=True, file_extension='mp4', resolution=quality).first()
        
        if not video_stream:
            print(f"No video stream found for quality: {quality}")
            # Get all available streams for user to choose
            available_streams = yt.streams.filter(progressive=True, file_extension='mp4')
            if available_streams:
                print("Available qualities:")
                for stream in available_streams:
                    print(f"  - {stream.resolution} ({stream.fps}fps)")
            return None
        
        # Download the video
        print(f"Downloading video in {video_stream.resolution}...")
        video_filename = video_stream.download(output_path=output_path)
        print(f"Video downloaded successfully: {video_filename}")
        
        return video_filename
        
    except Exception as e:
        print(f"Error downloading video: {str(e)}")
        return None


def extract_audio(video_path, output_path=None):
    """
    Extract audio from video file and save as MP3
    
    Args:
        video_path (str): Path to the video file
        output_path (str): Path to save the audio file (optional)
    
    Returns:
        str: Path to the extracted audio file
    """
    try:
        if not output_path:
            # Create output path in same directory as video
            video_dir = os.path.dirname(video_path)
            video_name = os.path.splitext(os.path.basename(video_path))[0]
            output_path = os.path.join(video_dir, f"{video_name}.mp3")
        
        print(f"Extracting audio from {video_path}...")
        
        # Load video and extract audio
        video = VideoFileClip(video_path)
        audio = video.audio
        
        # Write audio to file
        audio.write_audiofile(output_path)
        
        # Close the clips to free up resources
        audio.close()
        video.close()
        
        print(f"Audio extracted successfully: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"Error extracting audio: {str(e)}")
        return None


def download_audio_only(youtube_url, output_path="./downloads"):
    """
    Download only the audio from YouTube video as MP3
    
    Args:
        youtube_url (str): URL of the YouTube video
        output_path (str): Path to save the audio file
    
    Returns:
        str: Path to the downloaded audio file
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_path, exist_ok=True)
        
        # Create YouTube object
        yt = YouTube(youtube_url)
        
        print(f"Title: {yt.title}")
        print(f"Author: {yt.author}")
        
        # Get the audio stream (usually in mp4 format, will be converted)
        audio_stream = yt.streams.filter(only_audio=True).first()
        
        if not audio_stream:
            print("No audio stream found!")
            return None
        
        # Download the audio
        print("Downloading audio...")
        audio_filename = audio_stream.download(output_path=output_path)
        
        # Convert to MP3 if needed
        base, ext = os.path.splitext(audio_filename)
        mp3_filename = base + '.mp3'
        
        # Use moviepy to convert to MP3
        video = VideoFileClip(audio_filename)
        audio = video.audio
        audio.write_audiofile(mp3_filename)
        
        # Close resources
        audio.close()
        video.close()
        
        # Remove the original downloaded file
        os.remove(audio_filename)
        
        print(f"Audio downloaded successfully: {mp3_filename}")
        return mp3_filename
        
    except Exception as e:
        print(f"Error downloading audio: {str(e)}")
        return None


def main():
    parser = argparse.ArgumentParser(description="YouTube Video/Audio Downloader")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("--video", action="store_true", help="Download video in MP4 format")
    parser.add_argument("--audio", action="store_true", help="Download audio in MP3 format")
    parser.add_argument("--both", action="store_true", help="Download both video and audio")
    parser.add_argument("--quality", default="highest", help="Video quality (highest, lowest, or specific resolution like 720p)")
    parser.add_argument("--output", default="./downloads", help="Output directory")
    
    args = parser.parse_args()
    
    # Validate URL
    if not args.url or not args.url.startswith("http"):
        print("Please provide a valid YouTube URL")
        return
    
    # Create output directory
    os.makedirs(args.output, exist_ok=True)
    
    # Determine what to download
    if args.video:
        # Download video only
        video_file = download_video(args.url, args.output, args.quality)
        if video_file and args.audio:
            # Extract audio from the downloaded video
            extract_audio(video_file, os.path.join(args.output, os.path.splitext(os.path.basename(video_file))[0] + ".mp3"))
    elif args.audio:
        # Download audio only
        download_audio_only(args.url, args.output)
    elif args.both:
        # Download both video and audio
        video_file = download_video(args.url, args.output, args.quality)
        if video_file:
            extract_audio(video_file)
    else:
        # Default: ask user
        print("Please specify what to download:")
        print("  --video: Download video in MP4 format")
        print("  --audio: Download audio in MP3 format")
        print("  --both: Download both video and audio")


if __name__ == "__main__":
    main()