import cv2
import numpy as np
from ultralytics import YOLO

class pilates_logic:

    def __init__(self):
        self.model = YOLO('yolo11n-pose.pt')
        self.current_exercise="Plank"

    #liczenie kata
    def calculate_angle(self,a, b, c):

        a = np.array(a)
        b = np.array(b)
        c = np.array(c)

        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)

        if angle > 180.0:
            angle = 360 - angle

        return angle


    def check_person(self,points):
        critical_points=[5,6,7,8,9,10,11,12,13,14,15,16]
        for i in critical_points:
            if points[i][0]==0 or points[i][1]==0:
                return False
            return True

    def video_check(self,frame):
        results = self.model(frame, conf=0.5, device='cpu',verbose=False) #verbose- logi ai
        # device=0 oznacza użycie karty graficznej NVIDIA
        # results = model(frame, conf=0.5, device=0)
        msg = ""
        color = "#FFFFFF"
        annotated_frame=frame   #ustawienie domyslne, jesli nie znajdzie osoby


        if results and results[0].keypoints is not None and len(results[0].keypoints.xy) > 0 :
            r = results[0]
            # pobranie punktow x i y dla pierwwszej rozpoznanej osoby
            # YOLO keypoints: 11-lewe biodro, 13-lewe kolano, 15-lewa kostka
            points = r.keypoints.xy[0].cpu().numpy()
            annotated_frame = r.plot()
            if len(points) > 0 and np.any(points):
                full_body = self.check_person(points)
                if not full_body:
                    msg = "Oddal sie od kamery"
                    color = "#FF0000"
                    return annotated_frame, msg, color

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
                        ("R_shoulder", r_hip, r_shoulder, r_elbow),

                        ("L_body", l_shoulder, l_hip, l_ankle),
                        ("R_body", r_shoulder, r_hip, r_ankle)
                    ]

                    # zapisywanie wynikow
                    calculated_angles = {}
                    for label, pA, pW, pC in angles:
                        # sprawdzenie czy punkty zostaly wykryte/ nie sa zerami
                        if np.any(pA) and np.any(pW) and np.any(pC):
                            ang = self.calculate_angle(pA, pW, pC)
                            calculated_angles[label] = ang

                            # wizualizacja
                            cv2.putText(frame, f"{label}: {int(ang)}", tuple(pW.astype(int)),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                    l_knee_angle = calculated_angles.get("L_knee", 0)
                    r_knee_angle = calculated_angles.get("R_knee", 0)
                    l_body_angle = calculated_angles.get("L_body", 0)
                    r_body_angle = calculated_angles.get("R_body", 0)
                    l_shoulder_angle = calculated_angles.get("L_shoulder", 0)
                    r_shoulder_angle = calculated_angles.get("R_shoulder", 0)
                    l_hip_angle = calculated_angles.get("L_hip", 0)
                    r_hip_angle = calculated_angles.get("R_hip", 0)

                    if self.current_exercise == "Plank":
                        is_straight = (l_body_angle > 165) or (r_body_angle > 165)
                        if is_straight:
                            msg = "Tak trzymaj!"
                            color = "#00FF00"
                        elif l_body_angle > 0 or r_body_angle > 0:
                            msg = "Popraw pozycje"
                            color = "#FF0000"
                        else:
                            msg = "Nikogo nie widze :(("
                    elif self.current_exercise == "WarriorII":
                        # prawa lub lewa nowa jest zgieta 90stopni druga musi byc prosta
                        # trzeba poprawic aby tylko jedna opcje mogla byc
                        left_leg = (80 < l_knee_angle < 110) and (r_knee_angle > 160)
                        right_leg = (80 < r_knee_angle < 110) and (l_knee_angle > 160)
                        arms_position = (l_shoulder_angle > 80) and (r_shoulder_angle > 80)

                        if (left_leg or right_leg) and arms_position:
                            msg = "Tak trzymaj!"
                            color = "#00FF00"
                        elif (left_leg or right_leg) and not arms_position:
                            msg = "Popraw pozycje rak"
                            color = "#FF0000"
                        else:
                            msg = "Popraw pozycje nog"
                            color = "#FF0000"
                        # tu jeszcze wiecej warunkow???

                    elif self.current_exercise == "Bird Dog":
                        leg_extended = (l_hip_angle > 160) or (r_hip_angle > 160)

                        if leg_extended:
                            msg = "Tak trzymaj!"
                            color = "#00FF00"
                        else:
                            msg = "Popraw pozycje"
                            color = "#FF0000"

                except IndexError:
                    pass

            return annotated_frame, msg, color

        # if found_anybody:
        #     status_msg = "rozpoznano osobe"
        #     color = (0, 255, 0)
        # else:
        #     status_msg = "szukanie osoby"
        #     color = (0, 0, 255)
        #
        # # wyświetlanie obrazu z szkieletem YOLO
        # #cv2.putText(frame, status_msg, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        # annotated_frame = results[0].plot() if found_anybody else frame
        # cv2.imshow("cwiczenia z pilatesu", annotated_frame)


    # cap.release()
    # cv2.destroyAllWindows()