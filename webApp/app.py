from flask import Flask, render_template, request, jsonify, send_file
import os
import sys
import subprocess
from pathlib import Path
import glob

app = Flask(__name__)

# Add the project root to Python path so we can import download_yt.py
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/youtube/extract", methods=["POST"])
def extract_youtube_info():
    """Extract YouTube video information for preview"""
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        # Import the function from download_yt.py
        from download_yt import check_ffmpeg
        
        # Check if yt-dlp is available
        try:
            import yt_dlp
        except ImportError:
            return jsonify({'error': 'yt-dlp is not installed. Please install it with: pip install yt-dlp'}), 500
        
        # Extract video info without downloading
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Get the best thumbnail
            thumbnail = None
            if 'thumbnails' in info and info['thumbnails']:
                # Get the highest quality thumbnail
                thumbnail = max(info['thumbnails'], key=lambda x: x.get('height', 0) or 0)['url']
            
            video_info = {
                'title': info.get('title', 'Unknown'),
                'duration': info.get('duration', 0),
                'uploader': info.get('uploader', 'Unknown'),
                'view_count': info.get('view_count', 0),
                'thumbnail': thumbnail,
                'description': info.get('description', '')[:200] + '...' if info.get('description') else '',
                'formats': len(info.get('formats', [])),
                'ffmpeg_available': check_ffmpeg()
            }
            
            return jsonify(video_info)
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/api/youtube/download", methods=["POST"])
def download_youtube_video():
    """Download YouTube video with optional time range"""
    try:
        data = request.get_json()
        url = data.get('url')
        start_time = data.get('start_time') or None
        end_time = data.get('end_time') or None
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        # Import the download function and yt-dlp
        from download_yt import download_youtube_video, check_ffmpeg
        import yt_dlp
        
        # Get video title first to construct filename
        ydl_opts = {'quiet': True, 'no_warnings': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_title = info.get('title', 'video')
        
        # Clean filename
        safe_title = "".join(c for c in video_title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        
        # Download the video
        download_youtube_video(url, "downloads", start_time, end_time)
        
        # Find the downloaded file (most recent file in downloads folder)
        download_folder = Path("downloads")
        files = list(download_folder.glob("*.mp4"))
        if not files:
            files = list(download_folder.glob("*.mkv"))
        if not files:
            files = list(download_folder.glob("*.webm"))
        
        if files:
            latest_file = max(files, key=lambda p: p.stat().st_mtime)
            return jsonify({
                'message': 'Download completed successfully',
                'filename': latest_file.name,
                'filepath': str(latest_file)
            })
        else:
            return jsonify({'error': 'Download completed but file not found'}), 500
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/api/youtube/get-file/<path:filename>")
def get_downloaded_file(filename):
    """Serve the downloaded video file"""
    try:
        file_path = Path("downloads") / filename
        if file_path.exists():
            return send_file(
                file_path,
                as_attachment=True,
                download_name=filename
            )
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
