import cv2
import numpy as np
from ultralytics import YOLO


#liczenie kata
def calculate_angle(a, b, c):

    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle



model = YOLO('yolo11n-pose.pt')

#przechowywanie obrazu z kamery
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    #tu zmiana w zaleznosci jaka karta graficzna
    # device=0 oznacza użycie karty graficznej NVIDIA
    #results = model(frame, conf=0.5, device=0)
    results = model(frame, conf=0.5, device='cpu')
    found_anybody = False
    for r in results:
        if r.keypoints is not None and len(r.keypoints.xy) > 0 and r.keypoints.conf is not None:
            # pobranie punktow x i y dla pierwwszej rozpoznanej osoby
            # YOLO keypoints: 11-lewe biodro, 13-lewe kolano, 15-lewa kostka
            points = r.keypoints.xy[0].cpu().numpy()
            if len(points) > 0 and np.any(points):
                found_anybody = True
                try:
                    l_shoulder, l_elbow, l_wrist = points[5], points[7], points[9]
                    l_hip, l_knee, l_ankle = points[11], points[13], points[15]

                    r_shoulder, r_elbow, r_wrist = points[6], points[8], points[10]
                    r_hip, r_knee, r_ankle = points[12], points[14], points[16]

                    angles = [
                        ("L_knee", l_hip, l_knee, l_ankle),
                        ("R_knee", r_hip, r_knee, r_ankle),
                        ("L_hip", l_shoulder, l_hip, l_knee),
                        ("R_hip", r_shoulder, r_hip, r_knee),
                        ("L_elbow", l_shoulder, l_elbow, l_wrist),
                        ("R_elbow", r_shoulder, r_elbow, r_wrist),
                        ("L_shoulder", l_hip, l_shoulder, l_elbow),
                        ("R_shoulder", r_hip, r_shoulder, r_elbow)
                    ]
                    #zapisywanie wynikow
                    calculated_angles = {}
                    for label, pA, pW, pC in angles:
                        # sprawdzenie czy punkty zostaly wykryte/ nie sa zerami
                        if np.any(pA) and np.any(pW) and np.any(pC):
                            ang = calculate_angle(pA, pW, pC)
                            calculated_angles[label] = ang

                            # wizualizacja
                            cv2.putText(frame, f"{label}: {int(ang)}", tuple(pW.astype(int)),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

                    # feedback - przykladowo
                    l_k = calculated_angles.get("L Kolano", 0)
                    r_k = calculated_angles.get("R Kolano", 0)

                    if l_k > 170 and r_k > 170:
                        msg, color = "Nogi proste - OK", (0, 255, 0)
                    elif l_k == 0 or r_k == 0:
                        msg, color = "Ustaw sie bokiem/lepiej", (255, 255, 255)
                    else:
                        msg, color = "Zegnij/Wyprostuj!", (0, 0, 255)

                    cv2.putText(frame, msg, (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
                except IndexError:
                    pass
    if found_anybody:
        status_msg = "rozpoznano osobe"
        color = (0, 255, 0)
    else:
        status_msg = "szukanie osoby"
        color = (0, 0, 255)

    # wyświetlanie obrazu z szkieletem YOLO
    cv2.putText(frame, status_msg, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
    annotated_frame = results[0].plot() if found_anybody else frame
    cv2.imshow("cwiczenia z pilatesu", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()