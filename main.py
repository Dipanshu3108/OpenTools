from get_frames import FrameExtractor, get_total_frames

video_path = "downloads\zoro_vs_king.mp4"
output_dir= "frames_all"


frames = get_total_frames(video_path)
print(f"Total frames: {frames}")

extractor = FrameExtractor(video_path, output_dir)
total = extractor.extract_n_frames(10)
print(f"Done: {total} frames saved to '{output_dir}'")