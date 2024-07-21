import cv2

cap = cv2.VideoCapture('rtmp://localhost/stream', cv2.CAP_FFMPEG)


while True:
    ret, frame = cap.read()

    if not ret or frame is None or frame.size == 0:
        print("Error: Frame not captured properly")
        break

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()