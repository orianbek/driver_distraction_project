import cv2
import mediapipe as mp
import math

def euclidean_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def eye_aspect_ratio(eye_points):
    
    
   
    A = euclidean_distance(eye_points[1], eye_points[5])
    B = euclidean_distance(eye_points[2], eye_points[4])
    C = euclidean_distance(eye_points[0], eye_points[3])

    EAR = (A + B) / (2.0 * C)
    return EAR

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

mp_draw = mp.solutions.drawing_utils


RIGHT_EYE = [33, 160, 158, 133, 153, 144]
LEFT_EYE  = [263, 387, 385, 362, 380, 373]

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:
        for landmarks in results.multi_face_landmarks:
            
            # קבלת נקודות פיזיות של העיניים
            right_eye_points = []
            left_eye_points = []

            for idx in RIGHT_EYE:
                lm = landmarks.landmark[idx]
                right_eye_points.append((lm.x * w, lm.y * h))

            for idx in LEFT_EYE:
                lm = landmarks.landmark[idx]
                left_eye_points.append((lm.x * w, lm.y * h))

            # חישוב EAR
            right_EAR = eye_aspect_ratio(right_eye_points)
            left_EAR = eye_aspect_ratio(left_eye_points)
            avg_EAR = (right_EAR + left_EAR) / 2.0

            # הצגה על המסך
            cv2.putText(frame, f"EAR: {avg_EAR:.2f}", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    cv2.imshow("EAR Eye Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()