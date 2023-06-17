import cv2
import time
import sys
import os

manual = '''
Press keys on keyboard to record value!
    C: photo shoot
    Q: Quit
'''

def main():
    dir_name = sys.argv[1]
    path = "./dataset/" + dir_name
    if not os.path.exists(path):
        os.makedirs(path)

    # Start camera capture
    cap = cv2.VideoCapture(cv2.CAP_V4L2)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    time.sleep(1)

    print(manual)
    while True:
        try:
            # Read keyboard input
            key = cv2.waitKey(1) & 0xFF

            # Take photo on 'Q' key press
            if key == ord('c'):
                ret, frame = cap.read()
                if ret:
                    frame = cv2.flip(frame, 0)
                    _time = time.strftime("%y-%m-%d_%H-%M-%S", time.localtime())
                    cv2.imwrite(f"{path}/{_time}.jpg", frame)
                    print(f"The photo saved as {path}/{_time}.jpg")

            # Quit on 'G' key press
            elif key == ord('q'):
                break

            # Show preview window
            ret, frame = cap.read()
            if ret:
                frame = cv2.flip(frame, 0)
                cv2.imshow("Preview", frame)

        except KeyboardInterrupt:
            break

    # Release resources and close windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
