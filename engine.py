import time
from datetime import datetime
from random import randint, choice
from date import Date
from tkinter import *
from database import *
from PIL import Image,ImageTk

class Engine():
	NUMER_OF_ROUNDS = 10
	CURRENT_YEAR = 2022  # om man ändrar denna ändra också i date.py date_stringed
	def __init__(self, canvas, window):
		self.canvas = canvas
		self.window = window
		self.delete_btns = []
		self.choose_mode()

	def choose_mode(self):
		self.img = PhotoImage(file="images/card_back.png")
		self.canvas.create_image(400, 300, image=self.img)
		self.canvas.create_text(390, 130, text="Choose Gamemode", font=("Arial",50))
		self.all_years_btn = Button(text="History, Future\nand now", bg="#E1FC75", font=("Arial", 20), activebackground="#CCCC00",
									 command=self.all_years_mode)
		self.this_year_btn = Button(text="This year\n(2022)", bg="#E1FC75", font=("Arial", 20), activebackground="#CCCC00",
									 command=self.this_year_mode)
		self.only_years_btn = Button(text="Only Years\n(All)", bg="#E1FC75", font=("Arial", 20),
									activebackground="#CCCC00",
									command=self.only_years_mode)
		self.only_years_btn.place(x=350, y=250)
		self.all_years_btn.place(x=100, y=250)
		self.this_year_btn.place(x=550, y=250)
		self.place_user_options()

	def place_user_options(self):
		self.user = StringVar()
		self.user.set("Johannes")
		self.dropdown = OptionMenu(self.window, self.user, "Johannes", "Mats")
		self.dropdown.place(x=5,y=5)

	def start_it(self):
		self.dropdown.place_forget()
		self.this_year_btn.place_forget()
		self.all_years_btn.place_forget()
		self.only_years_btn.place_forget()
		self.canvas.delete("all")
		self.create_game()
		self.create_buttons()
		self.present_date()

	def all_years_mode(self):
		self.mode= "all_years"
		self.start_it()


	def this_year_mode(self):
		self.mode = "this_year"
		self.start_it()

	def only_years_mode(self):
		self.mode = "only_years"
		self.start_it()


	def create_game(self):
		self.img = PhotoImage(file="images/card_back.png")
		self.canvas.create_image(400, 300, image=self.img)
		self.canvas.bind("<Button-1>", self.show_weekday_answer)
		self.canvas_text = ""
		self.count_right = 0
		self.rounds = 0
		self.start = time.time()


	def create_buttons(self):
		self.right_img = PhotoImage(file="images/right.png")
		self.right_btn = Button(image=self.right_img, command=self.right_answer)

		self.wrong_img = PhotoImage(file="images/wrong.png")
		self.wrong_btn = Button(image=self.wrong_img, command=self.present_date)

		self.place_right_wrong_buttons()
		self.btn_state_change("disabled")

	def place_right_wrong_buttons(self):
		self.right_btn.grid(row=1, column=0)
		self.wrong_btn.grid(row=1, column=1, pady=30)

	def btn_state_change(self, state):
		self.right_btn["state"] = state
		self.wrong_btn["state"] = state

	def generate_random_date(self, year=None):
		day = randint(1,28)
		month = randint(1,12)

		#if year hasn't been manually set:
		if not year:
			centrie = choice([1700, 1800, 1900, 1900, 1900, 1900, 1900, 2000, 2000, 1800, 1700])
			year = randint(centrie, centrie+99)
		date = Date(year,month,day)
		return date

	def present_date(self):
		if self.rounds == self.NUMER_OF_ROUNDS:
			self.finish_game()
		else:
			if self.mode == "all_years" or self.mode == "only_years":
				self.date = self.generate_random_date()
			elif self.mode == "this_year":
				self.date = self.generate_random_date(year=self.CURRENT_YEAR)
			self.btn_state_change("disabled")
			self.canvas.delete(self.canvas_text)
			if self.mode == "only_years":
				card_text = self.date.year
			else:
				card_text = self.date.date_stringed()
			self.canvas_text = self.canvas.create_text(400, 287, text=card_text, font=("Arial", 50), fill="white")
			self.rounds += 1

	def show_weekday_answer(self, *args):
		self.btn_state_change("active")
		self.canvas.delete(self.canvas_text)
		if self.mode == "only_years":
			card_text = self.date.doomsday_text
		else:
			card_text = self.date.weekday
		self.canvas_text = self.canvas.create_text(400, 287, text=card_text, font=("Arial", 50), fill="white")

	def right_answer(self):
		self.count_right += 1
		self.present_date()

	def remove_right_wrong_btns(self):
		self.right_btn.grid_forget()
		self.wrong_btn.grid_forget()

	def play_again(self):
		for btn in self.delete_btns:
			btn.place_forget()
		self.canvas.delete("all")
		self.remove_right_wrong_btns()
		self.choose_mode()
		self.canvas.delete(self.finished_text_1, self.finished_text_2, self.finished_text_3)
		self.btn_scoreboard.place_forget()
		self.play_again_btn.place_forget()

	def delete_stat(self, stat):
		db.session.delete(stat)
		db.session.commit()
		self.canvas.delete("all")
		self.img = PhotoImage(file="images/card_back.png")
		self.canvas.create_image(400, 300, image=self.img)
		self.write_scoreboard()


	def write_scoreboard(self):
		self.y = 130
		def write(stat):
			self.canvas.create_text(20, self.y, text=stat.user, font=("Arial", 25), fill="white")
			self.canvas.create_text(140, self.y, text=stat.date, font=("Arial", 25), fill="white")
			self.canvas.create_text(290, self.y, text=stat.result, font=("Arial", 25), fill="white")
			self.canvas.create_text(450, self.y, text=stat.time, font=("Arial", 25), fill="white")
			self.canvas.create_text(625, self.y, text=f"{stat.time_per_date}sec", font=("Arial", 25), fill="white")
			self.btn = Button(text="X", bg="#91c2af", font=("Arial", 12),
									command=lambda st=stat: self.delete_stat(st), fg="#383C39",
									activebackground="#769283")
			self.btn.place(x=740, y=self.y - 15)
			self.delete_btns.append(self.btn)
			self.y += 70

		for btn in self.delete_btns:
			btn.place_forget()
		self.canvas.delete(self.finished_text_1, self.finished_text_2, self.finished_text_3)
		self.btn_scoreboard.place_forget()
		self.play_again_btn.place_forget()

		self.canvas.create_text(140, 80, text="Date", font=("Arial", 25, "underline"), fill="#383C39")
		self.canvas.create_text(290, 80, text="Score", font=("Arial", 25, "underline"), fill="#383C39")
		self.canvas.create_text(450, 80, text="Time", font=("Arial", 25, "underline"), fill="#383C39")
		self.canvas.create_text(625, 80, text="Time/Date", font=("Arial", 25, "underline"), fill="#383C39")
		y= 130
		photo = Image.open("images/x-green.png")
		photo = photo.resize((50,50),Image.ANTIALIAS)
		self.x_img = ImageTk.PhotoImage(photo)
		if self.mode == "all_years":
			for stat in AllYears.query.order_by(AllYears.time_per_date.asc()).limit(5).all():
				write(stat)
		elif self.mode == "this_year":
			for stat in ThisYear.query.order_by(ThisYear.time_per_date.asc()).limit(5).all():
				write(stat)
		elif self.mode == "only_years":
			for stat in OnlyYears.query.order_by(OnlyYears.time_per_date.asc()).limit(5).all():
				write(stat)

		self.play_again_btn = Button(text="Play Again", bg="#96F7B3", font=("Arial", 20), activebackground="#CCCC00",
									 command=self.play_again)
		self.play_again_btn.place(x=350, y=470)

	def finish_game(self):
		self.canvas.unbind("<Button-1>")
		score = f"{self.count_right}/{self.rounds}"
		self.canvas.delete(self.canvas_text)
		self.finished_text_1 = self.canvas.create_text(400, 190, text=f"Finished! Score: {score}", font=("Arial", 50), fill="white")
		time_taken = int(time.time() - self.start)
		time_date = int(time_taken / (self.rounds))
		time_taken_string = f"{time_taken // 60}min {time_taken % 60}sec"
		self.finished_text_2 = self.canvas.create_text(400, 270, text=f"Time: {time_taken_string}", font=("Arial", 40),
								fill="white")
		self.finished_text_3 = self.canvas.create_text(400, 330, text=f"Per Date: {time_date} sec", font=("Arial", 35),
								fill="white")
		now = datetime.now()
		date_now = now.strftime("%d/%m/%y")
		if self.user.get() == "Johannes":
			user_shortend = "J"
		elif self.user.get() == "Mats":
			user_shortend = "M"

		if self.mode == "all_years":
			new_run = AllYears(
			date=date_now,
			time=time_taken_string,
			time_per_date=time_date,
			result = score,
			user = user_shortend
		)
		elif self.mode == "this_year":
			new_run = ThisYear(
			date=date_now,
			time=time_taken_string,
			time_per_date=round(time_taken / (self.rounds),2),
			result = score,
			user=user_shortend
		)
		elif self.mode == "only_years":
			new_run = OnlyYears(
				date=date_now,
				time=time_taken_string,
				time_per_date=round(time_taken / (self.rounds), 2),
				result=score,
				user=user_shortend
			)
		db.session.add(new_run)
		db.session.commit()
		self.btn_scoreboard = Button(text="Scoreboard", bg="#FFFF99", font=("Arial", 25), activebackground="#CCCC00", command=self.write_scoreboard)
		self.btn_scoreboard.place(x=120, y=440)
		self.play_again_btn = Button(text="Play Again", bg="#96F7B3", font=("Arial", 25), activebackground="#CCCC00", command=self.play_again)
		self.play_again_btn.place(x=500, y=440)

		self.remove_right_wrong_btns()


