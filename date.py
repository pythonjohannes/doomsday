import calendar

num_to_weekday = {
		0: "Söndag",
		1: "Måndag",
		2: "Tisdag",
		3: "Onsdag",
		4: "Torsdag",
		5: "Fredag",
		6: "Lördag",

	}

num_to_month = {
	1: "Januari",
	2: "Februari",
	3: "Mars",
	4: "April",
	5: "Maj",
	6: "Juni",
	7: "Juli",
	8: "Augusti",
	9: "September",
	10: "Oktober",
	11: "November",
	12: "December",

}


class Date:
	def __init__(self, year, month, day):
		self.year = year
		self.month = month
		self.day = day
		self.doomsday = self.get_doomsday()
		self.doomsday_text = num_to_weekday[self.doomsday]
		self.weekday = self.find_weekday()


	def date_stringed(self):
		if self.year == 2022:
			return f"{self.day} {num_to_month[self.month]}"
		else:
			return f"{self.day} {num_to_month[self.month]} {self.year}"

	def get_doomsday(self):
		years_from_1700 = self.year - 1700
		leap_years = years_from_1700 // 4
		times_centerie_without_leap = 0
		for year in range(1701, self.year):
			if year % 100 == 0 and year % 400 != 0:
				times_centerie_without_leap += 1
		return (years_from_1700 + leap_years - times_centerie_without_leap) % 7

	def find_weekday(self):
		doomsdays = {
			1: 3,
			2: 14,
			3: 14,
			4: 4,
			5: 9,
			6: 6,
			7: 11,
			8: 8,
			9: 5,
			10: 10,
			11: 7,
			12: 12
		}
		#find out if year is a leap year, if it is then the doomsdays for january and february needs to be updated
		if self.year % 4 == 0: #leap year
			if self.year % 100 == 0 and self.year % 400 != 0: #every 4th year that is also a new centery is not a leap year unless it's divisable by 400
				pass
			else:
				doomsdays[1] = 4
				doomsdays[2] = 15

		months_doomsday = doomsdays[self.month]
		if months_doomsday > self.day + self.doomsday:
			self.doomsday += 14
		weekday_num = self.day + self.doomsday - months_doomsday
		weekday = num_to_weekday[weekday_num % 7]
		return weekday