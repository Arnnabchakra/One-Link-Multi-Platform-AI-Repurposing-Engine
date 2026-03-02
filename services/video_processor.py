from moviepy import VideoFileClip

def process_video(input_path, output_path):
    clip = VideoFileClip(input_path)

    # Trim to 60 seconds
    if clip.duration > 60:
        clip = clip.subclipped(0, 60)

    # Resize to 9:16
    clip = clip.resized((1080, 1920))

    clip.write_videofile(output_path, codec="libx264")

    clip.close()