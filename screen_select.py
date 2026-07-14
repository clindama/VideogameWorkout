import tkinter as tk

def select_region():
    start_x = 0
    start_y = 0
    end_x = 0
    end_y = 0

    def mouse_down(event):
        nonlocal start_x, start_y
        start_x = event.x
        start_y = event.y

    def mouse_up(event):
        nonlocal end_x, end_y
        end_x = event.x
        end_y = event.y
        # Close ONLY this selection window, not the whole app
        overlay.destroy() 

    # 1. Use Toplevel instead of Tk() so it links nicely with your main GUI
    overlay = tk.Toplevel()
    
    overlay.attributes("-fullscreen", True)
    overlay.attributes("-alpha", 0.3)
    
    # 2. Make sure this window sits on top of everything else
    overlay.lift()
    overlay.attributes("-topmost", True)

    canvas = tk.Canvas(overlay)
    canvas.pack(fill="both", expand=True)

    canvas.bind("<ButtonPress-1>", mouse_down)
    canvas.bind("<ButtonRelease-1>", mouse_up)

    # 3. CRITICAL: Instead of mainloop(), tell the script to pause right 
    # here and wait specifically until *this* overlay window is destroyed.
    overlay.wait_window()

    # Once overlay.destroy() runs in mouse_up, code execution resumes down here
    region = {
        "left": min(start_x, end_x),
        "top": min(start_y, end_y),
        "width": abs(end_x - start_x),
        "height": abs(end_y - start_y)
    }

    return region