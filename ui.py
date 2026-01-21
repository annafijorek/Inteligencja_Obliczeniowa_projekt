import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
from yolo_script import pilates_logic

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")


class PilatesApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Workout Assistant")
        self.geometry("1200x800")

        self.logic = pilates_logic()

        self.cap = cv2.VideoCapture(0)
        # self.cap = cv2.VideoCapture("video1.mp4") #nagranie z pliku

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Pilates AI", font=ctk.CTkFont(size=24, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.btn_plank = self.create_pink_button("Plank", "Plank", 1)
        self.btn_warrior = self.create_pink_button("Warrior II", "Warrior II", 2)
        self.btn_bird = self.create_pink_button("Bird Dog", "Bird Dog", 3)

        self.btn_exit = ctk.CTkButton(self.sidebar_frame, text="Zakończ", command=self.close_app,
                                      fg_color="transparent", border_width=2, text_color="#FF69B4",
                                      border_color="#FF69B4", hover_color="#333333")
        self.btn_exit.grid(row=6, column=0, padx=20, pady=20)

        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        #feedback
        self.feedback_label = ctk.CTkLabel(self.main_frame, text="Wybierz ćwiczenie...",
                                           font=ctk.CTkFont(size=30, weight="bold"),
                                           text_color="#FF69B4")
        self.feedback_label.pack(pady=(0, 20))

        self.video_label = ctk.CTkLabel(self.main_frame, text="")
        self.video_label.pack(expand=True, fill="both")

        #wywolanie petli
        self.update_frame()

    def create_pink_button(self, text, exercise_name, row):
        btn = ctk.CTkButton(self.sidebar_frame, text=text,
                            command=lambda: self.change_exercise(exercise_name),
                            fg_color="#D81B60",
                            hover_color="#AD1457",
                            height=50,
                            font=ctk.CTkFont(size=16))
        btn.grid(row=row, column=0, padx=20, pady=10, sticky="ew")
        return btn

    def change_exercise(self, exercise_name):
        self.logic.current_exercise = exercise_name
        print(f"Zmieniono cwiczenie na: {exercise_name}")

        self.feedback_label.configure(text=f"Tryb: {exercise_name}", text_color="#FF69B4")

    def close_app(self):
        self.cap.release()
        self.destroy()

    def update_frame(self):
        success, frame = self.cap.read()

        if not success:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            success, frame = self.cap.read()
            if not success:
                self.after(10, self.update_frame)
                return

        try:
            annotated_frame, msg, color_hex = self.logic.video_check(frame)
        except Exception as e:
            print(f"Blad w logice: {e}")
            annotated_frame = frame
            msg = "Blad obliczen"
            color_hex = "#FF0000"


        if self.feedback_label.cget("text") != msg:
            self.feedback_label.configure(text=msg, text_color=color_hex)


        frame = cv2.resize(annotated_frame, (800, 600))
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(frame_rgb)
        img_tk = ctk.CTkImage(light_image=img_pil, dark_image=img_pil, size=(800, 600))

        self.video_label.configure(image=img_tk)
        self.video_label.image = img_tk

        self.after(10, self.update_frame)


if __name__ == "__main__":
    app = PilatesApp()
    app.mainloop()