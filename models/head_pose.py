import cv2
import mediapipe as mp
import numpy as np
import time
import math
import csv
from datetime import datetime


mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

mp_draw = mp.solutions.drawing_utils

distraction_start = None
DISTRACTION_THRESHOLD = 4.5
is_distracted = False
EAR_THRESHOLD = 0.12      

total_events = 0
eyes_closed_events = 0
side_events = 0
up_events = 0
down_events = 0


prev_alert = False  


def euclidean_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def calculate_EAR(eye_points):
   
    A = euclidean_distance(eye_points[1], eye_points[5])
    B = euclidean_distance(eye_points[2], eye_points[4])
    C = euclidean_distance(eye_points[0], eye_points[3])

    EAR = (A + B) / (2.0 * C)
    return EAR


RIGHT_EYE_IDX = [33, 160, 158, 133, 153, 144]
LEFT_EYE_IDX  = [263, 387, 385, 362, 380, 373]

def detect_distraction(rot_x, rot_y,rot_z,avg_EAR):
   
    if avg_EAR < EAR_THRESHOLD:
        return "EYES CLOSED"
    
    if rot_y > 0.16  or  rot_y < -0.04:  
        return "Looking SIDE"

    if rot_x > -0.07:
        return "Looking UP"

    if rot_x < -0.25:
        return "Looking DOWN"   
       
    return "Looking FORWARD"


def time_based_check(state):
    global distraction_start, is_distracted

    distracting = ["Looking SIDE", "Looking DOWN", "Looking UP","EYES CLOSED"]

    if state == "EYES CLOSED":
        DISTRACTION_THRESHOLD = 2.5   
    else:
        DISTRACTION_THRESHOLD = 4.5 

    if state in distracting:
        if distraction_start is None:
            distraction_start = time.time()

        if time.time() - distraction_start >= DISTRACTION_THRESHOLD:
            is_distracted = True

    else:
        distraction_start = None
        is_distracted = False

    return is_distracted


KEY_POINTS = {
    "nose_tip": 1,
    "chin": 152,
    "left_eye": 33,
    "right_eye": 263,
    "left_mouth": 61,
    "right_mouth": 291
}

cap = cv2.VideoCapture(0)

session_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_filename = f"events_{session_time}.csv"

events_log = open(log_filename, mode="w", newline="")
events_writer = csv.writer(events_log)

events_writer.writerow(["timestamp", "event"])
print(f"[SESSION LOG CREATED] {log_filename}")


while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:
        for lm in results.multi_face_landmarks:
            right_eye = []
            left_eye = []

            for idx in RIGHT_EYE_IDX:
                x = int(lm.landmark[idx].x * w)
                y = int(lm.landmark[idx].y * h)
                right_eye.append(np.array([x, y]))

            for idx in LEFT_EYE_IDX:
                x = int(lm.landmark[idx].x * w)
                y = int(lm.landmark[idx].y * h)
                left_eye.append(np.array([x, y]))

            right_EAR = calculate_EAR(np.array(right_eye))
            left_EAR = calculate_EAR(np.array(left_eye))

            avg_EAR = (right_EAR + left_EAR) / 2
                        
            points_2d = []
            points_3d = []

            for key, idx in KEY_POINTS.items():
                p = lm.landmark[idx]
                x = int(p.x * w)
                y = int(p.y * h)
                points_2d.append([x, y])
                points_3d.append([x, y, p.z * 3000])

            points_2d = np.array(points_2d, dtype=np.float64)
            points_3d = np.array(points_3d, dtype=np.float64)

            focal_length = w
            cam_matrix = np.array([
                [focal_length, 0, w / 2],
                [0, focal_length, h / 2],
                [0, 0, 1]
            ])

            dist_matrix = np.zeros((4, 1), dtype=np.float64)

           
            success, rot_vec, trans_vec = cv2.solvePnP(
              points_3d,
              points_2d,
              cam_matrix,
              dist_matrix,
              flags=cv2.SOLVEPNP_SQPNP
            )
            
            rot_x = float(rot_vec[0])
            rot_y = float(rot_vec[1])
            rot_z = float(rot_vec[2])

            
            driver_state = detect_distraction(rot_x, rot_y,rot_z,avg_EAR)
            alert = time_based_check(driver_state)
                                                        
           # if alert and not prev_alert:

    ##            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    ##            events_writer.writerow([timestamp, driver_state])
    ##            print(f"[EVENT LOGGED] {timestamp} - {driver_state}")
    ##            img_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    ##            filename = f"event_{img_timestamp}_{driver_state.replace(' ', '_')}.jpg"
    ##            cv2.imwrite(filename, frame)
    ##            print(f"[IMAGE SAVED] {filename}")
    ##            
    ##            total_events += 1
##
    ##            if driver_state == "EYES CLOSED":
    ##                eyes_closed_events += 1
    ##            elif driver_state == "Looking SIDE":
    ##                side_events += 1
    ##            elif driver_state == "Looking UP":
    ##                up_events += 1
    ##            elif driver_state == "Looking DOWN":
    ##                down_events += 1
    ##           
    ##        prev_alert = alert
    ##        

##
    ##        if alert:
    ##            cv2.putText(frame, " DRIVER DISTRACTED! CONTACTING MANAGER", (30, 250),
    ##                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    ##        else:
    ##            cv2.putText(frame, "Driver OK", (30, 250),
    ##                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    ##            cv2.putText(frame, f"Total events: {total_events}", (30, 300),
    ##        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

        #    cv2.putText(frame, f"Eyes closed events: {eyes_closed_events}", (30, 330),
        #    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
#
        #    cv2.putText(frame, f"Side events: {side_events}", (30, 360),
        #    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 200, 255), 2)
#
        #    cv2.putText(frame, f"Up events: {up_events}", (30, 390),
        #    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 200), 2)
#
        #    cv2.putText(frame, f"Down events: {down_events}", (30, 420),
        #    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 150), 2)
            
#            cv2.putText(frame, f"Driver: {avg_EAR}", (30, 210),
#                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)    
#            cv2.putText(frame, f"Driver: {driver_state}", (30, 160),
#                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
#            cv2.putText(frame, f"Rot X: {rot_x:.3f}", (30, 40),
#                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
#            cv2.putText(frame, f"Rot Y: {rot_y:.3f}", (30, 80),
#                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
#            cv2.putText(frame, f"Rot Z: {rot_z:.3f}", (30, 120),
#                      cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
            
            
    cv2.imshow("Head Pose ", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
events_log.close()
cv2.destroyAllWindows()
