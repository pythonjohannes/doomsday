import time
from datetime import datetime
import datetime
from tkinter import *
from database import *
from engine import Engine


window = Tk()

canvas = Canvas(width=800, height=570)
x_img = PhotoImage(file="images/x-green.png")
canvas.create_image(400, 300, image=x_img)
canvas.grid(row=0, column=0, columnspan=2, padx=20)
engine = Engine(canvas, window)

window.bind("<space>", engine.show_weekday_answer)
window.mainloop()









# print("SCOREBOARD")
# for stat in db.session.query(Stats).all():
# 	print(stat.date,"|", stat.time,"|", stat.time_per_date, end="\n\n")

import pandas
from tabulate import tabulate




def present_date():
	global canvas_text
	global weekday
	global rounds
	global count_right
	global start
	rounds += 1
	if rounds == 2:
		score = f"{count_right}/{rounds-1}"
		canvas.delete(canvas_text)
		canvas.create_text(400,190, text=f"Finished! Score: {score}", font=("Arial", 50), fill="white")
		time_taken = int(time.time() - start)
		time_date = int(time_taken/(rounds-1))
		time_taken = f"{time_taken // 60}min {time_taken%60}sec"
		canvas.create_text(400, 270, text=f"Time: {time_taken}", font=("Arial", 40),
						   fill="white")
		canvas.create_text(400, 330, text=f"Per Date: {time_date} sec", font=("Arial", 35),
						   fill="white")

		now = datetime.datetime.now()
		date_now = now.strftime("%d/%m/%y")
		new_run = Stats(
				date= date_now,
				time= time_taken,
				time_per_date=time_date
			)
		db.session.add(new_run)
		db.session.commit()
		scoreboard = Button(text="Scoreboard")

	else:
		right_btn["state"] = "disabled"
		wrong_btn["state"] = "disabled"
		canvas.delete(canvas_text)
		date = engine.generate_random_date()

		start = time.time()
		canvas_text = canvas.create_text(400, 287, text=f"{date.date_stringed()}", font=("Arial", 50), fill="white")


def show_answer(*args):
	global canvas_text
	right_btn["state"] = "active"
	wrong_btn["state"] = "active"
	canvas.delete(canvas_text)
	canvas_text = canvas.create_text(400,287,text=f"{weekday}", font=("Arial",50), fill="white")


def right():
	global count_right
	count_right +=1
	present_date()




#
# df = pandas.read_sql("stats", "sqlite:///stats.db")
# df.style.hide_index()
# print(tabulate(df[["date", "time", "time_per_date"]], headers="keys", tablefmt='psql', showindex=False), end="\n\n\n")
#
# game_on = True
# while game_on:
# 	num_dates = 10
# 	dates = generate_random_dates(num_dates)
#
# 	start = time.time()
# 	for date in dates:
# 		doomsday = get_doomsday(date)
# 		weekday = find_weekday(date, doomsday)
# 		print(f"date: {date.date_stringed()}")
# 		input("Press enter to get answer: ")
# 		print(f"Right answer: {weekday}", end="\n\n")
#
#
# 	time_taken = int(time.time()-start)
# 	time_date = int(time_taken/num_dates)
# 	time_taken = f"{time_taken // 60}min {time_taken%60}sec"
# 	print(time_taken)
# 	print(f"Time per date: {time_date}")
#
# 	now = datetime.datetime.now()
# 	date_now = now.strftime("%D")
#
# 	new_run = Stats(
# 		date= date_now,
# 		time= time_taken,
# 		time_per_date=time_date
# 	)
# 	db.session.add(new_run)
# 	db.session.commit()
#
# 	if input("Go again? y/n: ") == "n":
# 		game_on = False
# tk.mainloop()




