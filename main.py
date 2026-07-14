import tkinter as tk
import threading
import time

from screen_select import select_region
from death_detector import detect_death
from pushup_tracker import start_pushup_test
from camera_test import camera_preview


# -----------------------------
# Session stats
# -----------------------------
total_pushups = 0
deaths = 0

running = True

region = None
monitoring_started = False
thread_created = False  # Track if the background thread has been created yet

# Session tracking
session_start = time.time()


from database import (
    create_database,
    get_or_create_user,
    save_session,
    get_user_stats
)

create_database()

user_id = get_or_create_user()



# -----------------------------
# Save Session Data Helper
# -----------------------------
def save_current_progress():
    global session_start, deaths, total_pushups

    duration = int(
        time.time() - session_start
    )

    print("Saving session data...")

    save_session(
        user_id,
        deaths,
        total_pushups,
        duration
    )

    print("Session saved successfully!")
    
    # Reset timers and current counts so a brand new session block saves cleanly if resumed
    session_start = time.time()
    deaths = 0
    total_pushups = 0



# -----------------------------
# Update GUI
# -----------------------------
def update_display():

    pushup_label.config(
        text=f"Total Pushups: {total_pushups}"
    )

    death_label.config(
        text=f"Deaths: {deaths}"
    )

    if running:
        root.after(500, update_display)



# -----------------------------
# Quit program
# -----------------------------
def quit_program():

    global running

    # If they are currently active, save whatever progress remains
    if monitoring_started:
        save_current_progress()

    running = False

    root.destroy()



# -----------------------------
# Select death region
# -----------------------------
def select_death_region():

    global region


    print("Selecting death region...")


    region = select_region()


    print("Region selected:")
    print(region)



# -----------------------------
# Show Stats Window
# -----------------------------
def show_stats():
    db_stats = get_user_stats(user_id) 
    
    total_p = db_stats[0] if db_stats[0] is not None else 0
    total_d = db_stats[1] if db_stats[1] is not None else 0
    total_sec = db_stats[2] if db_stats[2] is not None else 0
    
    total_min = round(total_sec / 60, 1)
    
    stats_window = tk.Toplevel(root)
    stats_window.title("User Lifetime Stats")
    stats_window.geometry("250x220")
    stats_window.lift()
    stats_window.attributes("-topmost", True)
    
    tk.Label(stats_window, text="Lifetime History", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Label(stats_window, text=f"Total Pushups: {total_p}", font=("Arial", 11)).pack(pady=5)
    tk.Label(stats_window, text=f"Total Deaths: {total_d}", font=("Arial", 11)).pack(pady=5)
    tk.Label(stats_window, text=f"Time Tracked: {total_min} mins", font=("Arial", 11)).pack(pady=5)
    
    tk.Button(stats_window, text="Close", command=stats_window.destroy, width=10).pack(pady=15)



# -----------------------------
# Start monitoring
# -----------------------------
def start_monitoring():

    global monitoring_started
    global thread_created
    global session_start


    if region is None:

        print("Please select a region first")

        return


    if monitoring_started:

        print("Already monitoring")

        return


    monitoring_started = True
    
    # Freshly reset the session timer block whenever tracking is newly kicked off
    session_start = time.time()


    # Only create the thread once. If it already exists, just unpause it!
    if not thread_created:
        print("Starting death detector thread...")
        thread = threading.Thread(
            target=game_loop,
            daemon=True
        )
        thread.start()
        thread_created = True
    else:
        print("Resuming death detector...")



# -----------------------------
# Stop monitoring
# -----------------------------
def stop_monitoring():

    global monitoring_started

    if not monitoring_started:
        print("Monitoring is not active")
        return

    monitoring_started = False
    print("Monitoring stopped.")
    
    # Save the tracked block data immediately to match the quit behavior
    save_current_progress()



# -----------------------------
# Main detector loop
# -----------------------------
def game_loop():

    global total_pushups
    global deaths
    global region


    print("Watching for death...")


    while running:

        # Only run detection if monitoring flag is active
        if monitoring_started:

            died = detect_death(
                region,
                lambda: running and monitoring_started
            )


            if died and running and monitoring_started:


                deaths += 1


                print("Death detected!")


                # 1 death = pushups
                start_pushup_test(deaths)


                total_pushups += deaths


                print("Back to monitoring")


# -----------------------------
# Create popup window
# -----------------------------
root = tk.Tk()

root.title("Game Pushup Tracker")

root.geometry("300x400")



title = tk.Label(
    root,
    text="Workout Tracker",
    font=("Arial", 16)
)

title.pack(pady=10)



pushup_label = tk.Label(
    root,
    text="Total Pushups: 0",
    font=("Arial", 12)
)

pushup_label.pack()



death_label = tk.Label(
    root,
    text="Deaths: 0",
    font=("Arial", 12)
)

death_label.pack()



# -----------------------------
# Select Region Button
# -----------------------------
select_button = tk.Button(
    root,
    text="Select Death Region",
    command=select_death_region,
    width=20
)

select_button.pack(pady=10)



# -----------------------------
# Start Monitoring Button
# -----------------------------
start_button = tk.Button(
    root,
    text="Start Monitoring",
    command=start_monitoring,
    width=20
)

start_button.pack(pady=10)



# -----------------------------
# Stop Monitoring Button
# -----------------------------
stop_button = tk.Button(
    root,
    text="Stop Monitoring",
    command=stop_monitoring,
    width=20
)

stop_button.pack(pady=10)



# -----------------------------
# Show Stats Button
# -----------------------------
stats_button = tk.Button(
    root,
    text="Show Stats",
    command=show_stats,
    width=20
)
stats_button.pack(pady=10)



quit_button = tk.Button(
    root,
    text="Quit Program",
    command=quit_program,
    width=15
)

quit_button.pack(pady=10)



# -----------------------------
# Startup
# -----------------------------
print("Starting camera test...")


camera_working = camera_preview()


if camera_working:

    print("Camera passed!")


else:

    print("Camera unavailable")

    root.destroy()



# -----------------------------
# Start GUI updates
# -----------------------------
update_display()


root.mainloop()