import tkinter as tk
import signal
import sys
import random

def signal_handler(sig, frame):
	print(" Exiting...")
	sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
top = None
popup_open = False


def start_move(event):
	global x, y
	x = event.x
	y = event.y


def on_move(event):
	global x, y, top
	deltax = event.x - x
	deltay = event.y - y
	x0 = top.winfo_x() + deltax
	y0 = top.winfo_y() + deltay
	top.geometry(f"+{x0}+{y0}")


def dismiss_popup():
	global popup_open, top
	if top:
		top.destroy()
		top = None
	popup_open = False


def show_popup():
	global popup_open, top
	if not popup_open:
		popup_open = True

		top = tk.Toplevel(root)
		top.overrideredirect(True)
		top.attributes('-topmost', True)
		top.configure(bg='light blue')

		# create widgets
		title_bar = tk.Frame(top, bg='white', relief='raised', bd=2)
		title_bar.pack(fill='x')
		title_label = tk.Label(title_bar, text='Peter Alert', bg='white')
		title_label.pack(side='left', padx=10)
		window_close_button = tk.Button(title_bar, text='X')
		window_close_button.pack(side='right')

		# bind window movement
		title_bar.bind('<Button-1>', start_move)
		title_bar.bind('<B1-Motion>', on_move)

		# place window
		random_pos()

		# update window to make sure it is rendered, before setting the grab
		top.update_idletasks()  # updates the window geometry
		top.grab_set_global()   # set the global grab

		# create and place image
		image_label = tk.Label(top, image=img, bg='light blue')
		image_label.pack()

		ok_button = tk.Button(top, text="OK", command=dismiss_popup, bg='white')
		ok_button.pack()
		keep_on_top(top)

	# schedule next popup after 1000ms (1 second) (OLD)
	# schedule next popup after 300000ms (5 minutes)
	root.after(300000, show_popup)


def center_window(width=250, height=120):
	global top
	screen_width = root.winfo_screenwidth()
	screen_height = root.winfo_screenheight()
	x_cordinate = int((screen_width/2) - (width/2))
	y_cordinate = int((screen_height/2) - (height/2))
	top.geometry(f"{width}x{height}+{x_cordinate}+{y_cordinate}")


def keep_on_top(window):
	# attempt to refocus the window every 100 ms
	window.attributes('-topmost', True)
	window.after(100, lambda: keep_on_top(window))


def random_pos(width=250, height=120):
	global top
	screen_width = root.winfo_screenwidth()
	screen_height = root.winfo_screenheight()
	x_coordinate = random.randint(0, screen_width - width)
	y_coordinate = random.randint(0, screen_height - height)
	top.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")



# create the root tk window
root = tk.Tk()

root.withdraw()
root.update() 

img = tk.PhotoImage(file='peter3.png')

show_popup()
root.mainloop()