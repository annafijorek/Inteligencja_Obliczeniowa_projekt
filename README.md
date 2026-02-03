## Description

**Workout Assistant** is a computer vision-based fitness application that uses pose estimation to analyze body movement in real time.  
The app can **count Jumping Jacks repetitions** and **measure Plank hold time** using a webcam or video input.

The project combines **YOLO pose detection**, **OpenCV**, and a **CustomTkinter GUI** to provide live feedback on exercise correctness.

---

## How It Works

- The camera frame is processed by a **YOLO pose estimation model**  
- Key body landmarks (joints) are extracted  
- Joint angles and body alignment are calculated  
- Exercise-specific logic evaluates:  
  - posture correctness  
  - repetition timing  
  - body visibility  
- Feedback is displayed live in the UI

---

## Exercises

### Plank

**Measures time spent in correct plank position**  

**Checks:**  
- straight body line  
- correct elbow angle (~90°)  
- horizontal body alignment  
- hips not touching the floor  

### Jumping Jacks

**Counts repetitions within a time limit. Invalid reps reset the counter**  

**Detects:**  
- hands raised above head  
- legs spread wider than shoulders  

---

## Tech Stack

- Python 3.13  
- Ultralytics YOLO (Pose Model)  
- OpenCV  
- NumPy  
- CustomTkinter  

---

## How to Use

1. **Choose video source**  
   - Camera – if you want to train by yourself  
   - Video: Plank / Jumping Jack – to see demo  

   <p align="center">
     <img src="https://github.com/user-attachments/assets/d09fe05a-cdd4-4b7d-bea4-92aceb01e65b" width="800" />
   </p>

2. **Choose exercise**  
   You can change your choice at any time during your workout  

3. **During workout you will see feedback**  

4. **Plank:**  
   - App measures how long you are able to maintain a correct plank position  

   <p align="center">
     <img src="https://github.com/user-attachments/assets/b4d9e7c6-dcc7-464f-8dcd-cd40de39827b" width="800" />
   </p>

   - If the position becomes incorrect, the application will notify you and restart the timer  

   <p align="center">
     <img src="https://github.com/user-attachments/assets/23a01038-9af3-4fa9-b437-4ae6aa9be58c" width="800" />
   </p>

5. **Jumping Jack:**  
   - App tracks and counts correctly performed jumping jack repetitions  

   <p align="center">
     <img src="https://github.com/user-attachments/assets/b88c8219-e6a4-4064-9b88-ad5587226837" width="800" />
   </p>

   - If a jumping jack is performed incorrectly, the counter is reset
