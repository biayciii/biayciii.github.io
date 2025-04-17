import streamlit as st
import cv2
import numpy as np
from ultralytics import YOLO
import os

class PlayerTracker:
    def __init__(self, model_path):
        self.model = YOLO(model_path)
        self.tracker_type = "bytetrack.yaml"

    def detect_frames(self, frames):
        return [self.detect_frame(frame, idx) for idx, frame in enumerate(frames)]

    def detect_frame(self, frame, idx=0):
        results = self.model.track(frame, persist=True, tracker=self.tracker_type)[0]
        id_name_dict = results.names

        team1_players = {}
        team2_players = {}

        for box in results.boxes:
            if box.id is not None:
                track_id = int(box.id.tolist()[0])
                x1, y1, x2, y2 = box.xyxy.tolist()[0]
                class_id = int(box.cls.tolist()[0])
                class_name = id_name_dict[class_id]

                if class_name == "Team1":
                    team1_players[track_id] = (x1, y1, x2, y2)
                elif class_name == "Team2":
                    team2_players[track_id] = (x1, y1, x2, y2)

        return {"Team1": team1_players, "Team2": team2_players}

    def assign_player_roles(self, detections_per_frame, frame_height):
        updated_detections = []
        for frame_data in detections_per_frame:
            players = []
            for team in ["Team1", "Team2"]:
                for track_id, (x1, y1, x2, y2) in frame_data[team].items():
                    y_center = (y1 + y2) / 2
                    players.append({"track_id": track_id, "bbox": (x1, y1, x2, y2), "y_center": y_center})

            players_sorted = sorted(players, key=lambda x: x["y_center"])

            player_dict = {}
            if len(players_sorted) >= 2:
                player_dict["Player1"] = players_sorted[0]["bbox"]
                player_dict["Player2"] = players_sorted[1]["bbox"]

            updated_detections.append(player_dict)

        return updated_detections

    def draw_bboxes(self, frames, player_detections):
        for frame, player_dicts in zip(frames, player_detections):
            for player, color in zip(["Player1", "Player2"], [(255, 255, 0), (255, 255, 0)]):
                if player in player_dicts:
                    x1, y1, x2, y2 = map(int, player_dicts[player])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 3)
                    cv2.putText(frame, player, (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        return frames

    def save_video(self, frames, output_path, fps=30):
        height, width = frames[0].shape[:2]
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        for frame in frames:
            out.write(frame)

        out.release()
        print(f"[✅ DONE] Video saved at {output_path}")
        return output_path  # Trả về đường dẫn video đã lưu


# === Giao diện Streamlit ===
st.title("🎾 Ứng dụng phân tích trận đấu Pickleball")
st.write("Tải video từ máy tính để phân tích trận đấu và hiển thị kết quả.")

# Tải video từ file
video_file = st.file_uploader("📥 Chọn video", type=["mp4", "mov", "avi"])

if video_file is not None:
    video_path = "uploaded_video.mp4"
    with open(video_path, "wb") as f:
        f.write(video_file.read())

    st.info("⏳ Đang phân tích video...")

    # Khởi tạo tracker
    model_path = "last_pt_new.pt"  # Cập nhật đúng đường dẫn mô hình của bạn
    if not os.path.exists(model_path):
        st.error(f"❌ Không tìm thấy mô hình tại: {model_path}")
        st.stop()

    tracker = PlayerTracker(model_path)

    # Đọc tất cả frame từ video
    cap = cv2.VideoCapture(video_path)
    frames = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    cap.release()

    if len(frames) == 0:
        st.error("❌ Không đọc được khung hình nào từ video.")
        st.stop()

    # Phát hiện và gán người chơi
    detections = tracker.detect_frames(frames)
    frame_height = frames[0].shape[0]
    player_detections = tracker.assign_player_roles(detections, frame_height)

    # Vẽ bounding boxes & lưu video output
    output_frames = tracker.draw_bboxes(frames, player_detections)
    output_video_path = "output_video_player_tracker.mp4"
    saved_video_path = tracker.save_video(output_frames, output_video_path)

    # Hiển thị video đã xử lý
    if os.path.exists(saved_video_path):
        st.success("✅ Video đã xử lý xong. Xem bên dưới:")
        st.video(saved_video_path)
    else:
        st.error("❌ Không tìm thấy video output.")
