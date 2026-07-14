import cv2
import mediapipe as mp
import math
import time


# -----------------------------
# Function to calculate angle
# -----------------------------
def calculate_angle(a, b, c):

    ax, ay = a.x, a.y
    bx, by = b.x, b.y
    cx, cy = c.x, c.y

    radians = math.atan2(cy - by, cx - bx) - math.atan2(ay - by, ax - bx)

    angle = abs(math.degrees(radians))

    if angle > 180:
        angle = 360 - angle

    return angle



# -----------------------------
# Start Pushup Challenge
# -----------------------------
def start_pushup_test(target_reps):

    # Initialize MediaPipe
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()

    mp_draw = mp.solutions.drawing_utils


    # Open webcam
    camera = cv2.VideoCapture(0)


    # Pushup variables
    counter = 0
    stage = None


    # Countdown
    countdown_start = time.time()
    tracking_started = False



    while True:

        success, frame = camera.read()

        if not success:
            break



        # Convert image
        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )


        # Detect pose
        results = pose.process(rgb)



        if results.pose_landmarks:


            # Draw skeleton
            mp_draw.draw_landmarks(
                frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS
            )


            landmarks = results.pose_landmarks.landmark


            left_shoulder = landmarks[
                mp_pose.PoseLandmark.LEFT_SHOULDER
            ]

            left_elbow = landmarks[
                mp_pose.PoseLandmark.LEFT_ELBOW
            ]

            left_wrist = landmarks[
                mp_pose.PoseLandmark.LEFT_WRIST
            ]



            angle = calculate_angle(
                left_shoulder,
                left_elbow,
                left_wrist
            )



            # -----------------------------
            # Countdown before starting
            # -----------------------------
            if not tracking_started:

                elapsed = time.time() - countdown_start

                remaining = 3 - int(elapsed)


                if remaining > 0:

                    cv2.putText(
                        frame,
                        f"Countdown: {remaining}",
                        (350,100),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0,255,0),
                        2
                    )

                else:

                    tracking_started = True



            # -----------------------------
            # Pushup counting
            # -----------------------------
            if tracking_started:


                # Top position
                if angle > 160:


                    # Finished a rep
                    if stage == "DOWN":
                        counter += 1


                    stage = "UP"



                # Bottom position
                elif angle < 90:

                    stage = "DOWN"


        # Display count
        cv2.putText(
            frame,
            f"Pushups: {counter}/{target_reps}",
            (30,100),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255,255,255),
            2
        )



        # -----------------------------
        # Target Achieved State
        # -----------------------------
        if counter >= target_reps:

            # 1. Draw completion messages onto the frame
            cv2.putText(
                frame,
                "Completed!",
                (220,150),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.5,
                (0,255,0),
                3
            )
            
            cv2.putText(
                frame,
                "Press [SPACE] or [R] to return to game",
                (50,420),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255,255,255),
                2
            )

            cv2.imshow(
                "Pushup Tracker",
                frame
            )

            # 2. Halt everything and wait specifically for the user to signal a respawn
            print("Workout finished! Waiting for user to confirm respawn...")
            while True:
                key = cv2.waitKey(100) & 0xFF
                # 32 = Spacebar, ord('r')/ord('R') = R Key
                if key == 32 or key == ord('r') or key == ord('R'):
                    break
                
                # Safe breakout option if you manually close the camera window using the OS 'X' button
                if cv2.getWindowProperty("Pushup Tracker", cv2.WND_PROP_VISIBLE) < 1:
                    break

            break



        cv2.imshow(
            "Pushup Tracker",
            frame
        )


        # -----------------------------
        # Manual Quit / Skip Early
        # -----------------------------
        # Allows you to press Q, R, or Spacebar to skip back to the game at any point
        key_press = cv2.waitKey(1) & 0xFF
        if key_press in [ord('q'), ord('r'), ord('R'), 32]:
            break



    # Cleanup
    camera.release()
    cv2.destroyAllWindows()