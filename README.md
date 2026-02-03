##Description##
Workout Assistant is a computer vision-based fitness application that uses pose estimation to analyze body movement in real time.
The app can count Jumping Jacks repetitions and measure Plank hold time using a webcam or video input.

The project combines YOLO pose detection, OpenCV, and a CustomTkinter GUI to provide live feedback on exercise correctness.


##How It Works##
- The camera frame is processed by a YOLO pose estimation model
- Key body landmarks (joints) are extracted
- Joint angles and body alignment are calculated
- Exercise-specific logic evaluates:
    -posture correctness
    -repetition timing
    -body visibility
- Feedback is displayed live in the UI


##Exercises##

#Plank#
Measures time spent in correct plank position
Checks:
- straight body line
- correct elbow angle (~90°)
- horizontal body alignment
- hips not touching the floor

#Jumping Jacks#
Counts repetitions within a time limit. Invalid reps reset the counter
Detects:
-hands raised above head
-legs spread wider than shoulders


##Tech Stack##
-Python 3.13
-Ultralytics YOLO (Pose Model)
-OpenCV
-NumPy
-CustomTkinter


##How to use##
1. Choose video source
   -camera- if you want to train by yourself
   -wideo: plank/jumping jack - to see demo    
2. Choose excercise
<img width="1269" height="678" alt="Zrzut ekranu 2026-02-03 003833" src="https://github.com/user-attachments/assets/d09fe05a-cdd4-4b7d-bea4-92aceb01e65b" />    
3. You can change your choice in any time during your workout
4. During workout you will see feedback
5. Plank: app measures how long you are able to maintain a correct plank position
<img width="1212" height="901" alt="Zrzut ekranu 2026-02-03 004249" src="https://github.com/user-attachments/assets/b4d9e7c6-dcc7-464f-8dcd-cd40de39827b" />
If the position becomes incorrect, the application will notify you and restart the timer
<img width="1110" height="837" alt="Zrzut ekranu 2026-02-03 004706" src="https://github.com/user-attachments/assets/23a01038-9af3-4fa9-b437-4ae6aa9be58c" />
5. Jumping Jack: app tracks and counts correctly performed jumping jack repetitions
<img width="1101" height="865" alt="Zrzut ekranu 2026-02-03 004423" src="https://github.com/user-attachments/assets/b88c8219-e6a4-4064-9b88-ad5587226837" />
If a jumping jack is performed incorrectly, the counter is reset

