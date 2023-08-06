# -*- coding: utf-8 -*-
import re  #내장모듈
import time  #내장모듈
import calendar #내장모듈
from datetime import datetime, time, date, timedelta   #내장모듈

import jfinder  # halmoney 모듈

class pynal():
	"""
	시간을 다루기 위한 모듈
	"""
	def __init__(self):
		#기본적으로 날짜의 변환이 필요한 경우는 utc 시간을 기준으로 변경하도록 하겠읍니다
		self.jf = jfinder.jfinder()
		self.var ={}

	def change_any_time_string_to_dt_obj(self, input_string):
		"""
		어떤 시간형이 오더라도 datetime형으로 돌려주는것
		datetime.replace(year=self.year, month=self.month, day=self.day, hour=self.hour, minute=self.minute, second=self.second, microsecond=self.microsecond, tzinfo=self.tzinfo, *, fold=0)
		"""
		result = {}

		result["year"] = 0
		result["mon"] = 0
		result["day"] = 0
		result["hour"] = 0
		result["min"] = 0
		result["sec"] = 0
		result["bellow_sec"] = 0
		result["utc_+-"] = 0
		result["utc_h"] = 0
		result["utc_m"] = 0
		mon_l = ['january','february', 'march', 'april', 'may','june', 'july', 'august', 'september', 'october','november', 'december']
		mon_s = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

		one = (str(input_string).strip()).lower()
		one = one.replace("/", "-")
		one = one.replace("#", "-")
		#print(len(one))

		ymd_sql = []
		#20230301
		if len(one) <= 13:
			#print("len(one) <= 13 ********")
			# "180919 015519"
			if self.jf.search_by_jfsql("[숫자:6~6][공백:1~1][숫자:6~6]", one):
				aaa = self.jf.search_by_jfsql("[숫자:6~6][공백:1~1][숫자:6~6]", one)
				#print(aaa)
				#print(self.jf.change_jfsql_to_resql("[숫자:6~6][공백:1~1][숫자:6~6]"))
				one = one.replace(aaa[0][0], "")
				result["day"] = aaa[0][0][0:2]
				result["mon"] = aaa[0][0][2:4]
				result["year"] = aaa[0][0][4:6]
				result["bellow_sec"] = aaa[0][0][:-6]

				if int(result["year"]) > 50:
					result["year"] = "19"+ result["year"]
				else:
					result["year"] = "20" + result["year"]

			elif 8 <= len(one) <= 10:
				#print(one)
				#2022-03-04
				if self.jf.search_by_jfsql("[숫자:4~4]-[숫자:1~2]-[숫자:1~2]", one):
					aaa = self.jf.search_by_jfsql("[숫자:4~4]-[숫자:1~2]-[숫자:1~2]", one)
					temp = aaa[0][0].split("-")
					one = one.replace(aaa[0][0], "")
					result["year"] = temp[0]
					result["mon"] = temp[1]
					result["day"] = temp[2]
				#02-03-2022
				elif self.jf.search_by_jfsql("[숫자:1~2]-[숫자:1~2]-[숫자:4~4]", one):
					aaa = self.jf.search_by_jfsql("[숫자:1~2]-[숫자:1~2]-[숫자:4~4]", one)
					temp = aaa[0][0].split("-")
					one = one.replace(aaa[0][0], "")
					result["year"] = temp[2]
					result["mon"] = temp[1]
					result["day"] = temp[0]
				#02-03-2022
				elif self.jf.search_by_jfsql("[숫자:1~2]-[숫자:1~2]-[숫자:2~2]", one):
					aaa = self.jf.search_by_jfsql("[숫자:1~2]-[숫자:1~2]-[숫자:2~2]", one)
					temp = aaa[0][0].split("-")
					one = one.replace(aaa[0][0], "")
					result["year"] = temp[2]
					result["mon"] = temp[1]
					result["day"] = temp[0]
				#20220607
				elif self.jf.search_by_jfsql("20[숫자:6~6]", one):
					aaa = self.jf.search_by_jfsql("20[숫자:6~6]", one)
					one = one.replace(aaa[0][0], "")
					result["year"] = aaa[0][0][0:4]
					result["mon"] = aaa[0][0][4:6]
					result["day"] = aaa[0][0][6:8]
		else:
				#print("len(one) > 13 ##########")
				# 2018-03-12
				if self.jf.search_by_jfsql("[숫자:4~4]-[숫자:1~2]-[숫자:1~2]", one) and len(one) > 1:
					aaa = self.jf.search_by_jfsql("[숫자:4~4]-[숫자:1~2]-[숫자:1~2]", one)
					#print("입력형식 ==> 2018-03-12")
					one = one.replace(aaa[0][0], "")
					temp = aaa[0][0].split("-")
					result["year"] = temp[0]
					result["mon"] = temp[1]
					result["day"] = temp[2]

				#3/12/2018
				elif self.jf.search_by_jfsql("[숫자:1~2][-/_:1~1][숫자:1~2][-/_:1~1][숫자:4~4]", one) and len(one) > 1:
					new_sql = self.jf.change_jfsql_to_resql("[숫자:1~2][-/_:1~1][숫자:1~2][-/_:1~1][숫자:4~4]")
					#print("입력형식 ==> 3/12/2018")
					aaa = self.jf.search_all_by_resql(new_sql, one)
					#print("3/12/2018 스타일 ==> ", aaa)
					one = one.replace(aaa[0][0], "")
					temp = aaa[0][0].split("-")
					result["year"] = temp[2]
					if int(temp[0]) >12:
						result["mon"] = temp[1]
						result["day"] = temp[0]
					elif int(temp[1]) >12:
						result["mon"] = temp[0]
						result["day"] = temp[1]
					else:
						result["mon"] = temp[0]
						result["day"] = temp[1]

				# 18/09/19
				elif self.jf.search_by_jfsql("[숫자:2~2][-/_:1~1][숫자:1~2][-/_:1~1][숫자:1~2]", one) and len(one) > 1:
					aaa = self.jf.search_by_jfsql("[숫자:2~2][-/_:1~1][숫자:1~2][-/_:1~1][숫자:1~2]", one)
					#print("18/09/19 형식입니다")
					one = one.replace(aaa[0][0], "")
					temp = aaa[0][0].split("-")
					result["year"] = temp[2]
					if int(temp[0]) >12:
						result["mon"] = temp[1]
						result["day"] = temp[0]
					elif int(temp[1]) >12:
						result["mon"] = temp[0]
						result["day"] = temp[1]
					else:
						result["mon"] = temp[0]
						result["day"] = temp[1]

					if int(result["year"]) > 50:
						result["year"] = "19"+ result["year"]
					else:
						result["year"] = "20" + result["year"]

		#'Jun 28 2018 7:40AM',
		#'Jun 28 2018 at 7:40AM',
		#'September 18, 2017, 22:19:55',
		#'Sun, 05/12/1999, 12:30PM',
		#'Mon, 21 March, 2015',
		#'Tuesday , 6th September, 2017 at 4:30pm'
		if self.jf.search_by_jfsql("[영어:3~9][공백&,:1~3][숫자:1~2][공백&,:1~3][숫자:4~4]", one) and len(one) > 1:
			aaa = self.jf.search_by_jfsql("[영어:3~9][공백&,:1~3][숫자:1~2][공백&,:1~3][숫자:4~4]", one)
			one = one.replace(aaa[0][0], "")
			#print(aaa)
			found_text = aaa[0][0]

			bbb = self.jf.search_by_jfsql("[영어:3~9]", found_text)
			#print(bbb)
			for num in range(len(mon_l)):
				if bbb[0][0] in mon_l[num]:
					result["mon"] = num+1
			found_text = found_text.replace(bbb[0][0], "")
			#print(found_text)


			ccc = self.jf.search_by_jfsql("[숫자:4~4]", found_text)
			result["year"] = ccc[0][0]
			found_text = found_text.replace(ccc[0][0], "")

			ddd = self.jf.search_by_jfsql("[숫자:2~2]", found_text)
			result["day"] = ddd[0][0]

		#	'Mon, 21 March, 2015',
		elif self.jf.search_by_jfsql("[숫자:1~2][공백&,:0~3][영어:3~9][공백&,:0~3][숫자:4~4]", one) and len(one) > 1:
			aaa = self.jf.search_by_jfsql("[숫자:1~2][공백&,:0~3][영어:3~9][공백&,:0~3][숫자:4~4]", one)
			one = one.replace(aaa[0][0], "")
			#print(aaa)
			found_text = aaa[0][0]

			bbb = self.jf.search_by_jfsql("[영어:3~9]", found_text)
			#print(bbb)
			for num in range(len(mon_l)):
				if bbb[0][0] in mon_l[num]:
					result["mon"] = num+1
			found_text = found_text.replace(bbb[0][0], "")
			#print(found_text)


			ccc = self.jf.search_by_jfsql("[숫자:4~4]", found_text)
			result["year"] = ccc[0][0]
			found_text = found_text.replace(ccc[0][0], "")

			ddd = self.jf.search_by_jfsql("[숫자:1~2]", found_text)
			result["day"] = ddd[0][0]

		#	'Tuesday , 6th September, 2017 at 4:30pm'
		elif self.jf.search_by_jfsql("[숫자:1~2][영어:2~3][공백&,:1~3][영어:3~9][공백&,:0~3][숫자:4~4]", one) and len(one) > 1:
			aaa = self.jf.search_by_jfsql("[숫자:1~2][영어:2~3][공백&,:1~3][영어:3~9][공백&,:0~3][숫자:4~4]", one)
			one = one.replace(aaa[0][0], "")
			#print(aaa)
			found_text = aaa[0][0]

			bbb = self.jf.search_by_jfsql("[영어:3~9]", found_text)
			#print(bbb)
			for num in range(len(mon_l)):
				if bbb[0][0] in mon_l[num]:
					result["mon"] = num+1
			found_text = found_text.replace(bbb[0][0], "")
			#print(found_text)

			ccc = self.jf.search_by_jfsql("[숫자:4~4]", found_text)
			result["year"] = ccc[0][0]
			found_text = found_text.replace(ccc[0][0], "")

			ddd = self.jf.search_by_jfsql("[숫자:1~2]", found_text)
			result["day"] = ddd[0][0]

		# 17:08:00
		if self.jf.search_by_jfsql("[숫자:2~2]:[숫자:2~2]:[숫자:2~2]", one) and len(one) > 1:
			aaa = self.jf.search_by_jfsql("[숫자:2~2]:[숫자:2~2]:[숫자:2~2]", one)
			#print(aaa)
			one = one.replace(aaa[0][0], "")
			temp = aaa[0][0].split(":")
			if len(temp) == 2:
				result["hour"] = temp[0]
				result["min"] = temp[1]
			elif len(temp) == 3:
				result["hour"] = temp[0]
				result["min"] = temp[1]
				result["sec"] = temp[2]
			one = one.replace("at", "")
		#7:40AM
		elif self.jf.search_by_jfsql("[숫자:1~2]:[숫자:2~2][공백&apm:2~3]", one) and len(one) > 1:
			aaa = self.jf.search_by_jfsql("[숫자:1~2]:[숫자:2~2][공백&apm:2~3]", one)
			bbb = self.jf.search_by_jfsql("[apm:2~2]", aaa[0][0])
			one = one.replace(aaa[0][0], "")
			#print(aaa, " ====> ", one)
			temp = aaa[0][0].split(":")
			result["hour"] = temp[0]
			result["min"] = temp[1][0:2]

			if bbb == "pm" and int(result["hour"])<= 12:
				result["hour"] = int(result["hour"]) +12

		# +00:00
		if self.jf.search_by_jfsql("[+-:1~1][숫자:2~2]:[숫자:2~2]", one) and len(one) > 1:
			aaa = self.jf.search_by_jfsql("[+-:1~1][숫자:2~2]:[숫자:2~2]", one)
			#print(aaa)
			one = one.replace(aaa[0][0], "")
			temp = aaa[0][0].split(":")
			result["current_+-"] = temp[0][0]
			result["current_h"] = temp[0][1:3]
			result["current_m"] = temp[1]


		if self.jf.search_by_jfsql("\.[숫자:6~6]", one) and len(one) > 1:
			aaa = self.jf.search_by_jfsql("\.[숫자:6~6]", one)
			#print(aaa)
			one = one.replace(aaa[0][0], "")
			# .586525
			# 초단위 이하의 자료
			result["bellow_sec"] = aaa[0][0]

		#여태 걸린것주에 없는 4가지 숫자는 연도로 추측한다
		if self.jf.search_by_jfsql("[숫자:4~4]", one) and len(one) > 1:
			aaa = self.jf.search_by_jfsql("[숫자:4~4]", one)
			#print(aaa)
			one = one.replace(aaa[0][0], "")
			result["year"] = aaa[0][0]


		# 여태 걸린것 없는 2가지 숫자는 날짜로 추측한다
		if self.jf.search_by_jfsql("[숫자:2~2]", one) and len(one) > 1:
			aaa = self.jf.search_by_jfsql("[숫자:2~2]", one)
			#print(aaa)
			one = one.replace(aaa[0][0], "")
			result["day"] = aaa[0][0]

		if self.jf.search_by_jfsql("pm[또는]am", one) and len(one) > 1:
			aaa = self.jf.search_by_jfsql("pm[또는]am", one)
			#print(aaa)
			if aaa[0][0] == "pm" and int(result["hour"]) <= 12:
				result["hour"] = int(result["hour"]) +12

		result["year"] = int(result["year"])
		result["mon"] = int(result["mon"])
		result["day"] = int(result["day"])
		result["hour"] = int(result["hour"])
		result["min"] = int(result["min"])
		result["sec"] = int(result["sec"])

		try:
			result = datetime(result["year"], result["mon"], result["day"], result["hour"], result["min"], result["sec"])
		except:
			result = "error"

		return result

	def change_any_time_style_to_dt_obj(self, input_time):
		"""
		어떤 시간의 형태로된 문자열을 날짜 객체로 만드는 것
		"""
		result = self.check_input_time(input_time)
		return result

	def change_dt_obj_to_str_time_set(self, input_utc=""):
		"""
		입력된 시간에 대한 왠만한 모든 형식의 날짜 표현을 사전형식으로 돌려준다
		"""
		lt = self.check_input_time(input_utc)
		result = {}
		# s는 short, e는 english, l은 long
		result["year_s"] = time.strftime('%y', lt) # 22
		result["year"] = time.strftime('%Y', lt) # 2023
		result["yyyy"] = result["year"]

		result["mon"] = time.strftime('%m', lt) # 1
		result["mm"] = result["mon"]
		result["mon_eng_s"] = time.strftime('%b', lt) #jan
		result["mon_eng_l"] = time.strftime('%B', lt) #january

		result["day_s"] = time.strftime('%d', lt) # 1
		result["d"] = time.strftime('%d', lt) # 1
		result["day"] = time.strftime('%j', lt) #01
		result["dd"] = result["day"]

		result["week"] = time.strftime('%w', lt) # 6
		result["yearweek"] = time.strftime('%W', lt) #34, 1년중에 몇번째 주인지
		result["week_eng_s"] = time.strftime('%a', lt) # mon
		result["week_eng_l"] = time.strftime('%A', lt) #monday

		result["hour_s"] = time.strftime('%I', lt) #1
		result["hour"] = time.strftime('%H', lt) #13

		result["ampm"] = time.strftime('%p', lt)
		result["min"] = time.strftime('%M', lt)
		result["sec"] = time.strftime('%S', lt)
		return result

	def change_dt_obj_to_time_string_as_input_format(self, dt_obj, input_format):
		"""
		dt = datetime.strptime("21/11/06 16:30", "%d/%m/%y %H:%M")
		"""
		result = dt_obj.strptime(input_format)
		return result

	def change_dt_obj_to_timestamp(self, input_time):
		"""
		날짜객체를 timestamp로 만드는 것
		"""
		utf_time  =self.check_input_time(input_time)
		result = utf_time.timestamp()
		return result

	def change_dt_obj_to_ymd_list(self, input_time):
		"""
		날짜객체를 년월일의 리스트로 돌려주는 것
		"""
		utc_time = self.check_input_time(input_time)
		utc_str = self.change_dt_obj_to_str_time_set(utc_time)
		result = [utc_str["yyyy"], utc_str["mm"], utc_str["dd"]]
		return result

	def change_hmdlist_to_sec(self,input_list=[0,0,1]):
		"""
		몇년 몇월 몇일을 초로 바꾸는 것
		입력형태 : [몇년, 몇월, 몇일]
		현재일자를 기준으로
		월은 30일 기준으로 계산한다
		기준날짜에서 계산을 하는 것이다
		"""
		total_sec = int(input_list[0]) *60*60*24*365  + int(input_list[1]) *60*60*24*30 + int(input_list[2])*60*60*24
		return total_sec

	def change_hms_list_to_sec(self, input_data=""):
		"""
		hmslist : [시, 분, 초]
		input_data = "14:06:23"
		출력값 : 초
		입력값으로 온 시분초를 초로 계산한것
		"""
		re_compile = re.compile("\d+")
		result = re_compile.findall(input_data)
		total_sec = int(result[0]) * 3600 + int(result[1]) * 60 + int(result[2])
		return total_sec

	def change_hmslist_to_sec(self, input_data=""):
		"""
		hmslist : [시, 분, 초]
		출력값 : 초, 입력값으로 온 시분초를 초로 계산한것
		"""
		total_sec = int(input_data[0]) * 3600 + int(input_data[1]) * 60 + int(input_data[2])
		return total_sec

	def change_input_time_n_format_to_dt_obj(self, input_time, input_format):
		"""
		입력한 시간 문자열과 문자열의 형식을 넣어주면 datetime객체를 만들어 준다
		날짜와 시간(datetime) -> 문자열로 : strftime
		날짜와 시간 형식의 문자열을 -> datetime으로 : strptime
		"""
		dt_obj =  datetime.strptime(input_time, input_format)
		return dt_obj

	def change_input_time_to_utc_format(self, input_time, input_format):
		"""
		입력시간을 utc로 바꾸는 것
		"""
		cheked_input_time = self.check_input_time(input_time)
		result = time.strptime(cheked_input_time, input_format)
		return result

	def change_input_time_to_ymd_style(self, input_time, connect_str="-"):
		"""
		입력시간을 년월일을 특수 문자로 연결하여 돌려주는 것
		"""
		utc_time = self.check_input_time(input_time)
		utc_str = self.change_dt_obj_to_str_time_set(utc_time)
		result = utc_str["yyyy"] + connect_str + utc_str["mm"] + connect_str + utc_str["dd"]
		return result

	def change_iso_format_string_to_dt_obj(self, input_time):
		"""
		datetime.isoformat('2011-11-04 00:05:23.283+00:00')
		"""
		result = datetime.isoformat(input_time)
		return result

	def change_sec_to_dhms(self, input_data):
		"""
		초를 날자로 계산해 주는것
		입력값 : 1000초
		출력값 : 2일3시간10분30초
		dhms : day-hour-minute-sec
		"""
		nalsu = int(input_data)/(60*60*24)
		return nalsu


	def change_sec_to_dhms_list(self, input_data=""):
		"""
		초를 날자로 계산해 주는것
		입력값 : 1000초
		출력값 : 2일3시간10분30초
		dhms : day-hour-minute-sec
		"""
		step_1 = divmod(int(input_data), 60)
		step_2 = divmod(step_1[0], 60)
		day = int(input_data) / (60 * 60 * 24)
		result = [day, step_2[0], step_2[1], step_1[1]]
		return result

	def change_sec_to_hms(self, input_data=""):
		"""
		초로 넘어온 자료를 기간으로 돌려주는 것
		입력값 : 123456
		"""
		step_1 = divmod(int(input_data), 60)
		step_2 = divmod(step_1[0], 60)
		final_result = [step_2[0], step_2[1], step_1[1]]
		return final_result


	def change_set_item_by_list(self, input_set, input_list2d):
		"""
		input_list = [["변경전자료1", "변경후자료2"], ["변경전자료11", "변경후자료22"], ]
		"""
		for list_1d in input_list2d:
			input_set.discard(list_1d[0])
			input_set.add(list_1d[1])
		return input_set

	def change_timestamp_to_utc(self, input_time):
		"""
		숫자형으로된 시간을 utc로 바꾸는 것
		"""
		result = time.gmtime(input_time)
		return result

	def change_utc_timestamp_to_dt_obj(self, input_timestamp):
		"""
		입력값 : utf시간숫자, 1640995200.0 또는 ""
		날짜객체로 만들어 주는 것
		"""
		result = datetime.fromtimestamp(input_timestamp)
		return result

	def change_utftime_to_daylist (self, input_data=""):
		"""
		입력값 : utf시간숫자, 1640995200.0 또는 ""
		일 -----> ['05']
		닞은숫자 -> 많은글자 순으로 정리
		"""
		utf_local_time = self.check_input_time(input_data)
		day = time.strftime('%d', utf_local_time)
		day_l = time.strftime('%j', utf_local_time)
		result = [day, day_l]
		return result

	def change_utftime_to_hourlist (self, input_data=""):
		"""
		입력값 : utf시간숫자, 1640995200.0 또는 ""
		시 -----> ['10', '22']
		닞은숫자 -> 많은글자 순으로 정리
		"""
		utf_local_time = self.check_input_time(input_data)
		hour = time.strftime('%I', utf_local_time)
		hour_l = time.strftime('%H', utf_local_time)
		result = [hour, hour_l]
		return result

	def change_utftime_to_minlist (self, input_data=""):
		"""
		입력값 : utf시간숫자, 1640995200.0 또는 ""
		분 -----> ['07']
		닞은숫자 -> 많은글자 순으로 정리
		"""
		utf_local_time = self.check_input_time(input_data)
		min = time.strftime('%M', utf_local_time)
		result = [min]
		return result

	def change_utftime_to_monthlist (self, input_data=""):
		"""
		입력값 : utf시간숫자, 1640995200.0 또는 ""
		월 -----> ['04', Apr, April]
		닞은숫자 -> 많은글자 순으로 정리
		"""
		utf_local_time = self.check_input_time(input_data)
		mon = time.strftime('%m', utf_local_time)
		mon_e = time.strftime('%b', utf_local_time)
		mon_e_l = time.strftime('%B', utf_local_time)
		result = [mon, mon_e, mon_e_l]
		return result

	def change_utftime_to_seclist(self, input_data=""):
		"""
		입력값 : utf시간숫자, 1640995200.0 또는 ""
		초 -----> ['48']
		닞은숫자 -> 많은글자 순으로 정리
		"""
		utf_local_time = self.check_input_time(input_data)
		sec = time.strftime('%S', utf_local_time)
		result = [sec]
		return result

	def change_utftime_to_weeklist(self, input_data=""):
		"""
		입력값 : utf시간숫자, 1640995200.0 또는 ""
		주 -----> ['5', '13', 'Fri', 'Friday']
		닞은숫자 -> 많은글자 순으로 정리
		"""
		utf_local_time = self.check_input_time(input_data)
		week_no = time.strftime('%w', utf_local_time)
		yearweek_no = time.strftime('%W', utf_local_time)
		week_e = time.strftime('%a', utf_local_time)
		week_e_l = time.strftime('%A', utf_local_time)
		result = [week_no, yearweek_no, week_e, week_e_l]
		return result

	def change_utftime_to_weekno(self, input_data=""):
		"""
		시간이 들어온면
		입력값 : 년도, 위크번호
		한 주의 시작은 '월'요일 부터이다
		"""
		lt = self.check_input_time(input_data)
		result = time.strftime('%W', lt)  # 34, 1년중에 몇번째 주인지
		return result


	def change_utftime_to_yearlist(self, input_data=""):
		"""
		년 -----> ['22', '2022']
		닞은숫자 -> 많은글자 순으로 정리
		"""
		utf_local_time = self.check_input_time(input_data)
		year_s = time.strftime('%y', utf_local_time)
		year = time.strftime('%Y', utf_local_time)
		result = [year_s, year]
		return result

	def change_utftime_to_ymd_dash(self, input_data=""):
		"""
		utc를 2023--2-2형태로 돌려주는 것
		"""
		lt = self.change_any_time_string_to_dt_obj(input_data)
		result = lt.format("YYYY-MM-DD")
		return result

	def change_ymd_list_to_dt_obj(self, input_ymd):
		"""
		datetime객체는 최소한 년/월/일은 들어가야 생성된다
		dt = datetime.strptime("21/11/06 16:30", "%d/%m/%y %H:%M")
		"""
		dt_obj =  self.check_input_time(input_ymd)
		return dt_obj

	def change_ymd_list_to_sec(self, base_day, input_list=[0,0,1]):
		"""
		몇년 몇월 몇일을 초로 바꾸는 것
		입력형태 : [몇년, 몇월, 몇일]
		현재일자를 기준으로
		월은 30일 기준으로 계산한다
		기준날짜에서 계산을 하는 것이다
		"""
		result = int(input_list[0]) *60*60*24*365  + int(input_list[1]) *60*60*24*30 + int(input_list[2])*60*60*24
		return result

	def check_input_time(self, input_time=""):
		"""
		어떤 형태가 들어오더라도 datetime으로 돌려주는 것
		"""
		if input_time =="":
			#아무것도 입력하지 않으면 local time 으로 인식한다
			result = datetime.now()

		elif type(input_time) == type(datetime.now()):
			#만약 datetime객체일때
			result = input_time

		elif type(input_time) == type(float(123.00)) or type(input_time) == type(int(123.00)):
			#timestamp로 인식
			result = datetime.fromtimestamp(input_time)

		elif type("string") == type(input_time):
			#  만약 입력형태가 문자열이면 : "202201O", "22/mar/01","22mar01"
			result = self.change_any_time_string_to_dt_obj(input_time)

		elif type(input_time) == type([]):
			#리스트 형태의 경우
			if len(input_time) >= 3:
				self.year, self.month, self.day = int(input_time[0]), int(input_time[1]), int(input_time[2])
				result = datetime(self.year, self.month, self.day)
		else:
			result = datetime.now()
		return result

	def del_set_item_by_list(self, input_set, input_list):
		"""
		list의 항목으로 들어간것을 하나씩 꺼내어서
		set안에 같은것이 있으면 지운다
		"""
		for one in input_list:
			input_set.remove(one)
		return input_set

	def get_1st_day_N_last_day_for_ym_list(self, input_ymlist):
		"""
		입력 : [2023, 05]
		출력 : [날짜객체, [1,31], 1, 31]
		"""
		date = datetime(year=input_ymlist[0], month=input_ymlist[1], day=1).date()
		monthrange = calendar.monthrange(date.year, date.month)
		first_day = calendar.monthrange(date.year, date.month)[0]
		last_day = calendar.monthrange(date.year, date.month)[1]
		return [date, monthrange, first_day, last_day]

	def get_date_monday_of_weekno(self, year, week_no):
		"""
		입력값 : 년도, 위크번호
		한 주의 시작은 '월'요일 부터이다
		"""

		utf_local_time = self.check_input_time([year, 1, 1])
		base = 1 if utf_local_time.isocalendar()[1] == 1 else 8
		temp = utf_local_time + datetime.timedelta(days=base - utf_local_time.isocalendar()[2] + 7 * (int(week_no) - 1))
		days = str(temp).split("-")
		#input_utf_time_no = nal.change_ymdlist_to_utftime([2022, 1, 1])
		#return [str(temp), temp, input_utf_time_no]

	def get_end_day_for_input_month(self, input_time):
		"""
		입력한 날의 월의 마지막 날짜를 계산
		입력받은 날자에서 월을 1나 늘린후 1일을 마이너스 한다
		예 : 2023-04-19 -> 2023-05-01 ->  2023-05-01 - 1일 -> 2023-04-30
		"""
		dt_obj =  self.check_input_time(input_time)
		if dt_obj.month == 12:
			year = dt_obj.year + 1
			month = 1
		else:
			year = dt_obj.year
			month = dt_obj.month +1

		dt_obj_1 = datetime(year, month, 1)
		dt_obj_2 = dt_obj_1 +timedelta(days = -1)
		result = dt_obj_2.day
		return result

	def get_last_day_of_month_for_ym_list(self, input_list = [2002, 3]):
		"""
		입력값 : datetime.date(2012, month, 1)
		결과값 : 원하는 년과 월의 마지막날을 알아내는것
		"""
		any_day = datetime.date(input_list[0], input_list[1], 1)
		next_month = any_day.replace(day=28) + timedelta(days=4)  # this will never fail
		result = next_month - timedelta(days=next_month.day)
		return result

	def get_month_range(self, year, month):
		"""
		입력월의 첫날과 끝날을 알려주는 것
		"""
		date = datetime(year=year, month=month, day=1).date()
		monthrange = calendar.monthrange(date.year, date.month)
		first_day = calendar.monthrange(date.year, date.month)[0]
		last_day = calendar.monthrange(date.year, date.month)[1]
		return [date, monthrange, first_day, last_day]

	def get_now(self):
		"""
		기본인 datetime 객체를 돌려주는 것은 별도로 표기하지 않는다
		"""
		dt_obj =  datetime.now()
		return dt_obj

	def get_now_as_utc_style(self):
		"""
		현재의 시간을 utc로 바꿉니다
		"""
		time_stamp = time.time()
		result = time.gmtime(time_stamp)
		return result

	def get_today_as_ymd_dash(self):
		"""
		오늘 날짜를 yyyy-mm-dd형식으로 돌려준다
		지금의 날짜를 돌려준다
		입력값 : 없음
		출력값 : 2022-03-01,
		"""
		just_now = self.check_input_time("")
		result = just_now.format("YYYY-MM-DD")
		return result

	def get_today_as_yyyy_mm_dd_style(self):
		"""
		날짜와 시간(datetime) -> 문자열로 : strftime
		날짜와 시간 형식의 문자열을 -> datetime으로 : strptime
		"""
		dt_obj =  datetime.now()
		result = dt_obj.strftime("%Y-%m-%d")
		return result

	def get_dt_obj_for_today(self):
		"""
		날짜와 시간(datetime) -> 문자열로 : strftime
		날짜와 시간 형식의 문자열을 -> datetime으로 : strptime
		"""
		dt_obj =  datetime.now()
		return dt_obj

	def get_ymd_of_monday_by_weekno(self, year, week_no):
		"""
		입력값 : 년도, 위크번호
		한 주의 시작은 '월'요일 부터이다
		"""
		first = date(year, 1, 1)
		base = 1 if first.isocalendar()[1] == 1 else 8
		temp = first + timedelta(days=base - first.isocalendar()[2] + 7 * (int(week_no) - 1))
		days = str(temp).split("-")
		#input_utf_time_no = nal.change_ymd_utftime([2022, 1, 1])
		#return [str(temp), temp, input_utf_time_no]

	def holiday_nation (self):
		"""
		휴일기준
		"""
		self.var["holiday_common"] = ["0101","0301","0505","0606", "0815","1001","1225",1.3]
		self.var["holiday_company"] = ["0708"]

	def make_unique_words(self, input_list2d):
		"""
		입력으로 들어온 자료들을 단어별로 구분하기위해서 만든것이며 /,&-등의 문자는 없앨려고 하는것이다
		"""

		list1d = []
		for one in input_list2d:
			list1d.extend(one)
		temp_result = []
		for one in list1d:
			one = str(one).lower()
			one = one.replace("/", " ")
			one = one.replace(",", " ")
			one = one.replace("&", " ")
			one = one.replace("-", " ")
			temp_result.extend(one.split(" "))
		result = list(set(temp_result))
		return result

	def minus_date0_date1(self, input_date1, input_date2):
		"""
		두날짜의 빼기
		"""
		utc1 = self.change_any_time_string_to_dt_obj(input_date1)
		utc2 = self.change_any_time_string_to_dt_obj(input_date2)
		result = abs((float(utc1) - float(utc2))/(60*60*24))
		return result

	def minus_date1_date2(self, date_1, date_2):
		"""
		두날짜의 빼기
		"""
		time_big = 1 #ymd_cls(date_1)
		time_small = 2 #ymd_cls(date_2)
		if time_big.lt_utc > time_small.lt_utc:
			pass
		else:
			time_big, time_small = time_small, time_big
		time_big.last_day = self.get_month_range(time_big.year, time_big.month)[3]
		time_small.last_day = self.get_month_range(time_small.year, time_small.month)[3]

		delta_year = abs(time_big.year - time_small.year)
		delta_day = int(abs(time_big.lt_utc - time_small.lt_utc) / (24 * 60 * 60))
		# 실제 1 년의 차이는 365 일 5 시간 48 분 46초 + 0.5초이다 (2 년에 1 번씩 윤초를 실시》
		actual_delta_year = int(abs(time_big.lt_utc - time_small.lt_utc) / (31556926 + 0.5))
		delta_month = abs((time_big.year * 12 + time_big.month) - (time_small.year * 12 + time_small.month))
		if time_big.day > time_small.day:
			actual_delta_month = delta_month - 1
		else:
			actual_delta_month = delta_month
		actual_delta_day = delta_day
		return [delta_year, delta_month, delta_day, actual_delta_year, actual_delta_month, actual_delta_day]

	def overtime(self):
		"""
		overtime
		[시작시간, 끝시간, 일당몇배]
		"""
		self.var["ot_common"] = [["0000", "0500", 1],["0505", "0606", 1.2]]
		self.var["ot_company"] = ["0708"]

	def period(self):
		"""
		계산기간
		"""
		self.var["during_common"] = ["0101","0301","0505","0606", "0815","1001","1225",1.3]

	def replace_time(self, dt_obj, input_dic):
		"""
		datetime.replace(year=self.year, month=self.month, day=self.day, hour=self.hour, minute=self.minute, second=self.second, microsecond=self.microsecond, tzinfo=self.tzinfo, *, fold=0)
		입력된 시간의 특정 단위를 바꿀수있다
		즉, 모든 년을 2002로 바꿀수도 있다는 것이다
		"""
		new_dt_obj = dt_obj.replace(input_dic)
		return new_dt_obj

	def salary(self):
		"""
		휴일기준
		"""
		self.var["holiday_common"] = ["0101","0301","0505","0606", "0815","1001","1225",1.3]
		self.var["holiday_company"] = ["0708"]

	def service_period(self):
		"""
		재직기간
		"""
		self.var["during_common"] = [["20110203","20130301"],["20150101","20160708"]]

	def shift_day_for_ymd_list(self, input_ymd_list="", input_no=""):
		"""
		입력한 날짜리스트를 기준으로 날을 이동시키는것
		아무것도 입력하지 않으면 현재 시간
		입력값 : [2022, 03, 02]
		출력값 : 2022-01-01
		"""
		utf_local_time = self.check_input_time(input_ymd_list)
		shift_now = utf_local_time.shift(days=int(input_no))
		result = shift_now.format("YYYY-MM-DD")
		return result

	def shift_dt_obj_by_day(self, dt_obj, input_no):
		"""
		"""
		new_dt_obj = dt_obj +timedelta(days = input_no)
		return new_dt_obj

	def shift_dt_obj_by_hour(self, dt_obj, input_no):
		"""
		시간을 이동
		"""
		new_dt_obj = dt_obj +timedelta(hours= input_no)
		return new_dt_obj

	def shift_dt_obj_by_min(self, dt_obj, input_no):
		"""
		분을 이동
		"""
		new_dt_obj = dt_obj +timedelta(minutes= input_no)
		return new_dt_obj

	def shift_dt_obj_by_month(self, dt_obj, input_no):
		"""
		월을 이동
		"""

		original_mon = dt_obj.month
		original_year = dt_obj.year

		delta_year, delta_month = divmod(input_no+original_mon, 12)

		new_month = original_mon + delta_month
		new_year = original_year + delta_year

		new_dt_obj = dt_obj.replace(year = new_year)
		new_dt_obj = new_dt_obj.replace(month = new_month)
		return new_dt_obj

	def shift_dt_obj_by_sec(self, dt_obj, input_no):
		"""
		날짜객체를 초단위로 이동시키는 것
		"""
		new_dt_obj = dt_obj +timedelta(seconds = input_no)
		return new_dt_obj

	def shift_dt_obj_by_year(self, dt_obj, input_no):
		"""
		년을 이동
		"""
		new_year = dt_obj.year + input_no
		new_dt_obj = dt_obj.replace(year = new_year)
		return new_dt_obj

	def shift_month_for_ymd_list(self, input_ymd_list = "", input_no = 3):
		"""
		입력한 날짜를 기준으로 날을 이동시키는것
		아무것도 입력하지 않으면 현재 시간
		입력값 : 시간
		출력값 : 2022-01-01
		"""
		utf_local_time = self.check_input_time(input_ymd_list)
		shift_now = utf_local_time.shift(months=int(input_no))
		result = shift_now.format("YYYY-MM-DD")
		return result

	def shift_time_by_month_as_ymd_list(self, input_time, input_no):
		"""
		기준날짜에서 월을 이동시키는것
		"""
		utf_time  =self.check_input_time(input_time)

		input_list  =self.change_input_time_to_ymd_style(utf_time)
		year = int(input_list[0])
		month = int(input_list[1])
		day = int(input_list[2])

		add_year,  remain_month = divmod((month + int(input_no)), 12)
		if remain_month == 0:
			add_year = add_year -1
			remain_month = 12
		result = [year+int(add_year), remain_month, day]
		return result

	def shift_year_for_ymd_list(self, input_ymd_list = "", input_no = 3):
		"""
		기준날짜에서 년을 이동시키는것
		입력형태 : [2022, 3, 1]
		"""
		utf_local_time = self.check_input_time(input_ymd_list)
		shift_now = utf_local_time.shift(years=int(input_no))
		result = shift_now.format("YYYY-MM-DD")
		return result


	def terms(self):
		"""
		용어정리
		아래와같은 형태로 용어를 사용한다
		"""

		result = """
		date	 : 2000-01-01
		datelist : [2000, 01, 01]
		ymdlist : [2000, 01, 01]
		time	 : 시간의 여러형태로 입력을 하면, 이에 맞도록 알아서 조정한다
		dhms	 : 2일3시간10분30초, day-hour-minute-sec
		hmslist  : [시, 분, 초]
		utftime  : 1640995200.0 또는 "", 1648037614.4801838 (의미 : 2022-03-23T21:13:34.480183+09:00)
		move	 : 입력값에 더하거나 빼서 다른 값으로 바꾸는것, 입력값과 출력값이 다를때 (출력값을 입력의 형태로 바꾸면 값이 다른것)
		change   : 형태를 바꾼것
		read	 : 입력값을 원하는 형태로 변경해서 갖고오는것
		get	  : 입력값에서 원하는 형태의 값을 갖고오는것
		shift	: 현재의 값을 같은 형태에서 값을 이동시키는것
		class datetime.datetime(year, month, day, hour=0, minute=0, second=0, microsecond=0, tzinfo=None, *, fold=0)
		datetime class : 1년 1월1일부터 날짜를 시작, 1년은 3600*24초로 계산
		utc class: 1970년 1월1일부터 날짜를 시작
		"""
		return result

	def time_list_by_step(self, start_hsm_list, step = 30, cycle = 20):
		"""
		시작과 종료시간을 입력하면, 30분간격으로 시간목록을 자동으로 생성시키는것
		"""
		result = []
		hour, min, sec = start_hsm_list
		result.append([hour, min, sec])
		for one in range(cycle):
			min = min + step
			over_min, min = divmod(min, 60)
			if over_min > 0:
				hour = hour + over_min
			hour = divmod(hour, 24)[1]
			result.append([hour, min, sec])
		return result

	def time_list_by_step_with_start_end(self, start_hsm_list, end_hsm_list, step = 30):
		"""
		시작과 종료시간을 입력하면, 30분간격으로 시간목록을 자동으로 생성시키는것
		"""
		result = []
		hour, min, sec = start_hsm_list
		hour_end, min_end, sec_end = end_hsm_list
		result.append([ hour, min, sec])
		while 1:
			min = min + step
			over_min, min = divmod(min, 60)
			if over_min > 0:
				hour = hour + over_min
			hour = divmod(hour, 24)[1]
			if int(hour)*60 + int(min) > int(hour_end)*60 + int(min_end) :
				break
			result.append([hour, min, sec])
		return result
	def working_hour(self):
		"""
		근무시간기준
		"""
		self.var["wt96"] = [[900,1800]]
		self.var["wt85"] = [[800,1700]]


	def get_weekno_for_ymd_list(self, input_date =""):
		"""
		입력한날의 week 번호를	계산
		입력값 : 날짜
		"""
		if input_date == "":
			today = self.get_today_as_yyyy_mm_dd_style()
			print(today)
			year, month, day = today.split("-")
			utf_local_time = self.check_input_time([year, month, day])
		else:
			utf_local_time = self.change_any_time_string_to_dt_obj(input_date)
		result = int(utf_local_time.strftime("%W"))
		return result

	def get_7_days_list_for_weekno(self, year, week_no):
		"""
		일요일부터 시작하는 7 개의 날짜를 돌려준다
		"""
		str_datetime = f'{year} {week_no} 0'
		startdate = datetime.strptime(str_datetime, '%Y %W %w')
		dates = [startdate.strftime("%Y-%m-%d")]
		for i in range(1, 7):
			day = startdate + timedelta(days=i)
			dates.append(day.strftime("%Y-%m-%d"))
		return dates

	###############################################################################

	def get_time_format(self, input_time=""):
		self.check_input_time(input_time)
		return self.var["utc"]


	def change_utc_timeformat(self, input_utc_time, format_a):
		result = time.strftime(format_a, input_utc_time)
		return result