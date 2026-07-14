# DOTA 2 PUSHUP / SHOULDER PRESS TRACKER

A computer vision program that detects when you die in a game and forces you to complete pushups or shoulder presses.

"We either can be a smart team or a strong team" - My highschool football coach

<img width="300" height="251" alt="demotest" src="https://github.com/user-attachments/assets/e05b39ef-7dcf-4607-9e09-cd59e4a7f11d" />

## Features

- Select a screen region to monitor
- Detect game deaths using pixel changes
- Track pushups using MediaPipe pose detection
- Require a set number of pushups / shoulder presses after each death

## Repository Installation

git clone <https://github.com/clindama/VideogameWorkout>

pip install -r requirements.txt

python main.py

## Usage

Pretty much only designed for Dota 2.

Boot up a Dota 2 match and select the region of your character. 

Click start tracking.

Once you die in the game, it will force you to do push-ups based on your webcam tracking you.

You can also do a shoulder press movement if you don't want the camera on the floor. 

Able to track total stats based on each user.

Each death adds another total pushup to complete. 1 death 1 pushup, 2 deaths 2 pushups etc.

## Demo Video

https://youtu.be/EQkhTtRvPOc
