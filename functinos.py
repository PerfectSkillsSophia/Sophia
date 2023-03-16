import cv2
import tempfile
import os
import speech_recognition as sr
import ffmpeg

def transcript(video):
    video_blob = video
    with tempfile.NamedTemporaryFile(suffix='.webm') as f:
        f.write(video_blob)
        f.seek(0)

    cap = cv2.VideoCapture(f.name)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("video",frame)
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
        cap.release()
        cv2.destroyAllWindows()