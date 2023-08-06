# -*- coding: utf-8 -*-
import shutil#내장모듈
import pickle #내장모듈
import inspect #내장모듈
import re #내장모듈
import os #내장모듈
import random #내장모듈
from difflib import SequenceMatcher #내장모듈

import basic_data  # halmoney 모듈
import pynal  # halmoney 모듈
import pyclick  # halmoney 모듈

class youtil(pynal.pynal, pyclick.pyclick):
	"""
	여러가지 사무용에 사용할 만한 메소드들을 만들어 놓은것이며,
	좀더 특이한 것은 youtil2로 만들어서 사용할 예정입니다 
	"""
	def __init__(self):
		super().__init__()
		self.base_data = basic_data.basic_data()
		self.var = self.base_data.vars
		#공통으로 사용할 변수들을 설정하는 것

	def append_input_value_at_each_list1d_in_list2d(self, input_list2d, input_value):
		"""
		같은 항목으로 되어있는 자료를 제일 처음의 자료를 기준으로 합치는것
		2차원 리스트의 모든 자료끝에 값 추가하기
		"""
		result = []
		for list1d in input_list2d:
			result.append(list1d.append(input_value))
		return result

	def change_alpha_to_jamo(self, input_alpha_list):
		"""
		알파벳으로 바꾼 자음과 모음을 다시 저음과 모음으로 바꾸는 것
		"""
		changed_value = input_alpha_list
		data_set = self.var["eng_vs_jamo_list"]
		for one_list in data_set:
			for one_data in one_list:
				changed_value = changed_value.replace(one_data[0], one_data[1])
		result = changed_value.split("_")[:-1]
		#자모를 한글로 만드는 방법
		return result

	def change_alpha_to_jamo_old(self, input_alpha_list):
		"""
		알파벳을 한글의 자음이나 모음으로 변경
		"""
		import jfinder
		jf = jfinder.jfinder()
		words = str(input_alpha_list).replace("y", "")
		words = str(input_alpha_list).split("z")
		# print(input_alpha_list, words)
		result = []
		sql = "[o-x]+"
		for letter in words[:-1]:
			temp = []
			dd = jf.search_all_by_jfsql(sql, letter)
			jamo_1 = letter[0:dd[0][1]]
			jamo_1_changed = self.var["eng_vs_jamo"][jamo_1]
			jamo_2 = letter[dd[0][1]: dd[0][2]]
			jamo_2_changed = self.var["eng_vs_jamo"][jamo_2]
			jamo_3 = letter[dd[0][2]:]
			if jamo_3:
				jamo_3_changed = self.var["eng_vs_jamo"][jamo_3]
			else:
				jamo_3_changed = ""
			temp = [jamo_1_changed, jamo_2_changed, jamo_3_changed]
			result.append(temp)
		return result

	def change_alpha_to_korean(self, input_alpha):
		"""
		한글을 자음과 모음으로 분리해서, 알파벳으로 변경하는 것
		알파벳으로 바꾸면, 영문의 문자열 다루는 것을 사용할수도 있을것 같아 만들어 보았으며
		동시에 자음과 모음을 한번에 바꿀수있게 되는 것이다
		박 ==> ["ㅂ", "ㅏ", "ㄱ"] => "abc"
		이렇게 자음과 모음으로 구분된영어단어로 바뀌는 것이다
		자음과모음의 연결로도 가능하는데, 문제는 받침이 없는 경우와 space의 구분이 어렵다는 것이다
		"""

		result = self.change_alpha_to_jamo(input_alpha)
		return result

	def change_filename(self, old_path, new_path):
		"""
		화일이름 변경
		"""
		old_path = self.check_filepath(old_path)
		new_path = self.check_filepath(new_path)
		os.rename(old_path, new_path)

	def change_folder_name(self, old_path, new_path):
		"""
		폴더이름 변경
		"""
		os.rename(old_path, new_path)

	def change_jamo_to_alpha(self, input_jamo_list):
		"""
		한글의 자음과 모음의 한글자를 알파벳으로 바꾸는것
		"""
		result = ""
		for one_list in input_jamo_list:
			for jamo in one_list:
				eng_one = self.var["jamo_vs_eng"][jamo]
				result = result + eng_one
			result = result + "z"
		return result


	def change_jamo_to_korea(self, input_jamo_list):
		"""
		한글의 자음과 모음을 한글의 글자로 바꾸는것
		"""
		result = ""
		for one_list in input_jamo_list:
			for jamo in one_list:
				eng_one = self.var["jamo_vs_eng"][jamo]
				result = result + eng_one
			result = result + "z"
		return result

	def change_jamo_to_korean(self, input_list):
		"""
		한글을 자음과 모음으로 분리해서, 알파벳으로 변경하는 것
		"""
		result = self.change_jamo_to_korea(input_list)
		return result

	def change_jamo_to_korean_1(self, input_jamo_list):
		"""
		모든 한글은 유니코드에 U+AC00(가)부터 U+D7A3(힣)까지 사전순으로 올라가 있읍니다
		초성 19자 : ㄱ,ㄲ,ㄴ,ㄷ,ㄸ,ㄹ,ㅁ,ㅂ,ㅃ,ㅅ,ㅆ,ㅇ,ㅈ,ㅉ,ㅊ,ㅋ,ㅌ,ㅍ,ㅎ
		중성 21자 : ㅏ,ㅐ,ㅑ,ㅒ,ㅓ,ㅔ,ㅕ,ㅖ,ㅗ,ㅘ,ㅙ,ㅚ,ㅛ,ㅜ,ㅝ,ㅞ,ㅟ,ㅠ,ㅡ,ㅢ,ㅣ
		종성 28자 : (없음),ㄱ,ㄲ,ㄳ,ㄴ,ㄵ,ㄶ,ㄷ,ㄹ,ㄺ,ㄻ,ㄼ,ㄽ,ㄾ,ㄿ,ㅀ,ㅁ,ㅂ,ㅄ,ㅅ,ㅆ,ㅇ,ㅈ,ㅊ,ㅋ,ㅌ,ㅍ,ㅎ
		"""
		result = []
		for one_jamo in input_jamo_list:
			#유니코드의 순서대로 번호를 붙인것에서 순서를 읽어온다
			chosung_no = self.var["first_letter_no"][one_jamo[0]]  # 초성
			joongsung_no = self.var["second_letter_no"][one_jamo[1]]  # 중성
			try:
				jongsung_no = self.var["third_letter_no"][one_jamo[2]]  # 종성
			except:
				jongsung_no = self.var["third_letter_no"][""]  # 종성

			#한글이 시작되는 번호 44032번째부터 몇번째인지를 계산하는것
			unicode_no = chosung_no*21*28 + joongsung_no*28 + jongsung_no + 44032
			#print(one_jamo, " ==> unicode_no ==> ", unicode_no)
			result.append(chr(unicode_no))
		return result

	def change_korean_to_alpha(self, input_han):
		"""
		한글을 자음과 모음으로 분리해서, 알파벳으로 변경하는 것
		"""
		aa = self.split_jamo_in_korean(input_han)
		result = self.change_jamo_to_alpha(aa)
		return result

	def change_list1d_to_lower(self, data):
		"""
		모든 리스트의 자료를 소문자로 만드는것이다
		"""
		for a in range(len(data)):
			try:
				data[a] = (data[a]).lower()
			except:
				pass
		return data

	def sort_list2d_by_yy_list(input_data, input_list=[0, 2, 3]):
		"""
		2차원리스트를 몇번째를 기준으로 정렬하는것
		"""
		text = ""
		for one in input_list:
			text = text + "row[" + str(one * -1) + "],"
		text = text[:-1]
		exec("global sorted_list2d; sorted_list2d = sorted(input_data, key=lambda row: (%s))" % text)
		global sorted_list2d
		return sorted_list2d

	def change_list1d_to_upper (self, data):
		"""
		1차원자료의 모든 내용물을 대문자로 만들어 주는 것이다
		"""
		for a in range(len(data)):
			try:
				data[a] = (data[a]).upper()
			except:
				pass
		return data

	def change_list1d_to_list2d(self, input_data):
		"""
		입력된 1차원 자료를 2차원으로 만드는 것
		입력자료는 리스트나 듀플이어야 한다
		"""
		if type(input_data[0]) == type([]) or type(input_data[0]) == type(()):
			# 2차원의 자료이므로 입력값 그대로를 돌려준다
			result = input_data
		else:
			# 1차원의 자료라는 뜻으로, 이것을 2차원으로 만들어 주는 것이다
			result = []
			for one in input_data:
				result.append([one])
		return result

	def change_list1d_to_list2d_by_step(self, input_list="", xy=""):
		"""
		입력값이 1차원과 2차원의 자료가 섞여 일을때
		2차원의 자료형태로 모두 같은 크기로 만들어 주는것
		"""
		temp_result = []
		x_len, y_len = xy
		list1_max_len = len(input_list)
		list2_max_len = y_len
		count = int(list1_max_len / x_len)

		# 2차원자료중 가장 큰것을 계산한다
		for one_value in input_list:
			if type(one_value) == type([]):
				list2_max_len = max(list2_max_len, len(one_value))

		for one_value in input_list:
			temp_list = one_value
			# 모든 항목을 리스트형태로 만든다
			if type(one_value) != type([]):
				temp_list = [one_value]

			# 최대길이에 맞도록 적은것은 ""으로 갯수를 채운다
			if list2_max_len - len(temp_list) > 0:
				temp_list.extend([""] * (list2_max_len - len(temp_list)))
			temp_result.append(temp_list)

		result = []
		for no in range(count):
			start = no * x_len
			end  = start + x_len
			result.append(temp_result[start:end])

		return result

	def change_list1d_data_to_space_by_step(self, input_list, step, start=0):
		"""
		1차원의 자료중에서 원하는 순서째의 자료를 ""으로 만드는것
		"""
		if start != 0:
			result = input_list[0:start]
		else:
			result = []

		for num in range(start, len(input_list)):
			temp_value = input_list[num]
			if divmod(num, step)[1] == 0:
				temp_value = ""
			result.append(temp_value)

		return result

	def change_list1d_to_text_with_chainword(self, input_list, chain_word=" ,"):
		"""
		리스트 자료들을 중간문자를 추가하여 하나의 문자열로 만드는 것,
		“aa, bbb, ccc” 이런 식으로 만드는 방법이다
		리스트 자료들을 중간에 문자를 추가하여 한줄의 문자로 만드는 것
		입력형태 : ["aa", "bb","ccc"]
		출력형태 : “aa, bbb, ccc”
		"""
		result = ""
		for one_word in input_list:
			result = result + str(one_word) + str(chain_word)

		return result[:-len(chain_word)]

	def change_list2d_to_dic(self, list_2d, list_title):
		"""
		2차원리스트를 사전형식으로 만드는 것
		제목과 연결해서 사전을 만들어서 다음에 편하게 쓰고 넣을수있도록 만들려고 한다
		"""
		result = []
		for one in list_2d:
			my_dic = {}
			for no in range(len(list_title)):
				my_dic[list_title[no]] = one[no]
			result.append(my_dic)
		return result

	def change_list2d_to_list1d(self, input_data):
		"""
		2차원의 list를 1차원으로 만들어 주는것
		항목 : ['항목1', '기본값1', '설명', {'입력형태1':'설명1', '입력형태2':'설명1',.... }]
		결과 ['항목1', '기본값1', '설명', '입력형태1:설명1', '입력형태2:설명1',.... }]
		위 형태의 자료를 한줄로 만들기위해 자료를 변경한다
		"""
		result = []
		for one_data in input_data:
			if type(one_data) == type({}):
				for key in list(one_data.Keys()):
					value = str(key) + " : " + str(one_data[key])
					result.append(value)
			elif type(one_data) == type(()) or type(one_data) == type([]) or type(one_data) == type(set()):
				for value in one_data:
					result.append(value)
			else:
				result.append(one_data)
		return result

	def change_list2d_to_samelen_list2d(self, input_data):
		"""
		길이가 다른 2dlist의 내부 값들을 길이가 같게 만들어주는 것이다
		가변적인 2차원배열을 최대크기로 모두 같이 만들어 준다
		"""
		result = []
		max_len = max(len(row) for row in input_data)
		for list_x in input_data:
			temp = list_x
			for no in range(len(list_x), max_len):
				temp.append("")
			result.append(temp)
		return result

	def change_num_to_1000comma_num(self, input_num):
		"""
		입력된 숫자를 1000단위로 콤마를 넣는것
		"""
		temp = str(input_num).split(".")
		total_len = len(temp[0])
		result = ""
		for num in range(total_len):
			one_num = temp[0][- num - 1]
			if num % 3 == 2:
				result = "," + one_num + result
			else:
				result = one_num + result
		if len(temp) > 1:
			result = result + "." + str(temp[1])
		return result

	def change_python_file_to_sorted_by_def(self, filename):
		"""
		python으로만든 화일을 읽어서 def를 기준으로 정렬해서 돌려주는 것
		1. 프린트해서 나타냄
		2. 화일로 정렬된것을 만듦
		3. 리스트형태로 돌려주는것
		"""
		file_pointer = open(filename, 'r', encoding='utf-8') #텍스트 읽어오기
		file_list = file_pointer.readlines() # 한번에 다 읽기

		all_text = ""
		temp = []
		result = {}
		title = "000"
		for one_line_text in file_list:
			#def로 시작이 되는지 알아 내는것
			if str(one_line_text).strip()[0:3] == "def" and str(one_line_text).strip()[-1] == ":":
				result[title] = temp #def나오기 전까지의 자료를 저장합니다
				temp = []
				title = str(one_line_text).strip() #사전의 key를 def의 이름으로 만드는 것이다
			temp.append(one_line_text)
		result[title] = temp

		sorted_keys = list(result.keys())
		sorted_keys.sort() #key인 제목을 기준으로 정렬을 하도록 만든것
		write_file = open("output_output_33.txt", 'w', encoding='utf-8') #텍스트 읽어오기

		for one_key in sorted_keys:
			for one_line in result[one_key]:
				one_line = one_line.replace("\n", "")
				print(one_line) #별도로 화일로 만들지 않고, 터미널에 나타나는것을 복사해서 사용하는 방법으로 만듦
				all_text = 	all_text + one_line
				write_file.write(one_line+"\n")
		write_file.close()
		return result

	def change_list2d_to_set_item(self, input_set, input_list2d):
		"""
		2차원 리스트의 항목들을 set자료형으로 바꾸는 것
		input_list = [["변경전자료1", "변경후자료2"], ["변경전자료11", "변경후자료22"], ]

		"""
		for list_1d in input_list2d:
			input_set.discard(list_1d[0])
			input_set.add(list_1d[1])
		return input_set

	def change_xylist_to_yxlist(self, input_list2d="입력필요"):
		"""
		trans_list( input_list2d="입력필요")
		2차원자료를 행과열을 바꿔서 만드는것
		단, 길이가 같아야 한다
		"""
		checked_input_list2d = self.change_list2d_to_samelen_list2d(input_list2d)
		result = [list(x) for x in zip(*checked_input_list2d)]
		return result

	def check_col_name(self, col_name):
		"""
		각 제목으로 들어가는 글자에 대해서 변경해야 하는것을 변경하는 것이다
		커럼의제목으로 사용 못하는것을 제외
		"""
		for temp_01 in [[" ", "_"], ["(", "_"], [")", "_"], ["/", "_per_"], ["%", ""], ["'", ""], ['"', ""], ["$", ""],
						["__", "_"], ["__", "_"]]:
			col_name = col_name.replace(temp_01[0], temp_01[1])
		if col_name[-1] == "_": col_name = col_name[:-2]
		return col_name

	def check_filename(self, temp_title):
		"""
		화일의 제목으로 사용이 불가능한것을 제거한다
		"""
		for temp_01 in [[" ", "_"], ["(", "_"], [")", "_"], ["/", "_per_"], ["%", ""], ["'", ""], ['"', ""], ["$", ""], ["__", "_"], ["__", "_"]]:
			temp_title = temp_title.replace(temp_01[0], temp_01[1])
		if temp_title[-1] == "_": temp_title = temp_title[:-2]
		return

	def check_filepath(self, file):
		"""
		입력자료가 폴더를 갖고있지 않으면 현재 폴더를 포함해서 돌려준다
		"""
		if len(file.split(".")) > 1:
			result = file
		else:
			cur_dir = self.read_current_path()
			result = cur_dir + "\\" + file
		return result

	def compare_list_two_value(self, raw_data, req_number, project_name, vendor_name, nal):
		'''
		위아래 비교
		회사에서 사용하는 inq용 화일은 두줄로 구성이 된다
		한줄은 client가 요청한 스팩이며
		나머지 한줄은 vendor가 deviation사항으로 만든 스팩이다
		이두가지의 스팩을 하나로 만드는 것이다
		즉, 두줄에서 아래의 글씨가 있고 그것이 0, None가 아니면 위의것과 치환되는 것이다
		그런후 이위의 자료들만 따로 모아서 돌려주는 것이다
		'''
		data = list(raw_data)
		data_set = []
		data_set_final = []

		for a in range(0, len(data), 2):
			for b in range(len(data[1])):
				if not (data[a + 1][b] == data[a][b]) and data[a + 1][
					b] != None and data[a + 1][b] != 0:
					data_set.append(data[a + 1][b])
				else:
					data_set.append(data[a][b])
			data_set.append(req_number)
			data_set.append(project_name)
			data_set.append(vendor_name)
			data_set.append(nal)
			data_set_final.append(data_set)
			data_set = []
		return data_set_final

	def copy_file(self, old_path, new_path, meta=""):
		"""
		화일복사
		"""
		old_path = self.check_filepath(old_path)
		new_path = self.check_filepath(new_path)
		if meta == "":
			shutil.copy(old_path, new_path)
		else:
			shutil.copy2(old_path, new_path)

	def copy_folder(self, old_path, new_path):
		"""
		폴더복사
		"""
		shutil.copy(old_path, new_path)

	def count_same_value_for_ordered_list(self, input_list):
		"""
		2개이상 반복되는것중 높은 갯수 기준으로 돌려주는것
		"""
		result_dic = {}
		# 리스트안의 자료가 몇번나오는지 갯수를 센후에
		# 1번이상의 자료만 남기고 다 삭제하는것
		for one in input_list:
			if one in result_dic.keys():
				result_dic[one] = result_dic[one] + 1
			else:
				result_dic[one] = 1

		# 1번이상의 자료만 남기고 다 삭제하는것
		for one in list(result_dic.keys()):
			if result_dic[one] == 1:
				del result_dic[one]

		# 사전자료를 2차원리스트로 만든것
		new_list = []
		for key, val in result_dic.items():
			new_list.append([key, val])

		# 사전자료를 2차원리스트로 만든것을 역순으로 정렬한것
		new_list = sorted(new_list, key=lambda x: x[1], reverse=True)
		return new_list

	def del_set_item_as_same_list_data(self, input_set, input_list):
		"""
		list의 항목으로 들어간것을 하나씩 꺼내어서
		set안에 같은것이 있으면 지운다
		"""
		for one in input_list:
			input_set.remove(one)
		return input_set

	def delete_all_explanation_in_input_text(self, input_text):
		"""
		넘어온 text 에서 주석으로 사용되는 것들을 지우는것
		"""
		input_text = re.sub(re.compile(r"[\s]*#.*[\n]"), "\n", input_text)
		input_text = re.sub(re.compile(r"[\s]*''',*?'''", re.DOTALL|re.MULTILINE), "", input_text)
		input_text = re.sub(re.compile(r'[\s]*""".*?"""', re.DOTALL|re.MULTILINE), "", input_text)
		input_text = re.sub(re.compile(r"[\n][\s]*?[\n]"), "\n", input_text)
		return input_text

	def delete_contineous_same_data_in_list1d (self, input_datas):
		"""
		입력된 자료중에서 연속으로 같은값만 나오면 삭제하는 것이다
		"""
		if len(input_datas) == 0:
			#print ("아무자료도 없읍니다. 확인 바랍니다")
			pass
		else:
			a = 0
			while a!= len(input_datas)-1:
				if input_datas[a] == input_datas[a+1]: input_datas[a] = []
				a = a+1
		return input_datas

	def delete_continious_same_data(self, input_list):
		"""
		연속된 같은 자료만 지우는 것
		"""
		result = []
		for no in range(len(input_list)-1):
			if input_list[no] == input_list[no+1]:
				pass
				#excel.write_value_in_cell("", [no+3, "ae"], "")
			else:
				result.append(input_list[no])
		return result

	def delete_empty_value_in_list(self, input_list, condition=["", None, [], ()]):
		"""
		넘어온 리스트 형태의 자료중 조건에 맞는것이 있으면 제거하는 것
		입력형태 : ["aaa", "", None, "", "bbb"], [["aaa", "", None, "", "bbb"],"werw", 31231, [], ["aaa", "", None, "", "bbb"]]
		출력형태 : ["aaa", "bbb"], [['aaa', 'bbb'], 'werw', 31231, [], ['aaa', 'bbb']]
		"""
		for x in range(len(input_list) - 1, -1, -1):
			if input_list[x] in condition:
				del (input_list[x])
			else:
				if type(input_list[x]) == type([]):
					for y in range(len(input_list[x]) - 1, -1, -1):
						if input_list[x][y] in condition:
							del (input_list[x][y])
				else:
					if input_list[x] in condition:
						del (input_list[x])
		return input_list

	def delete_file(self, old_path):
		"""
		화일삭제
		"""
		old_path = self.check_filepath(old_path)
		os.remove(old_path)

	def delete_folder(self, old_dir, empty="no"):
		"""
		폴더삭제
		폴더안에 자료가 있어도 삭제
		"""
		if empty == "no":
			shutil.rmtree(old_dir)
		else:
			os.rmdir(old_dir)

	def delete_list1d_by_even_no (self, data):
		"""
		홀수의 자료만 삭제
		"""
		result = []
		for no in range(len(data)):
			if divmod(no, 2)[1] != 1:
				result.append(data[no])
		return result

	def delete_list1d_by_odd_no (self, data):
		"""
		짝수의 자료만 삭제
		"""
		result = []
		for no in range(len(data)):
			if divmod(no, 2)[1] != 0:
				result.append(data[no])
		return result

	def delete_over2_emptyline_in_file(self, filename):
		"""
		화일을 읽어 내려가다가 2줄이상의 띄어쓰기가 된것을 하나만 남기는것
		텍스트로 저장된것을 사용하다가 필요해서 만듦
		"""
		f = open(filename, 'r', encoding='UTF8')
		lines = f.readlines()
		num = 0
		result = ""
		for one_line in lines:
			if one_line == "\n":
				num = num + 1
				if num == 1:
					result = result + str(one_line)
				elif num > 1:
					# print("2줄발견")
					pass
			else:
				num = 0
				result = result + str(one_line)
		return result

	def delete_same_value_in_list1d (self, input_datas, status = 0):
		"""
		입력자료에서 같은것만 삭제
		"""
		if status == 0:
			result = []
			#계속해서 pop으로 하나씩 없애므로 하나도 없으면 그만 실행한다
			while len(input_datas)!= 0:
				gijun = input_datas.pop()
				sjpark = 0
				result.append(gijun)
				for number in range(len(input_datas)):
					if input_datas[int(number)] == [] : #빈자료일때는 그냥 통과한다
						pass
					if input_datas[int(number)] == gijun :#자료가 같은것이 있으면 []으로 변경한다
						sjpark = sjpark+1
						input_datas[int(number)] = []
			else:
				#중복된것중에서 아무것도없는 []마저 없애는 것이다. 위의 only_one을 이용하여 사용한다
				#같은것중에서 하나만 남기고 나머지는 []으로 고친다
				#이것은 연속된 자료만 기준으로 삭제를 하는 것입니다
				#만약 연속이 되지않은 같은자료는 삭제가 되지를 않읍니다
				result = list(set(input_datas))
				for a in range(len(result)-1,0,-1):
					if result[a] == []:
						del result[int(a)]
		return result

	def delete_waste_data_in_inputdata_except_num_eng(self, original_data):
		"""
		숫자와 영어만 남기는것, 나머지것은 다 삭제하는것
		result = []
		입력형태 :
		출력형태 :
		"""
		result = []
		for one_data in original_data:
			temp = ""
			for one in one_data:
				if str(one) in ' 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_':
					temp = temp + str(one)
			result.append(temp)
		return result

	def get_all_method_help_text_for_input_object(self, input_object):
		"""
		객체를 주면 메소드의 help를 돌려 주는것
		"""
		result = {}
		for method_name in dir(input_object):
			temp = []
			#이중언더 메소드는 제외시키는것
			if not method_name.startswith('__'):
				try:
					temp.append(method_name)
					temp.append(getattr(input_object, method_name).__doc__)
				except:
					pass
			result[method_name] = temp
		return result

	def get_all_method_name_with_argument_for_input_object(self, object):
		"""
		원하는 객체를 넣으면, 객체의 함수와 각 함수의 인자를 사전형식으로 돌려준다
		"""
		result = {}
		for obj_method in dir(object):
			try:
				method_data = inspect.signature(getattr(object, obj_method))
				dic_fun_var = {}
				if not obj_method.startswith("_"):
					for one in method_data.parameters:
						value_default = method_data.parameters[one].default
						value_data = str(method_data.parameters[one])

						if value_default == inspect._empty:
							dic_fun_var[value_data] = None
						else:
							value_key, value_value = value_data.split("=")
							if "remove" in obj_method:
								print(value_key, value_value)
							if value_value == "''" or value_value == '""':
								value_value = ''
							# 변수값중 ''가 들어간것이 없어져서, 아래의 것을 주석처리를 함
							# value_value = str(value_value).replace("'", "")
							# print(value_data, "키값==>", value_key, "입력값==>", value_value)
							dic_fun_var[str(value_key)] = value_value
						result[obj_method] = dic_fun_var

			except:
				pass
		return result


	def get_all_method_name_for_input_object(self, object):
		"""
		원하는 객체를 넣으면, 객체의 함수와 각 함수의 인자를 사전형식으로 돌려준다
		"""
		result = []
		for obj_method in dir(object):
			result.append(obj_method)

		return result


	def get_all_method_name_for_input_object_except_dunder_methods(self, object):
		"""
		원하는 객체를 넣으면, 객체의 함수와 각 함수의 인자를 사전형식으로 돌려준다
		"""
		result = []
		for obj_method in dir(object):
			if obj_method.startswith("__"):
				pass
			else:
				result.append(obj_method)

		return result


	def get_file_list_from_directory(self, directory):
		"""
		입력폴더안의 화일들을 리스트형태로 돌려주는것
		"""
		result = os.listdir(directory)
		return result

	def get_max_length_for_list2d(self, input_list2d):
		"""
		2차원 배열의 제일 큰 갯수를 확인한다
		"""
		max_length = max(len(row) for row in input_list2d)
		return max_length

	def get_one_line_as_searched_word_in_file(self, file_name="pcell.py", input_text="menu_dic["):
		"""
		화일안에서 원하는 단어가 들어간 줄을 리스트로 만들어서 돌려주는것
		메뉴를 만들 목적으로 한것
		"""
		aa = open(file_name, 'r', encoding="UTF-8")
		result = []
		for one in aa.readlines():
			if input_text in str(one).strip():
				#print(str(one).strip())
				result.append(str(one).strip())
		return result

	def history(self):
		result = 	"""
			"""
		return result

	def insert_input_data_in_list1d_by_step(self, input_list, insert_value, step):
		"""
		기존자료에 n번째마다 자료를 추가하는 기능
		raw_data = ['qweqw','qweqweqw','rterert','gdgdfgd',23,534534,'박상진']
		added_data = "new_data"
		step=3, 각 3번째 마다 자료를 추가한다면
		"""
		var_1, var_2 = divmod(len(input_list), int(step))
		for num in range(var_1, 0, -1):
			input_list.insert(num * int(step) - var_2 + 1, insert_value)
		return input_list

	def insert_line_in_list(self, data, number=1, input_data=[]):
		"""
		리스트에 일정한 간격으로 자료삽입
		"""
		total_number = len(data)
		dd = 0
		for a in range(len(data)):
			if a % number == 0 and a != 0:
				if total_number != a:
					data.insert(dd, input_data)
					dd = dd + 1
			dd = dd + 1
		return data

	def make_dic_for_2list(self, key_list, value_list):
		"""
		두개의 리스트를 받으면 사전으로 만들어 주는 코드
		"""
		result = dict(zip(key_list, value_list))
		return result

	def make_text_file_for_input_text(self, file_full_name, input_text):
		"""
		텍스트자료를 화일로 저장하는것
		"""
		new_file = open(file_full_name, "w", encoding="UTF-8")
		for one_line in input_text:
			new_file.write(one_line)

	def make_folder(self, input_folder_name):
		"""
		폴더 만들기
		"""
		os.mkdir(input_folder_name)

	def make_random_list(self, input_list, input_limit, input_times=1):
		"""
		입력된 자료를 랜덤으로 리스트를 만드는 것
		"""
		result_set = []
		if len(input_list) == 2:
			input_list = list(range(input_list[0], input_list[1]))
		for no in range(input_times):
			result = []
			for num in range(input_limit):
				dd = random.choice(input_list)
				result.append(dd)
				input_list.remove(dd)
			result_set.append(result)
		return result_set

	def manual(self):
		result ="""
		여기저기 사용이 가능한것을 하나로 모아놓은 것이다
		"""
		return result

	def minus_two_list1d(self, list1d_a, list1d_b):
		"""
		두개 리스트중에서，앞과 동일한것만 삭제하기 위한 것
		앞의 리스트에서 뒤에 갈은것만 삭제하는것
		예 : [1,2,3,4,5] - [3,4,5,6,7] ==> [1,2]
		"""
		result = [x for x in list1d_a if x not in list1d_b]
		return result

	def move_data_to_right_by_step(self, input_list1d, step_no):
		"""
		1차원으로 들어온 자료를 갯수에 맞도록  분리해서 2차원의 자료로 만들어 주는것
		"""
		result = []
		for partial_list in input_list1d[::step_no]:
			result.append(partial_list)
		return result

	def move_file(self, old_file, new_file):
		"""
		화일을 이동시키는것
		"""
		old_file = self.check_filepath(old_file)
		shutil.move(old_file, new_file)

	def move_folder(self, old_dir, new_dir):
		"""
		폴더를 이동시키는것
		"""
		shutil.move(old_dir, new_dir)

	def pick_unique_col_name_compare_table_col_name(self, table_name, data2):
		"""
		고유한 컬럼만 골라낸다
		"""
		result = []
		columns = self.read_all_filename_in_folder(table_name)
		update_data2 = self.delete_waste_data_in_inputdata_except_num_eng(data2)
		for temp_3 in update_data2:
			if not temp_3.lower() in columns:
				result.append(temp_3)
		return result

	def pick_unique_data_in_list1d(self, input_data):
		"""
		리스트의 값중 고유한것만 골라내기
		"""
		temp = set()
		for one in input_data:
			temp.add(one)
		result = list(temp)
		return result

	def plus_two_list_with_samelen(self, input_list2d_1, input_list2d_2):
		"""
		선택한 영역이 2개를 서로 같은것을 기준으로 묶을려고하는것이다
		제일앞의 한줄이 같은것이다
		만약 묶을려고 할때 자료가 없을때는 그 기준자료만큼 빈자료를 넣어서 다음자료를 추가하는 것이다
		"""
		no_of_list2d_1 = len(input_list2d_1[0]) - 1
		no_of_list2d_2 = len(input_list2d_2[0]) - 1
		empty_list2d_1 = [""] * no_of_list2d_1
		empty_list2d_2 = [""] * no_of_list2d_2
		# 리스트형태로는 코드가 더 길어질것으로 보여서 입력자료를 사전으로 변경 한것
		temp_dic = {}
		for one in input_list2d_1:
			temp_dic[one[0]] = one[1:]
		checked_list = []
		# 기준이 되는 자료에 항목이 있을때
		for one in input_list2d_2:
			if one[0] in temp_dic.keys():
				temp_dic[one[0]] = list(temp_dic[one[0]]) + list(one[1:])
			else:
				temp_dic[one[0]] = empty_list2d_1 + list(one[1:])
			checked_list.append(one[0])
		# 기준자료에 항목이 없는것에 대한것
		for one in temp_dic.keys():
			if not one in checked_list:
				temp_dic[one] = list(temp_dic[one]) + empty_list2d_2
		# 사전형식을 리스트로 다시 만드는것
		result = []
		for one in temp_dic:
			result.append([one] + list(temp_dic[one]))
		return result

	def read_all_filename_in_folder(self, directory=""):
		"""
		폴더안의 모든 화일이름을 읽오오는것
		단, 폴더안의 폴더이름은 제외시킨다
		"""
		if directory=="":
			directory = self.read_current_path()
		result = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
		return result

	def read_current_path(self):
		"""
		현재의 경로를 돌려주는것
		"""
		result = os.getcwd()
		return result

	def read_file(self, filename):
		"""
		화일 읽기
		"""
		try:
			f = open(filename, 'r',encoding='UTF-8')
			result = f.readlines()
			f.close()
		except:
			f = open(filename, 'r')
			result = f.readlines()
			f.close()

		return result

	def read_file_as_list1d(self, file_full_name):
		"""
		화일을 리스트형태와 text형태로 2개로 돌려준다
		"""
		file_object = open(file_full_name, "r", encoding="UTF-8")
		file_as_list = file_object.readlines()
		file_object.close()
		return file_as_list

	def read_file_by_filename(self, filename):
		"""
		화일을 읽어오는 것
		"""
		try:
			f = open(filename, 'r',encoding='UTF-8')
			result = f.readlines()
			f.close()
		except:
			f = open(filename, 'r')
			result = f.readlines()
			f.close()
		return result

	def read_filenames_in_folder_by_extension_name(self, directory="./", filter="pickle"):
		"""
		pickle로 만든 자료를 저장하는것
		"""
		result = []
		all_files = os.listdir(directory)
		if filter == "*" or filter == "":
			filter = ""
			result = all_files
		else:
			filter = "." + filter
			for x in all_files:
				if x.endswith(filter):
					result.append(x)
		return result

	def read_method_code_by_method_name(self, str_method_name):
		"""
		메소드의 코드를 읽어오는것
		문자로 넣을수있도록 만든 것이다
		"""
		#method_name = eval(str_method_name)
		code_text = inspect.getsource(str_method_name)
		return code_text

	def read_pickle_file(self, path_n_name=""):
		"""
		pickle로 자료를 만든것을 읽어오는 것이다
		"""
		with open(path_n_name, "rb") as fr:
			result = pickle.load(fr)
		return result

	def save_input_data_to_pickle_file(self, source_data = "", file_name = "", path = "D:\\"):
		"""
		자료를 pickle 로 저장하는것
		"""
		if not "." in file_name:
			file_name = file_name +".pickle"
		with open(path+file_name, "wb") as fr:
			pickle.dump(source_data, fr)

	def similar(self, a, b):
		"""
		두개의 유사도를 측정
		"""
		return SequenceMatcher(None, a, b).ratio()

	def sort_list1d (self, input_list1d):
		"""
		1차원 리스트를 정렬하는 것
		"""

		str_temp = []
		int_temp = []
		for one in input_list1d:
			if type(one) == type("str"):
				str_temp.append(one)
			else:
				int_temp.append(one)

		result_int = sorted(int_temp)
		result_str = sorted(str_temp)
		result = result_int + result_str
		return result

	def sort_list1d_by_str_len(self, input_list):
		"""
		일반적인 정렬이 아니고,	문자의 길이에 따라서 정렬
		"""
		input_list.sort(key=lambda x: len(str(x)))
		return input_list

	def sort_list2d(self, input_list2d):
		"""
		2차원 리스트를 정렬하는 것
		"""
		result=self.sort_list2d_by_index(input_list2d, index_no=0)
		return result

	def sort_list2d_by_index(self, input_list2d, index_no=0):
		"""
		입력 :  리스트자료
		리스트자료를 몇번째 순서를 기준으로 정렬하는것
		숫자와 문자가 같이 섞여 있어도, 정렬이 가능
		aa = [[111, 'abc'], [222, 222],['333', 333], ['777', 'sjpark'], ['aaa', 123],['zzz', 'sang'], ['jjj', 987], ['ppp', 'park']]
		value=sort_list(리스트자료, 정렬기준번호)
		"""

		str_temp = []
		int_temp = []
		for one in input_list2d:
			if type(one[index_no]) == type("str"):
				str_temp.append(one)
			else:
				int_temp.append(one)

		result_int = sorted(int_temp, key=lambda x: x[index_no])
		result_str = sorted(str_temp, key=lambda x: x[index_no])
		result = result_int + result_str

		return result

	def sort_mixed_list1d(self, input_list1d):
		"""
		1, 2차원의 자료가 섞여서 저장된 자료를 정렬하는 것
		"""
		int_list = sorted([i for i in input_list1d if type(i) is float or type(i) is int])
		str_list = sorted([i for i in input_list1d if type(i) is str])
		return int_list + str_list

	def split_all_list1d_to_list2d_by_input_text(self, input_list, input_text):
		"""
		리스트로 들어온 자료들을 한번에 분리해서 2차원리스트로 만드는 것
		"""

		result = []
		for one_value in input_list:
			temp_result = str(one_value).split(input_text)
			result.append(temp_result)
		return result

	def split_file_by_def(self, filename, base_text="def"):
		"""
		화일안의 def를 기준으로 문서를 분리하는것
		같은 함수의 코드를 찾기위해 def로 나누는것
		맨앞의 시작글자에 따라서 나눌수도 있다
		"""
		temp_list = []
		result = []
		# 화일을 읽어온다
		f = open(filename, 'r', encoding='UTF8')
		lines = f.readlines()
		original = lines
		# 빈 줄을 제거한다
		lines = list(map(lambda s: s.strip(), lines))
		start_no = 0
		for no in range(len(lines)):
			line = lines[no]

			# 각줄의 공백을 제거한다
			one_line = line.strip()
			# 혹시 있을수 있는 줄바꿈을 제거한다
			one_line = one_line.replace("\n", "")
			# 맨 앞에서 def가 발견이되면 여태저장한것을 최종result리스트에 저장 하고 새로이 시작한다
			if one_line[0:(len(base_text) + 1)] == base_text and temp_list != []:
				#print("처음은 ===> ", start_no)
				#print("끝은 ===> ", no)
				result.append(temp_list, start_no, no)
				start_no = no
				temp_list = []
			# 빈행이나 주석으로된 열을 제외한다
			if one_line != "" and one_line[0] != "#":
				temp_list.append(one_line)
		f.close()
		return result

	def split_filepath_by_path_and_name(self, input_value=""):
		"""
		입력값을 경로와 이름으로 분리
		"""
		filename = ""
		path = ""
		input_value = input_value.replace("/", "\\")
		temp_1 = input_value.split("\\")
		if "." in temp_1[-1]:
			filename = temp_1[-1]
		if len(temp_1) > 1 and "\\" in temp_1[:len(temp_1[-1])]:
			path = input_value[:len(temp_1[-1])]
		result = [filename, path]
		return result

	def split_input_file_by_method_name_with_delete_empty_line(self, filename):
		"""
		py화일을 다를려고 만든것이며
		화일의 메소드를 기준으로 나누면서 동시에 빈라인은 삭제하는것
		"""
		def_list = []
		result = []
		total_code = ""
		total = ""
		# 화일을 읽어온다
		f = open(filename, 'r', encoding='UTF8')
		original_lines = f.readlines()
		f.close()
		#print(len(original_lines))
		num = 1
		temp = ""
		exp_start = ""
		exp_end = ""
		exp_mid = ""
		for one_line in original_lines:
			total = total + one_line
			changed_one_line = one_line.strip()
			if changed_one_line == "":
				one_line = ""
			elif changed_one_line[0] == "#":
				one_line = ""
			elif changed_one_line[0:3] == "def":
				def_list.append(temp)
				temp = one_line
			elif '"""' in changed_one_line:
				if changed_one_line[0:3] == '"""':
					exp_end = "no"
					exp_start = "yes"
					one_line = ""
				elif changed_one_line[:-3] == '"""':
					if exp_mid == "yes":
						exp_mid = "no"
					else:
						exp_end = "yes"
						exp_start = "no"
						one_line = ""
				else:
					if exp_mid == "yes":
						exp_mid = "no"
					else:
						exp_mid = "yes"

				num = num +1

			if exp_start == "yes" and exp_end == "no":
				one_line = ""

			temp = temp + one_line
			total_code = total_code + one_line
		#print(num)

		return [def_list, total_code, total]

	def split_input_text_as_eng_vs_num(self, data):
		"""
		단어중에 나와있는 숫자, 영어를 분리하는기능
		"""
		re_compile = re.compile(r"([a-zA-Z]+)([0-9]+)")
		result = re_compile.findall(data)
		new_result = []
		for dim1_data in result:
			for dim2_data in dim1_data:
				new_result.append(dim2_data)
		return new_result

	def split_input_text_by_newline_tab(self, input_text, number):
		"""
		문자열을 \n, tab으로 구분해서 분리한다
		"""
		result = []
		temp_list = str(input_text).split("\n")
		for one_value_1 in temp_list:
			temp = []
			tab_list = str(one_value_1).split("\t")
			for one_value_2 in tab_list:
				temp.append(one_value_2)
			result.append(temp)

		return result

	def split_input_text_by_step(self, input_text, number):
		"""
		문자열을 몇개씩 숫자만큼 분리하기
		['123456'] => ['12','34','56']
		"""
		input_text = str(input_text)
		result = []
		for i in range(0, len(input_text), number):
			result.append(input_text[i:i + number])
		return result

	def split_inputdata_as_num_vs_char(self, raw_data):
		"""
		문자와숫자를 분리해서 리스트로 돌려주는 것이다
		123wer -> ['123','wer']
		"""
		temp = ""
		int_temp = ""
		result = []
		datas = str(raw_data)
		for num in range(len(datas)):
			if num == 0:
				temp = str(datas[num])
			else:
				try:
					fore_var = int(datas[num])
					fore_var_status = "integer"
				except:
					fore_var = datas[num]
					fore_var_status = "string"
				try:
					back_var = int(datas[num - 1])
					back_var_status = "integer"
				except:
					back_var = datas[num - 1]
					back_var_status = "string"

				if fore_var_status == back_var_status:
					temp = temp + datas[num]
				else:
					result.append(temp)
					temp = datas[num]
		if len(temp) > 0:
			result.append(temp)
		return result

	def split_jamo_in_korean(self, input_text):
		"""
		한글의 자음과 모음을 분리
		"""
		result = []
		for one_text in input_text:
			one_byte_data = one_text.encode("utf-8")
			#print("one_byte_data", one_byte_data)
			new_no_1 = (int(one_byte_data[0]) - 234) * 64 * 64
			new_no_2 = (int(one_byte_data[1]) - 128) * 64
			new_no_3 = (int(one_byte_data[2]) - 128)
			#유니코드의 번호로 바꾼다
			#한글의 경우는 44032번째부터 순서대로 표시되어있다
			value = new_no_1 + new_no_2 + new_no_3 - 3072

			#print("value", value)
			chosung = self.var["first_letter"][divmod(value, 588)[0]]  # 초성
			joongsung = self.var["second_letter"][divmod(divmod(value, 588)[1], 28)[0]]  # 중성
			jongsung = self.var["third_letter"][divmod(divmod(value, 588)[1], 28)[1]]  # 종성
			result.append(([chosung, joongsung, jongsung]))
			#print(divmod(value, 588), divmod(divmod(value, 588)[1], 28))
		return result

	def split_list1d_by_group_no(self, input_list1d, step_no):
		"""
		12개의 리스트를
		입력 : [ [1,2,3,4,5,6,7,8,9,10,11,12], 4]를 받으면
				총 4개의 묶읆으로 순서를 섞어서 만들어 주는것
			   [[1,5,9],  [2,6,10],  [3,7,11],  [4,8,12]] 로 만들어 주는것
		"""
		count_no = int(len(input_list1d) / step_no)
		group_no = divmod(len(input_list1d), int(step_no))[0]
		namuji = len(input_list1d) - step_no * group_no
		result = []

		for no in range(count_no):
			temp = input_list1d[no*count_no : no*count_no+count_no]
			result.append(temp)
		if namuji > 0:
			result.append(input_list1d[-namuji:])
		return result

	def split_list1d_by_step(self, input_list1d, step_no):
		"""
		1차원 리스트를 원하는 개수만 큼 자르는 것
		"""
		count_no = int(len(input_list1d) / step_no)
		#group_no = divmod(len(input_list1d), int(step_no))[0]
		namuji = len(input_list1d) - step_no * count_no
		result = []

		for no in range(count_no):
			temp = input_list1d[no*step_no : no*step_no+step_no]
			result.append(temp)
		if namuji > 0:
			result.append(input_list1d[-namuji:])
		return result

	def split_text_as_serial_no(self, input_data, input_list):
		"""
		입력문자를 숫자만큼씨 짤라서 리스트로 만드는 것
		"""
		result = []
		total_len = 0
		start_no = 0
		for no in range(len(input_list)):
			if no != 0:
				start_no = total_len
			end_len = input_list[no]
			result.append(input_data[start_no:start_no + end_len])
			total_len = total_len + end_len
		return result

	def split_text_line(self, input_text):
		"""
		csv 형식의 자료를 읽어오는 것
		""로 들러쌓인것은 숫자나 문자이며, 아닌것은 전부 문자이다
		"""
		result = []
		temp = ""
		num = 0
		my_type = ""
		for no in range(len(input_text)):
			one_char = input_text[no]
			if one_char == '"' and num == 0:
				my_type = "type_2"
			if one_char == '"': num = num + 1
			if one_char == ',':
				if divmod(num, 2)[1] == 0 and my_type == "type_2":
					temp = temp.replace(",", "")
					try:
						temp = int(temp[1:-1])
					except:
						temp = float(temp[1:-1])
					result.append(temp)
					temp = ""
					num = 0
					my_type = ""
				elif my_type == "":
					result.append(temp)
					temp = ""
					num = 0
				else:
					temp = temp + one_char
			else:
				temp = temp + one_char
		return result

	def swap(self, a, b):
		"""
		a,b를 바꾸는 함수이다
		"""
		t = a
		a = b
		b = t
		return [a, b]

	def swap_list1d_for_all_data(self, input_data):
		"""
		input_data : [a, b, c, d]
		result : [b, a, d, c]
		두개의 자료들에 대해서만 자리를 바꾸는 것이다
		"""
		result = []
		for one_data in range(int(len(input_data) / 2)):
			result.append(input_data[one_data * 2 + 1])
			result.append(input_data[one_data * 2])
		return result

	def terms(self):
		"""
		용어정리 : 아래와같은 형태로 용어를 사용한다
		"""

		result = """
		pxy : 커서의 픽셀 좌표
		pwh: 넓이, 높이의 길이를 픽셀단위로 나타낸것
		mouse_click = mouse_down + mouse_up film
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
		index : 0부터 시작되는 번호들
		no : 1부터 시작되는 번호들
		"""
		return result

	def text_encoding_data(self, text, encoding_type):
		"""
		인코딩 상태를 확인하는 것
		사용법 : text_encoding_data("Hello", "utf-8")
		"""
		byte_data = text.encode(encoding_type)
		hex_data_as_str = "".join("{0}".format(hex(c)) for c in byte_data)
		int_data_as_str = "".join(" {0}".format(int(c)) for c in byte_data)
		#print("\"" + text + "\" 전체 문자 길이: {0}".format(len(text)))
		#print("\"" + text + "\" 전체 문자를 표현하는 데 사용한 바이트 수: {0}	바이트".format(len(byte_data)))
		#print("\"" + text + "\" 16 진수 값: {0}".format(hex_data_as_str))
		#print("\"" + text + "\" 10진수 값: {0}".format(int_data_as_str))
		return int_data_as_str

	def draw_as_triangle(self, xyxy, per=100, reverse=1, size=100):
		"""
		삼각형을 만드는것
		# 정삼각형
		# 정삼각형에서 오른쪽이나 왼쪽으로 얼마나 더 간것인지
		# 100이나 -100이면 직삼각형이다
		# 사각형은 왼쪽위에서 오른쪽 아래로 만들어 진다
		"""
		x1, y1, x2, y2 = xyxy
		width = x2 - x1
		height = y2 - y1
		lt = [x1, y1]  # left top
		lb = [x2, y1]  # left bottom
		rt = [x1, y1]  # right top
		rb = [x2, y2]  # right bottom
		tm = [x1, int(y1 + width / 2)]  # 윗쪽의 중간
		lm = [int(x1 + height / 2), y1]  # 윗쪽의 중간
		rm = [int(x1 + height / 2), y1]  # 윗쪽의 중간
		bm = [x2, int(y1 + width / 2)]  # 윗쪽의 중간
		center = [int(x1 + width / 2), int(y1 + height / 2)]


		result = [lb, rb, tm]
		return result

	def read_filenames_in_folder_with_all_properties(self, directory="./"):
		"""
		폴더안의 파일을 이름, 작성한날, 크기, 총경로를 리스트로 만들어서 주는것
		"""
		result = []
		all_files = os.scandir(directory)
		for one in all_files:
			info = one.stat()
			if one.is_dir():
				#	print(directory+,,\\"+one.name)
				temp = self.read_filenames_in_folder_with_all_properties(directory + "\\" + one.name)
				result.extend(temp)
			else:
				#result.append(one)
				result.append([one.name, info.st_mtime, info.st_size, one.path])
		return result


	def find_same_value_in_list2d(self, input_lisd1d_1, input_lisd1d_2):
		"""
		2차원의 자료안에서 입력값이 같은것을 찾아내기
		"""
		result = []
		for one in input_lisd1d_1:
			if one in input_lisd1d_2:
				result.append(one)
		return result

	def get_same_value_for_list2d(self, input_lisd2d_1, input_lisd2d_2, index_list=[1,2]):
		"""
		2 차원의 자료들이 서로 같은것을 삭제하는 것인데,
		모두 같은것이 아니고, 일부분이 같은것을
		골라내는 기능을 만든 것이다
		"""
		semi_result_1 = {}
		for num, value in enumerate(input_lisd2d_1):
			temp_1 = []
			for one in index_list:
				temp_1.append(value[one])
				semi_result_1[num] = [temp_1, value]
		semi_result_2 = {}
		for num, value in enumerate(input_lisd2d_2):
			temp_2 = []
			for one in index_list:
				temp_2.append(value[one])
				semi_result_2[num] = [temp_2, value]
		result = []
		for key, value in semi_result_1.items():
			for key2, value2 in semi_result_2.items ():
				if value[0] == value2[0]:
					if value[1] in result:
						pass
					else:
						result.append(value[1])
		return list(result)

	def sort_by_index_list(self, source, sort_index):
		"""
		sort_index는 정렬되는 순서
		[1,-2,3] ==> 1,2,3으로 정렬을 하는데, 2번째는 역순으로 정렬한다
		"""
		temp = ""
		for one in sort_index:
			if "-" in str(one):
				temp = temp + ("-x[%s], " %(abs(one)))
			else:
				temp = temp + ("x[%s], " %(one))
	
		lam = ("lambda x : (%s)" %temp[:-2])

		result = sorted(source, key=eval(lam))
		return result

	def delete_empty_xline(self, input_list2d):
		"""
		가로나 세로열을 기준으로 값이 없는것을 삭제하기
		입력으로 들어온 2차원의 자료중에서, 가로행이 완전히 빈것을 삭제하는 기능
		"""
		base_no = len(input_list2d[0])
		result = []
		for list_1d in input_list2d:
			check_no = 0
			for value in list_1d:
				if value:
					break
				else:
					check_no = base_no + 1
			if check_no != base_no:
				result.append(list_1d)
		return result

	def delete_empty_yline(self, input_list2d):
		"""
		입력으로 들어온 2차원의 자료중에서, 세로행이 처음부터 끝까지 빈Y열을 삭제하는 기능
		"""
		changed_list_2d = self.change_xylist_to_yxlist(input_list2d)
		temp = self.delete_empty_xline(changed_list_2d)
		result = self.change_xylist_to_yxlist(temp)
		return result

	def read_size_for_list2d(self, input_list2d):
		"""
		입력값으로 온것의 크기를 돌려주는것
		"""
		len_x = len(input_list2d)
		len_y = len(input_list2d[0])
		return [len_x, len_y]

	def extract_list_byindex(self, input_list, position_list):
		"""
		리스트로 넘오온 자료를 원하는 열만 추출하는것
		"""
		result = []
		for one_list in input_list:
			temp = []
			for one in position_list:
				temp.append(one_list[one-1])
			result.append(temp)
		return result

	def split_name_and_title(self, input_name):
		"""
		# 이름과 직함이 같이 있는 입력값을 이름과 직함으로 분리하는 것
		"""
		name = ""
		title = ""
		title_list = ["부장", "이사", "프로", "사원", "대리", "과장", "사장", "차장", "대표", "대표이사", "전무", "전무이사", "공장장"]
		input_name = input_name.strip()  # 공백을 없애는 것
		if len(input_name) > 3:
			for one in title_list:
				title_len = len(one)
				if input_name[-title_len:] == one:
					name = input_name[:-title_len]
					title = input_name[-title_len:]
					break
		return [name, title]

	def delete_list2d_by_index(self, input_list2d, no_list):
		"""
		2차원 자료에서
		원하는 순서들의 자료를 삭제하는 것
		입력형태 : 2차원리스트, [2,5,7]
		"""
		no_list.sort()
		no_list.reverse()
		for one in no_list:
			for x in range(len(input_list2d)):
				del input_list2d[x][one]
		return input_list2d

	def change_list2d_by_index(self, input_list2d, input_no_list):
		"""
		# input_no_list.sort()
		# input_no_list.reverse()
		"""
		for before, after in input_no_list:
			for no in range(len(input_list2d)):
				value1 = input_list2d[no][before]
				value2 = input_list2d[no][after]
				input_list2d[no][before] = value2
				input_list2d[no][after] = value1
		return input_list2d

	def check_price(self, input_price):
		"""
		"""
		# 백만원단위, 전만원단위, 억단위로 구분
		input_price = int(input_price)
		if input_price > 100000000:
			result = str('{:.If}'.format(input_price / 100000000)) + "억원"
		elif input_price > 10000000:
			result = str('{: .0f}'.format(input_price / 1000000)) + "백만원"
		elif input_price > 1000000:
			result = str('{:.If}'.format(input_price / 1000000)) + "백만원"
		return result

	def split_value_to_str_num(self, input_text):
		"""
		문자와 숫자를 분리하는 것
		"""
		re_com_num = re.compile("[a-zA-Z]+|\d+")
		result = re_com_num.findall(input_text)
		return result