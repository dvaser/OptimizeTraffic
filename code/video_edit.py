import cv2
import numpy as np
import os
from moviepy.editor import VideoFileClip, concatenate_videoclips

def combine_videos(video_files, output_file):
    clips = [VideoFileClip(f) for f in video_files]
    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(output_file, codec="libx264")

def create_four_screen_video(videos_folder, output_folder, road_info_file):
    cam_videos = {f'cam{i}': [] for i in range(1, 5)}
    
    # Videolar? grupland?r
    for file in os.listdir(videos_folder):
        if file.endswith(".avi"):
            parts = file.split('_')
            cam_index = parts[0]
            cam_videos[cam_index].append(os.path.join(videos_folder, file))

    # Videolar? birle?tir
    combined_videos = {}
    for cam, files in cam_videos.items():
        if files:
            combined_file = os.path.join(output_folder, f'{cam}.avi')
            combine_videos(files, combined_file)
            combined_videos[cam] = combined_file

    # Ad?m verilerini oku
    with open(road_info_file, 'r') as file:
        steps = file.read().split('\n\n')

    # 4 ekran videosu olu?turma
    caps = [cv2.VideoCapture(combined_videos.get(f'cam{i}', None)) for i in range(1, 5)]
    frame_width = int(caps[0].get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(caps[0].get(cv2.CAP_PROP_FRAME_HEIGHT))
    output_size = (frame_width * 2, frame_height * 2)

    out = cv2.VideoWriter(os.path.join(output_folder, 'output.avi'), cv2.VideoWriter_fourcc(*'XVID'), 30, output_size)

    for step_index, step in enumerate(steps):
        # Ye?il ???k alacak yollar? belirle
        green_cameras = []
        info_text = ""
        duration = 0
        lines = step.split('\n')
        for line in lines:
            if line.startswith("Road"):
                road_id = int(line.split(":")[1].strip())
                green_cameras.append(f'cam{road_id}')
            elif line.startswith("REASON"):
                info_text = line.split(":")[1].strip()
            elif line.startswith("Duration"):
                duration = float(line.split(":")[1].strip())

        # Ye?il ???k yanan kamera �er�evelerini ye?il yap
        for cam in green_cameras:
            x = (int(cam[-1]) - 1) % 2 * frame_width
            y = (int(cam[-1]) - 1) // 2 * frame_height
            cv2.rectangle(combined_frame, (x, y), (x + frame_width, y + frame_height), (0, 255, 0), 10)

        # Di?er kamera �er�evelerini k?rm?z? yap
        for cam in set(cam_videos.keys()) - set(green_cameras):
            x = (int(cam[-1]) - 1) % 2 * frame_width
            y = (int(cam[-1]) - 1) // 2 * frame_height
            cv2.rectangle(combined_frame, (x, y), (x + frame_width, y + frame_height), (0, 0, 255), 10)

        # Bilgi metnini ekle
        combined_frame = np.zeros((output_size[1], output_size[0], 3), dtype=np.uint8)
        cv2.putText(combined_frame, info_text, (10, output_size[1] - 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(combined_frame, f'Duration: {duration} sec', (10, output_size[1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        out.write(combined_frame)

    for cap in caps:
        cap.release()
    out.release()

# Parametreler
videos_folder = "videos/"
output_folder = "videos/video/"
road_info_file = "docs/run.txt"

# �?kt? klas�r�n� olu?tur
os.makedirs(output_folder, exist_ok=True)

create_four_screen_video(videos_folder, output_folder, road_info_file)
