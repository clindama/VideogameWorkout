
# Game Pushup Tracker

A computer vision program that detects when you die in a game and forces you to complete pushups.

## Features

- Select a screen region to monitor
- Detect game deaths using pixel changes
- Track pushups using MediaPipe pose detection
- Require a set number of pushups after each death

## Repository Installation

git clone <https://github.com/clindama/VideogameWorkout>

pip install -r requirements.txt

python main.py

## Usage

Pretty much only designed for Dota 2.

 Boot up a Dota 2 match and select the region of your character. 

Click start tracking 

Once you die in the game, it will force you to do push-ups based on your webcam tracking you.

You can also do a shoulder press movement if you don't want the camera on the floor. 

Able to track total stats based on each user

## Demo Video

https://youtu.be/EQkhTtRvPOc
