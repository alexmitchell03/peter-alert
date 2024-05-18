import tkinter as tk
import signal
import sys
import random

def exit_program():
	print(" Exiting...")
	if scheduled_popup_id is not None:  # cancel the scheduled popup
		root.after_cancel(scheduled_popup_id)
	if top:  # destroy the popup window if it is open
		top.destroy()
	root.destroy()
	sys.exit(0)

signal.signal(signal.SIGINT, exit_program)
top = None
popup_open = False

interval_options = {
	"5 seconds": 5000,
	"30 seconds": 30000,
	"1 minute": 60000,
	"5 minutes": 300000,
	"30 minutes": 1800000
}


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
		top.configure(bg='lightblue')

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
		image_label = tk.Label(top, image=img, bg='lightblue')
		image_label.pack()

		ok_button = tk.Button(top, text="OK", command=dismiss_popup, bg='white')
		ok_button.pack()
		keep_on_top(top)

	# schedule next popup after 1000ms (1 second) (OLD)
	# schedule next popup after 300000ms (5 minutes)
	# root.after(300000, show_popup)


def center_window(control_win, width=200, height=200):
	screen_width = control_win.winfo_screenwidth()
	screen_height = control_win.winfo_screenheight()
	x_cordinate = int((screen_width/2) - (width/2))
	y_cordinate = int((screen_height/2) - (height/2))
	control_win.geometry(f"{width}x{height}+{x_cordinate}+{y_cordinate}")


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


scheduled_popup_id = None

def start_alerts():
	global alert_interval, scheduled_popup_id, start_button
	interval = interval_options[alert_interval.get()]
	
	if scheduled_popup_id is None:
		start_button['state'] = 'disabled'
		scheduled_popup_id = root.after(interval, start_alerts)
		show_popup()


def stop_alerts():
	global scheduled_popup_id, start_button
	if scheduled_popup_id is not None:
		root.after_cancel(scheduled_popup_id)
		scheduled_popup_id = None
		start_button['state'] = 'normal'


def controller_window():
	global alert_interval, scheduled_popup_id, start_button
	control_win = tk.Toplevel(root)
	control_win.title("Alert Control")
	control_win.configure(bg='lightblue')
	control_win.protocol("WM_DELETE_WINDOW", exit_program)

	center_window(control_win)
	
	main_label = tk.Label(control_win, text="Peter Alert", bg='lightblue', font=(16))
	main_label.pack(pady=10)

	# dropdown for selecting alert interval
	dropdown_label = tk.Label(control_win, text="Choose alert interval:", bg='lightblue')
	dropdown_label.pack()

	dropdown = tk.OptionMenu(control_win, alert_interval, *interval_options.keys())
	dropdown.pack()

	start_button = tk.Button(control_win, text="Start Alerts", command=start_alerts, bg='green', fg='white')
	start_button.pack(pady=5)

	stop_button = tk.Button(control_win, text="Stop Alerts", command=stop_alerts, bg='red', fg='white')
	stop_button.pack(pady=5)


# create the root tk window
root = tk.Tk()

root.withdraw()
root.update() 

alert_interval = tk.StringVar(value="5 minutes")

img = tk.PhotoImage(file='peter3.png')

# show_popup()
controller_window()

root.mainloop()