from flask import Flask, render_template, request, jsonify, send_file
import os
import sys
import subprocess
from pathlib import Path
import glob
import threading 
import time

app = Flask(__name__)

# Add the project root to Python path so we can import download_yt.py
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(PROJECT_ROOT)

# Use absolute path for downloads folder
DOWNLOADS_FOLDER = os.path.join(PROJECT_ROOT, 'downloads')

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
        
        # Download the video using absolute path
        download_youtube_video(url, DOWNLOADS_FOLDER, start_time, end_time)
        
        # Find the downloaded file (most recent file in downloads folder)
        download_folder = Path(DOWNLOADS_FOLDER)
        files = list(download_folder.glob("*.mp4"))
        if not files:
            files = list(download_folder.glob("*.mkv"))
        if not files:
            files = list(download_folder.glob("*.webm"))
        
        if files:
            latest_file = max(files, key=lambda p: p.stat().st_mtime)
            
            # Create a safe filename for serving
            original_name = latest_file.name
            safe_name = safe_title[:100] + latest_file.suffix  # Use safe_title we created earlier
            safe_path = download_folder / safe_name
            
            # Rename file to safe name if different
            if original_name != safe_name:
                latest_file.rename(safe_path)
            else:
                safe_path = latest_file
            
            return jsonify({
                'message': 'Download completed successfully',
                'filename': safe_name,
                'original_filename': original_name,
                'filepath': str(safe_path)
            })
        else:
            return jsonify({'error': 'Download completed but file not found'}), 500
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/api/youtube/get-file/<path:filename>")
def get_downloaded_file(filename):
    """Serve the downloaded video file"""
    try:
        # Decode URL-encoded filename and construct path
        from urllib.parse import unquote
        decoded_filename = unquote(filename)
        file_path = Path(DOWNLOADS_FOLDER) / decoded_filename
        
        if file_path.exists():
            return send_file(
                file_path,
                as_attachment=True,
                download_name=decoded_filename
            )
        else:
            return jsonify({'error': f'File not found: {decoded_filename}'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route("/api/youtube/delete-file/<path:filename>", methods=["DELETE"])
def delete_downloaded_file(filename):
    """Delete a file from the downloads folder after user has downloaded it"""
    try:
        from urllib.parse import unquote
        decoded_filename = unquote(filename)
        file_path = Path(DOWNLOADS_FOLDER) / decoded_filename
        
        if file_path.exists():
            # Try to delete with retries in case file is still being released
            for attempt in range(5):
                try:
                    file_path.unlink()
                    print(f"Deleted file: {decoded_filename}")
                    return jsonify({'message': f'File deleted: {decoded_filename}'})
                except PermissionError:
                    time.sleep(0.5)
            
            return jsonify({'error': 'File is still in use, please try again'}), 500
        else:
            return jsonify({'message': 'File already deleted or not found'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
