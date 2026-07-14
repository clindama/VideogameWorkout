import mss
import numpy as np
import time


def detect_death(region, running_check):

    sct = mss.mss()


    # Take starting screenshot
    previous = np.array(
        sct.grab(region)
    )


    while running_check():

        current = np.array(
            sct.grab(region)
        )


        # Compare pixels
        difference = np.abs(
            current.astype(int) -
            previous.astype(int)
        )


        change = np.mean(difference)

        if change > 15:
            print("DEATH DETECTED")
            return True


        previous = current

        time.sleep(0.1)