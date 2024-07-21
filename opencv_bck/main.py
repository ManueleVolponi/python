import cv2
def __main__():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open video stream")
        exit()

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