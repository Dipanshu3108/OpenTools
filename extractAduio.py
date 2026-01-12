import moviepy as mp
import os

class VideoAudioExtractor:
    def __init__(self, video_path):
        self.video_path = video_path

    def extract_audio(self, output_path=None):
        """
        Extracts audio from the video file and saves it as an audio file.
        
        :param output_path: Optional output file path. 
                            If not provided, saves as same name with .mp3 extension.
        :return: Path to saved audio file.
        """
        # If no output file is given, create one
        if output_path is None:
            base, _ = os.path.splitext(self.video_path)
            output_path = base + ".mp3"

        # Load video
        video = mp.VideoFileClip(self.video_path)

        # Extract and write audio
        if video.audio is None:
            raise ValueError("This video does not contain an audio track.")

        video.audio.write_audiofile(output_path)

        return output_path


# Example Usage:
extractor = VideoAudioExtractor("path to input video file")
audio_file = extractor.extract_audio()
print("Audio saved to:", audio_file)
