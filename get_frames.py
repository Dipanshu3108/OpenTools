import os
import cv2
import math

def get_total_frames(video_path: str) -> int:
    """
    Returns the total number of frames in a given video file.

    :param video_path: Path to the video file.
    :return: Total number of frames in the video.
    :raises: IOError if the video cannot be opened.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise IOError(f"Could not open video file: {video_path}")

    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # If frame count not available, count manually (slower but reliable)
    if total <= 0:
        print("Warning: Unable to get frame count via metadata, counting manually...")
        total = 0
        while True:
            success, _ = cap.read()
            if not success:
                break
            total += 1
        # Reset frame position to start for future use
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    cap.release()
    return total



class FrameExtractor:
    def __init__(self, video_path: str, output_folder: str, prefix: str = "frame", extension: str = ".jpg"):
        """
        Initializes the frame extractor.
        
        :param video_path: Path to input video file.
        :param output_folder: Folder where extracted frames will be saved.
        :param prefix: Filename prefix for saved frames.
        :param extension: File extension for saved images.
        """
        self.video_path = video_path
        self.output_folder = output_folder
        self.prefix = prefix
        self.extension = extension

        # Create output folder if it does not exist
        os.makedirs(self.output_folder, exist_ok=True)
    
    
    
    def extract_frames(self):
        """
        Extracts *all* frames from the video and saves them sequentially.
        
        :returns: number of frames saved
        """
        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            raise IOError(f"Could not open video file: {self.video_path}")
        
        count = 0
        success, frame = cap.read()
        while success:
            filename = os.path.join(self.output_folder, f"{self.prefix}{count:06d}{self.extension}")
            cv2.imwrite(filename, frame)
            count += 1
            success, frame = cap.read()
        
        cap.release()
        return count
    
    def extract_every_nth(self, n: int) -> int:
        """
        Extracts every n-th frame from the video and saves them.
        
        :param n: interval of frames to save (e.g., n=10 => save every 10th frame)
        :returns: number of frames saved
        """
        if n <= 0:
            raise ValueError("n must be a positive integer.")
        
        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            raise IOError(f"Could not open video file: {self.video_path}")
        
        count = 0
        saved = 0
        success, frame = cap.read()
        while success:
            if count % n == 0:
                filename = os.path.join(self.output_folder, f"{self.prefix}{count:06d}{self.extension}")
                cv2.imwrite(filename, frame)
                saved += 1
            count += 1
            success, frame = cap.read()

        cap.release()
        return saved
    
    def extract_n_frames(self, n: int) -> int:
        """
        Extract exactly N frames uniformly spaced across the video.
        
        :param n: number of frames you want to extract
        :returns: number of frames actually saved
        :raises: ValueError if requested n > total frames
        """
        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            cap.release()
            raise IOError(f"Could not open video file: {self.video_path}")
        
        total_frames = get_total_frames(self.video_path)
        if total_frames == 0:
            cap.release()
            raise RuntimeError("Could not determine total frame count for the video.")
        
        if n > total_frames:
            cap.release()
            raise ValueError(f"Requested {n} frames, but video only has {total_frames} frames.")
        
        # Compute the interval between frames (in terms of frame count) to pick
        interval = total_frames / float(n)
        
        saved = 0
        for i in range(n):
            # compute the frame index to capture
            frame_idx = int(math.floor(i * interval))
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            success, frame = cap.read()
            if not success:
                # if it fails, you can skip or break; here we skip
                continue
            filename = os.path.join(self.output_folder, f"{self.prefix}{saved:06d}{self.extension}")
            cv2.imwrite(filename, frame)
            saved += 1
        
        cap.release()
        return saved
    