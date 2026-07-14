import cv2
import time


def camera_preview():

    camera = cv2.VideoCapture(0)


    if not camera.isOpened():
        print("Camera failed")
        return False


    start_time = time.time()


    while True:

        success, frame = camera.read()

        if not success:
            break


        cv2.putText(
            frame,
            "Camera Test",
            (30,50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0,255,0),
            2
        )


        cv2.imshow(
            "Camera Test",
            frame
        )


        # Show for 3 seconds
        if time.time() - start_time > 3:
            break


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break



    camera.release()
    cv2.destroyWindow("Camera Test")


    return True