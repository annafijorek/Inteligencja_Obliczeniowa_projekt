import cv2
import numpy as np
import time

from sympy import false
from ultralytics import YOLO

class logic:

    def __init__(self):
        self.model = YOLO('yolo11s-pose.pt')
        #yolo11n-pose.pt- szybsza ale slabsza wersja yolo
        self.current_exercise="Plank"

        self.start_time=None
        self.reps=0
        self.pose=False
        self.stage="down"
        self.time_limit = 1.5
        #reps- powtorzenia
        #pose-pozycja docelowa np noga w gorze


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


    def check_person(self,points, confidences):
        critical_points=[5,6,7,8,9,10,11,12,13,14,15,16]
        for i in critical_points:
            if points[i][0]==0 or points[i][1]==0 or confidences[i]<0.25:
                return False
        return True

    def video_check(self,frame):
        alpha=1.3
        beta=40
        ai_frame=cv2.convertScaleAbs(frame,alpha=1.1,beta=0)


        results = self.model(ai_frame, conf=0.3, device='cpu',verbose=False) #verbose- logi ai
        # device=0 oznacza użycie karty graficznej NVIDIA
        # results = model(frame, conf=0.5, device=0)
        msg = ""
        color = "#FFFFFF"
        annotated_frame=frame.copy()   #ustawienie domyslne, jesli nie znajdzie osoby


        if results and results[0].keypoints is not None and len(results[0].keypoints.xy) > 0 :
            r = results[0]
            # pobranie punktow x i y dla pierwwszej rozpoznanej osoby
            # YOLO keypoints: 11-lewe biodro, 13-lewe kolano, 15-lewa kostka
            points = r.keypoints.xy[0].cpu().numpy()

            confidence=r.keypoints.conf[0].cpu().numpy()
            annotated_frame = r.plot()
            if len(points) > 0 and np.any(points):
                full_body = self.check_person(points,confidence)
                if not full_body:
                    msg = "Oddal sie od kamery"
                    color = "#FF0000"
                    self.start_time=None
                    return annotated_frame, msg, color

                try:
                    nose = points[0]
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
                        ("R_body", r_shoulder, r_hip, r_ankle),

                    ]

                    # zapisywanie wynikow
                    calculated_angles = {}
                    for label, pA, pW, pC in angles:
                        # sprawdzenie czy punkty zostaly wykryte/ nie sa zerami
                        if np.any(pA) and np.any(pW) and np.any(pC):
                            ang = self.calculate_angle(pA, pW, pC)
                            calculated_angles[label] = ang

                            # wizualizacja annotated_frame-wyswietlanie katow, frame- bez katow
                            cv2.putText(annotated_frame, f"{label}: {int(ang)}", tuple(pW.astype(int)),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                    l_knee_angle = calculated_angles.get("L_knee", 0)
                    r_knee_angle = calculated_angles.get("R_knee", 0)
                    l_body_angle = calculated_angles.get("L_body", 0)
                    r_body_angle = calculated_angles.get("R_body", 0)
                    l_shoulder_angle = calculated_angles.get("L_shoulder", 0)
                    r_shoulder_angle = calculated_angles.get("R_shoulder", 0)
                    l_hip_angle = calculated_angles.get("L_hip", 0)
                    r_hip_angle = calculated_angles.get("R_hip", 0)
                    l_elbow_angle=calculated_angles.get("L_elbow", 0)
                    r_elbow_angle=calculated_angles.get("R_elbow",0)

                    if self.current_exercise == "Plank":
                        is_straight = (190>l_body_angle > 165) or (190>r_body_angle > 165)
                        #arms_straight = (l_elbow_angle > 160) or (r_elbow_angle > 160)
                        arms_90 = (70 < l_elbow_angle < 110) or (70 < r_elbow_angle < 110)
                        is_horizontal = abs(l_shoulder[1] - l_hip[1]) < 100 or abs(r_shoulder[1] - r_hip[1]) < 100
                        not_floor = (l_hip[1] < l_ankle[1] - 20) or (r_hip[1] < r_ankle[1] - 20)
                        if is_straight and arms_90 and is_horizontal and not_floor:
                            if self.start_time is None:
                                self.start_time=time.time()
                            workout_time=int(time.time() - self.start_time)
                            msg = f"Tak trzymaj! Czas: {workout_time}s"
                            color = "#00FF00"
                        elif l_body_angle > 0 or r_body_angle > 0:
                            msg = "Popraw pozycje"
                            color = "#FF0000"
                            self.start_time=None
                        else:
                            msg = "Nikogo nie widze :(("
                            self.start_time=None
                    elif self.current_exercise == "JumpingJack":
                        # msg=""
                        # color=""

                        hands_up = l_wrist[1] < nose[1] and r_wrist[1] < nose[1]
                        shoulder_dist = np.linalg.norm(l_shoulder - r_shoulder)
                        feet_dist = np.linalg.norm(l_ankle - r_ankle)
                        feet_wide = feet_dist > (shoulder_dist * 1.5)
                        current_time = time.time()
                        if self.stage == "down" and self.reps > 0:
                            if current_time - getattr(self, 'last_rep_time', current_time) > 3.0:
                                self.reps = 0
                                msg = f"Wynik: {self.reps}"
                                color = "#FF0000"
                        if hands_up and feet_wide:
                            if self.stage == "down":
                                self.stage = "up"
                                self.rep_start_time = current_time
                            msg = f"Wynik: {self.reps}"
                            color = "#00FF00"
                        elif not hands_up and not feet_wide:
                            if self.stage == "up":
                                duration = current_time - self.rep_start_time
                                if duration <= self.time_limit:
                                    self.reps += 1
                                else:
                                    self.reps = 0

                                self.stage = "down"
                                self.rep_start_time = None
                                msg = ""
                                color = "#FF0000"
                            else:
                                if self.stage == "up" and (current_time - self.rep_start_time) > self.time_limit:
                                    self.reps = 0
                                    self.stage = "down"
                                msg = ""
                                color = "#FFFF00"
                        else:
                            msg = "Powtorzenie wykonane niepoprawnie"
                            color = "#FFFF00"



                    else:
                        msg="nie wybrano cwiczenia"
                        color = "#FF0000"

                except IndexError:
                    msg="nie ma wszystkich punktow"
                    color = "#FFFF00"
                except Exception as e:
                    print(f"Błąd: {e}")
                    msg = "Blad"
                    color = "#FFFF00"

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