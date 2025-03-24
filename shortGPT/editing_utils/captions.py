import cv2
import numpy as np
import os
from typing import List, Tuple


def draw_caption(frame, text, highlight_word, position=(50, 400), font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=1,
                 font_thickness=2, text_color=(255, 255, 255), highlight_color=(0, 255, 0)):
    """
    Draws caption text on the video frame, highlighting the current spoken word.
    """
    words = text.split()
    text_x, text_y = position
    x_offset = text_x  # Start from given position

    for i, word in enumerate(words):
        word_size = cv2.getTextSize(word, font, font_scale, font_thickness)[0]
        word_x = x_offset

        # Highlight the word if it matches
        if word == highlight_word:
            cv2.rectangle(frame, (word_x - 5, text_y - 30), (word_x + word_size[0] + 5, text_y + 5), highlight_color, -1)
            cv2.putText(frame, word, (word_x, text_y), font, font_scale, (0, 0, 0), font_thickness)
        else:
            cv2.putText(frame, word, (word_x, text_y), font, font_scale, text_color, font_thickness)

        x_offset += word_size[0] + 15  # Adjust spacing dynamically

    return frame
                   
def getCaptionsWithTime(video_path):
    """
    Mock function to get captions with timestamps.
    Returns a list of tuples: [(start_time, end_time, caption_text)]
    """
    return [
        (0, 2, "Hello, welcome to this video."),
        (2, 5, "This is an example caption."),
        (5, 7, "Hope you enjoy the content.")
    ]


def generate_video_with_captions(video_path, captions, output_path=None):
    """
    Adds captions with dynamic word highlighting to the video.
    """
    if output_path is None:
        output_path = os.path.join(os.path.dirname(video_path), "output.mp4")

    cap = cv2.VideoCapture(video_path)
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        current_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000  # Get time in seconds

        for (time_range, caption) in captions:
            start, end = time_range
            words = caption.split()
            
            if start <= current_time <= end and words:
                duration_per_word = max((end - start) / len(words), 0.1)  # Avoid zero division
                word_index = min(int((current_time - start) / duration_per_word), len(words) - 1)
                frame = draw_caption(frame, caption, words[word_index])
                break
        
        out.write(frame)

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"Video processing complete. Saved as {output_path}")
