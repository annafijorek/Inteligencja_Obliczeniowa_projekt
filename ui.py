import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
from yolo_script import logic


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")


class Workout_App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Workout Assistant")
        self.geometry("1200x800")

        self.logic = logic()
        self.is_running=False
        self.exercise_buttons = {}

        self.cap = cv2.VideoCapture(0)
        #self.cap = cv2.VideoCapture("resources/jumpingjack.mp4") #nagranie z pliku

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(8, weight=0)

        #zrodlo obrazu
        self.source_label = ctk.CTkLabel(self.sidebar_frame, text="Zrodlo obrazu:", font=ctk.CTkFont(weight="bold"))
        self.source_label.grid(row=0, column=0, padx=20, pady=(10, 5))

        self.source_buttons = {}
        self.btn_cam = ctk.CTkButton(self.sidebar_frame, text="Kamera",
                                 command=lambda: self.change_source(0, "cam"),
                                 fg_color="#D81B60", hover_color="#AD1457", height=50, font=ctk.CTkFont(size=16))
        self.btn_cam.grid(row=1, column=0, padx=20, pady=5)
        self.source_buttons["cam"] = self.btn_cam

        self.btn_plank_vid = ctk.CTkButton(self.sidebar_frame, text="Wideo: Plank",
                                           command=lambda: self.change_source("resources/plank.mp4", "plank"),
                                           fg_color="#D81B60", hover_color="#AD1457", height=50,
                                           font=ctk.CTkFont(size=16))
        self.btn_plank_vid.grid(row=2, column=0, padx=20, pady=5, sticky="ew")
        self.source_buttons["plank"] = self.btn_plank_vid

        self.btn_jump_vid = ctk.CTkButton(self.sidebar_frame, text="Wideo: Pajacyki",
                                          command=lambda: self.change_source("resources/jumpingjack.mp4", "jump"),
                                          fg_color="#D81B60", hover_color="#AD1457", height=50,
                                          font=ctk.CTkFont(size=16))
        self.btn_jump_vid.grid(row=3, column=0, padx=20, pady=5, sticky="ew")
        self.source_buttons["jump"] = self.btn_jump_vid

        #wybor cwiczenia
        self.source_label = ctk.CTkLabel(self.sidebar_frame, text="Wybor cwiczenia:", font=ctk.CTkFont(weight="bold"))
        self.source_label.grid(row=4, column=0, padx=20, pady=(10, 5))

        self.btn_jump_vid.grid(row=3, column=0, padx=20, pady=5)
        self.create_button("Plank", "Plank", 5)
        self.create_button("Pajacyki", "JumpingJack", 6)

        self.btn_reset = ctk.CTkButton(self.sidebar_frame, text="Resetuj Wynik",
                                       command=self.reset_stats,fg_color="transparent",border_width=2, text_color="#FF69B4",
                                      border_color="#FF69B4", hover_color="#333333")
        self.btn_reset.grid(row=7, column=0, padx=20, pady=(20, 10), sticky="ew")

        self.btn_exit = ctk.CTkButton(self.sidebar_frame, text="Zakończ", command=self.close_app,
                                      fg_color="transparent", border_width=2, text_color="#FF69B4",
                                      border_color="#FF69B4", hover_color="#333333")
        self.btn_exit.grid(row=8, column=0, padx=20,pady=10, sticky="ew")

        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        #feedback
        self.feedback_label = ctk.CTkLabel(self.main_frame, text="Wybierz cwiczenie",
                                           font=ctk.CTkFont(size=30, weight="bold"),
                                           text_color="#FF69B4")
        self.feedback_label.pack(pady=(20, 20))

        self.video_label = ctk.CTkLabel(self.main_frame, text="")
        self.video_label.pack(expand=True, fill="both")
        #wywolanie petli
        self.update_frame()

    def change_source(self, source,btn_key):
        if self.cap is not None:
            self.cap.release()
        self.cap = cv2.VideoCapture(source)
        for key, btn in self.source_buttons.items():
            if key == btn_key:
                btn.configure(fg_color="#880E4F")
            else:
                btn.configure(fg_color="#D81B60")
        print(f"Zmieniono zrodlo na: {source}")

    def create_button(self, text, exercise_name, row):
        btn = ctk.CTkButton(self.sidebar_frame, text=text,
                            command=lambda: self.change_exercise(exercise_name),
                            fg_color="#D81B60",
                            hover_color="#AD1457",
                            height=50,
                            font=ctk.CTkFont(size=16))
        btn.grid(row=row, column=0, padx=20, pady=10, sticky="ew")
        self.exercise_buttons[exercise_name] = btn
        return btn

    def reset_stats(self):
        self.logic.reps = 0
        self.logic.counter = 0
        self.logic.start_time = None
        if hasattr(self.logic, 'pose'):
            self.logic.pose = False

    def change_exercise(self, exercise_name):
        self.logic.current_exercise = exercise_name
        print(f"Zmieniono cwiczenie na: {exercise_name}")
        self.reset_stats()
        self.is_running = True
        active_color = "#880E4F"
        default_color = "#D81B60"
        for name, btn in self.exercise_buttons.items():
            if name == exercise_name:
                btn.configure(fg_color=active_color)
            else:
                btn.configure(fg_color=default_color)
        self.feedback_label.configure(text="")

    def close_app(self):
        self.cap.release()
        self.destroy()

    def update_frame(self):
        success, frame = self.cap.read()

        if not self.is_running:
            self.after(30,self.update_frame)
            return

        if not success:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            success, frame = self.cap.read()
            if not success:
                self.after(10, self.update_frame)
                return

        try:
            annotated_frame, msg, color_hex = self.logic.video_check(frame)
            self.feedback_label.configure(text=msg, text_color=color_hex)
            # stale wymiary
            # frame = cv2.resize(annotated_frame, (800, 600))
            # frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # _pil = Image.fromarray(frame_rgb)
            # img_tk = ctk.CTkImage(light_image=img_pil, dark_image=img_pil, size=(800, 600))

            # wymiary obliczane
            h, w, _ = annotated_frame.shape
            target_width = 800
            aspect_ratio = w / h
            target_height = int(target_width / aspect_ratio)
            img_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(img_rgb)
            img_tk = ctk.CTkImage(light_image=img_pil, dark_image=img_pil, size=(target_width, target_height))

            self.video_label.configure(image=img_tk)
            self.video_label.image = img_tk

        except Exception as e:
            print(f"Blad w logice: {e}")
            annotated_frame = frame
            msg = "Blad obliczen"
            color_hex = "#FF0000"


        self.after(10, self.update_frame)


if __name__ == "__main__":
    app = Workout_App()
    app.mainloop()