#!/usr/bin/env python3
"""
YouTube Video Downloader with optional time range selection
Requires: yt-dlp and ffmpeg installed on your system
Install: pip install yt-dlp
"""

import argparse
import os
import sys
from pathlib import Path

try:
    import yt_dlp
except ImportError:
    print("Error: yt-dlp is not installed.")
    print("Install it using: pip install yt-dlp")
    sys.exit(1)


def convert_time_to_seconds(time_str):
    """Convert time string (HH:MM:SS or MM:SS or SS) to seconds."""
    parts = time_str.split(':')
    parts = [int(p) for p in parts]
    
    if len(parts) == 3:  # HH:MM:SS
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    elif len(parts) == 2:  # MM:SS
        return parts[0] * 60 + parts[1]
    elif len(parts) == 1:  # SS
        return parts[0]
    else:
        raise ValueError("Invalid time format. Use HH:MM:SS, MM:SS, or SS")


def check_ffmpeg():
    """Check if FFmpeg is available."""
    import subprocess
    import shutil
    
    # First try using shutil.which (checks PATH)
    if shutil.which('ffmpeg'):
        return True
    
    # Try running ffmpeg directly
    try:
        result = subprocess.run(
            ['ffmpeg', '-version'], 
            capture_output=True, 
            check=True,
            shell=True  # Use shell on Windows to help find ffmpeg
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    
    # Check common Windows installation paths
    common_paths = [
        r'C:\ffmpeg\bin\ffmpeg.exe',
        r'C:\Program Files\ffmpeg\bin\ffmpeg.exe',
        r'C:\Program Files (x86)\ffmpeg\bin\ffmpeg.exe',
    ]
    
    for path in common_paths:
        if os.path.exists(path):
            return True
    
    return False


def download_youtube_video(url, output_folder="downloads", start_time=None, end_time=None):
    """
    Download a YouTube video with optional time range.
    
    Args:
        url: YouTube video URL
        output_folder: Folder to save the video
        start_time: Start time (format: HH:MM:SS, MM:SS, or SS)
        end_time: End time (format: HH:MM:SS, MM:SS, or SS)
    """
    # Create output folder if it doesn't exist
    output_path = Path(output_folder)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Check if FFmpeg is available
    has_ffmpeg = check_ffmpeg()
    
    # Warn if time range is requested but FFmpeg is not available
    if (start_time or end_time) and not has_ffmpeg:
        print("⚠ WARNING: FFmpeg is not installed. Time range cutting will not work.")
        print("The complete video will be downloaded instead.")
        print("To enable time cutting, install FFmpeg from: https://ffmpeg.org/download.html\n")
        start_time = None
        end_time = None
    
    # Base yt-dlp options
    if has_ffmpeg:
        # Use best quality with separate video and audio (requires FFmpeg to merge)
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': str(output_path / '%(title)s.%(ext)s'),
            'quiet': False,
            'no_warnings': False,
            'socket_timeout': 30,
            'retries': 5,
            'fragment_retries': 5,
        }
    else:
        # Use pre-merged format (doesn't require FFmpeg)
        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'outtmpl': str(output_path / '%(title)s.%(ext)s'),
            'quiet': False,
            'no_warnings': False,
        }
    
    # Add time range options if provided (requires FFmpeg)
    if start_time or end_time:
        postprocessor_args = []
        
        if start_time:
            start_seconds = convert_time_to_seconds(start_time)
            postprocessor_args.extend(['-ss', str(start_seconds)])
        
        if end_time:
            end_seconds = convert_time_to_seconds(end_time)
            if start_time:
                # Calculate duration from start to end
                duration = end_seconds - start_seconds
                postprocessor_args.extend(['-t', str(duration)])
            else:
                # If only end time is provided, cut from beginning
                postprocessor_args.extend(['-to', str(end_seconds)])
        
        ydl_opts['postprocessor_args'] = postprocessor_args
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }]
        
        print(f"Downloading video segment: ", end="")
        if start_time:
            print(f"from {start_time} ", end="")
        if end_time:
            print(f"to {end_time}", end="")
        print()
    else:
        print("Downloading complete video...")
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract video info first
            info = ydl.extract_info(url, download=False)
            video_title = info.get('title', 'Unknown')
            print(f"\nVideo: {video_title}")
            
            # Download the video
            ydl.download([url])
            
        print(f"\n✓ Download completed successfully!")
        print(f"Saved to: {output_path.absolute()}")
        
        if not has_ffmpeg:
            print("\n💡 Tip: Install FFmpeg to enable:")
            print("   - Time range cutting (--start/--end options)")
            print("   - Better quality video downloads")
        
    except Exception as e:
        print(f"\n✗ Error downloading video: {str(e)}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Download YouTube videos with optional time range',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Download complete video
  python script.py https://youtube.com/watch?v=VIDEO_ID
  
  # Download from 1:30 to 3:45
  python script.py https://youtube.com/watch?v=VIDEO_ID --start 1:30 --end 3:45
  
  # Download first 60 seconds
  python script.py https://youtube.com/watch?v=VIDEO_ID --end 1:00
  
  # Download from 2:15 to end
  python script.py https://youtube.com/watch?v=VIDEO_ID --start 2:15
        """
    )
    
    parser.add_argument('url', help='YouTube video URL')
    parser.add_argument('-s', '--start', help='Start time (HH:MM:SS, MM:SS, or SS)')
    parser.add_argument('-e', '--end', help='End time (HH:MM:SS, MM:SS, or SS)')
    parser.add_argument('-o', '--output', default='downloads', 
                        help='Output folder (default: downloads)')
    
    args = parser.parse_args()
    
    # Validate that if end time is provided with start time, end > start
    if args.start and args.end:
        start_sec = convert_time_to_seconds(args.start)
        end_sec = convert_time_to_seconds(args.end)
        if end_sec <= start_sec:
            print("Error: End time must be greater than start time", file=sys.stderr)
            sys.exit(1)
    
    download_youtube_video(args.url, args.output, args.start, args.end)


if __name__ == "__main__":
    main()