import cv2
import numpy as np
import time
import os

def draw_caption(frame, text, highlight_word, position=(50, 400), font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=1,
                 font_thickness=2, text_color=(255, 255, 255), highlight_color=(0, 255, 0)):
    """
    Draws caption text on the video frame, highlighting the current spoken word.
    """
    words = text.split()
    highlight_index = words.index(highlight_word) if highlight_word in words else -1
    
    text_x, text_y = position
    total_text = ""
    
    for i, word in enumerate(words):
        word_size = cv2.getTextSize(word, font, font_scale, font_thickness)[0]
        word_x = text_x + len(total_text) * 12
        
        # Highlight the current word
        if i == highlight_index:
            cv2.rectangle(frame, (word_x - 5, text_y - 30), (word_x + word_size[0] + 5, text_y + 5), highlight_color, -1)
            cv2.putText(frame, word, (word_x, text_y), font, font_scale, (0, 0, 0), font_thickness)
        else:
            cv2.putText(frame, word, (word_x, text_y), font, font_scale, text_color, font_thickness)
        
        total_text += word + " "
    
    return frame

def generate_video_with_captions(video_path, captions, output_path=None):
    """
    Adds captions with dynamic word highlighting to the video.
    """
    if output_path is None:
        output_path = os.path.join(os.path.dirname(video_path), "output.mp4")
    
    cap = cv2.VideoCapture(video_path)
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, cap.get(cv2.CAP_PROP_FPS),
                          (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))
    
    frame_count = 0
    start_time = time.time()
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        current_time = time.time() - start_time
        
        for (time_range, caption) in captions:
            start, end = time_range
            if start <= current_time <= end:
                words = caption.split()
                duration_per_word = (end - start) / len(words)
                word_index = min(int((current_time - start) / duration_per_word), len(words) - 1)
                frame = draw_caption(frame, caption, words[word_index])
                break
        
        out.write(frame)
        frame_count += 1
    
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"Video processing complete. Saved as {output_path}")
