# -*- coding: utf-8 -*-
import win32com.client #pywin32의 모듈
import win32

class ganada:
	"""
	MS워드를 사용하기 쉽게하기위해 만든 모듈입니다,
	차후에는 다른 Libero및 한글의 연동또한 만들 예정입니다
	activedoc : 현재 선택된 워드문서
	doc : 여러문서중에 선택한 하나의 문서
	add : 어떤것을 만들어서 다른 조정없이 기본기능으로 새롭게 추가하는 것
	lx : location x, 하나의 문서로 된것의 문자의 위치를 나타내는 것
	xy : selection의 처음과 끝위치
	xl : x는 시작위치, l은 길이
	"""
	def	__init__(self, file_name=""):
		# 공통으로 사용할 변수들을 설정하는 것이다
		self.vars = {}
		self.table = ""
		self.range = ""
		#워드를 실행시킵니다
		self.word_program = win32com.client.dynamic.Dispatch('Word.Application')
		self.word_program.Visible = 1

		if file_name =="":
			#만약 오픈된 워드가 하나도 없으면,새로운 빈 워드를 만든다
			try:
				self.activedoc = self.word_program.ActiveDocument
			except:
				self.word_program.Documents.Add()
				self.activedoc = self.word_program.ActiveDocument
				self.selection = self.word_program.Section()
		else:
			self.word_program.Documents.Open(file_name)
			self.activedoc = self.word_program.ActiveDocument
			self.word_program.ActiveDocument.ActiveWindow.View.Type = 3
			self.selection = self.word_program.Section()

	def add_document_new(self):
		"""
		새 문서를 하나더 만듦
		"""
		self.word_program.Documents.Add()

	def check_cursor(self):
		"""
		현재 커서의 위치를 돌려준다
		영역이 선택되지 않으면 selection은 cursor를 가르킨다
		"""
		result = self.check_selection()
		return result

	def check_doc(self, file_name=""):
		"""
		만약 오픈된 워드가 하나도 없으면,새로운 빈 워드를 만든다
		"""
		self.check_file(file_name)

	def check_file(self, file_name=""):
		"""
		만약 오픈된 워드가 하나도 없으면,새로운 빈 워드를 만든다
		"""
		if file_name =="":
			try:
				self.activedoc = self.word_program.ActiveDocument
			except:
				self.word_program.Documents.Add()
				self.activedoc = self.word_program.ActiveDocument
		else:
			self.word_program.Documents.Open(file_name)
			self.activedoc = self.word_program.ActiveDocument
			self.word_program.ActiveDocument.ActiveWindow.View.Type = 3

	def check_selection(self):
		"""
		영역이 선택되지 않으면 selection은 cursor를 가르킨다
		"""
		self.my_selection = self.word_program.Selection
		result = self.my_selection
		self.vars["cursor"] = result
		self.selection = result
		return result

	def close(self):
		"""
		현재 활성화된 문서를 닫는다
		"""
		self.activedoc.Close()

	def count_document_all(self):
		"""
		테이블의 총 갯수
		"""
		result = self.word_program.Documents.Count
		return result

	def count_letter_nos_in_selection(self):
		"""
		현재 선택된 영역의 글자수
		갯수를 세는것은 count를 사용한다
		"""
		result = self.word_program.Selection.Characters.Count
		return result

	def count_paragraph_all(self):
		"""
		현재 선택한 문서의 문단의 갯수를 갖고온다
		"""
		result = self.activedoc.Paragraphs.Count
		return result

	def count_table_all(self):
		"""
		테이블의 총 갯수
		"""
		result = self.activedoc.Tables.Count
		return result

	def cut_selection(self):
		"""
		선택한 영역을 잘라내기
		"""
		self.word_program.Selection.Cut()

	def get_basic_properties_for_document(self):
		"""
		문서의 기본적인 속성을 돌려준다
		"""
		doc_name = self.activedoc.Name
		doc_fullname = self.activedoc.FullName
		doc_path = self.activedoc.Path
		return [doc_name, doc_fullname, doc_path]

	def get_document_name_all(self):
		"""
		모든 문서의 이름을 돌려준다
		"""
		doc_no = self.word_program.Documents.Count
		result = []
		for no in range(doc_no):
			result.append(self.word_program.Documents(no+1).Name)
		return result

	def get_name_for_activedoc(self):
		"""
		현재 선택된 문서의 이름을 돌려준다
		"""
		result = self.word_program.ActiveDocument.Name
		return result

	def get_paragraph_index_for_selection(self):
		"""
		선택된 문단이 전체문서중 몇번째 문단인 돌려준다
		"""
		result = self.word_program.Selection.Range.Information(10)
		return result

	def get_paragraph_object_all(self):
		"""
		모든 문단객체를 돌려준다
		"""
		para_objs = self.activedoc.Paragraphs
		return para_objs

	def get_paragraph_object_by_index(self, input_no):
		"""
		번호로 문단객체를 갖고온다
		"""
		para_obj = self.activedoc.Paragraphs(input_no)
		return para_obj

	def get_table_obj_all(self):
		"""
		모든 테이블객체를 돌려준다
		"""
		table_objs = self.activedoc.Tables
		return table_objs

	def get_table_obj_by_index(self, input_no=1):
		"""
		표의 갯수를 돌려준다
		"""
		table_obj = self.activedoc.Tables(input_no)
		return table_obj

	def get_xy_for_selection(self):
		"""
		선택된 영역의 위치값을 갖고온다
		"""
		x = self.word_program.Selection.Start
		y = self.word_program.Selection.End
		return [x, y]

	def insert_new_line_char_at_cursor(self):
		"""
		현재 커서의 위치에 줄바꿈문자를 넣어서 새로운 문단을 만드는 것이다
		"""
		self.word_program.Selection.InsertBefore("\r\n")

	def insert_table_after_paragraph(self, para_no , table_xy = [5,5]):
		"""
		선택한 문단뒤에 테이블을 만든다
		"""
		myrange = self.activedoc.Paragraphs(para_no).Range
		mytable = self.activedoc.Tables.Add(myrange, table_xy[0], table_xy[1])
		mytable.AutoFormat(36)

	def make_new_line_at_cursor(self):
		"""
		현재 커서의 위치에 줄바꿈문자를 넣어서 새로운 문단을 만드는 것이다
		"""
		self.insert_new_line_char_at_cursor()

	def move_cursor_to_end_of_document(self):
		"""
		영역이 선택되지 않으면 selection은 cursor를 가르킨다
		"""
		self.vars["cursor"] = self.activedoc.Range()
		self.vars["cursor"].Move()

	def move_next_line_for_selection_by_num(self, input_no=1):
		"""
		선택된 라인의 다음 줄로 이동하는 것
		계속해서 사용하면 한줄씩 내려갈수 있다
		"""
		self.word_program.Selection.MoveRight(Unit=win32com.client.constants.wdSentence, Count=input_no)

	def quit(self):
		"""
		워드 프로그램 종료하기
		"""
		self.word_program.Quit()

	def quit_word_program(self):
		"""
		워드 프로그램을 끈다
		"""
		self.word_program.Quit()

	def read_all_text_in_document(self):
		"""
		현재 문서에서 모든 텍스트만 돌려준다
		"""
		result = self.activedoc.Range().Text
		return result

	def read_text_for_all_paragraph_as_list1d_style(self):
		"""
		모든 paragraph를 리스트로 만들어서 돌려주는 것
		"""
		result = []
		para_nums = self.activedoc.Paragraphs.Count
		for i in range(para_nums):
			result.append(self.activedoc.Paragraphs(i).Range.Text)
		return result

	def read_text_for_paragraph_by_index(self, input_no):
		"""
		paragraph 번호에 해당하는 모든 text 를 갖고오는것
		"""
		aaa = self.activedoc.Paragraphs(input_no)
		result = aaa.Range.Text
		return result

	def read_text_from_para1_to_para2(self, para1_index, para2_index):
		"""
		선택한 문단 사이의 글을 돌려준다
		"""
		start = self.activedoc.Paragraphs(para1_index).Range.Start
		end = self.activedoc.Paragraphs(para2_index).Range.End
		result = self.activedoc.Range(start, end).Text
		return result

	def read_text_in_current_paragraph(self):
		"""
		현재 커서가 있는 문단의 전체 text를 돌려줍니다
		"""
		current_para_index = self.word_program.Selection.Range.Information(10)
		result = self.word_program.Selection.Paragraphs(current_para_index).Range.Text
		return result

	def read_text_in_document_by_lxly(self, lxly):
		"""
		전체 문자중에 몇번째의 것부터 읽어오는것
		"""
		result = self.activedoc.Range(lxly[0], lxly[1]).Text
		return result

	def read_text_in_paragraph_by_index(self, input_no):
		"""
		현재 커서가 있는 첫번째 문단의 text를 돌려줍니다
		"""
		result = self.word_program.Selection.Paragraphs(input_no).Range.Text
		return result

	def read_text_in_paragraph_by_xlen(self, input_index, x, length):
		"""
		선택된 문단에서 몇번째의 글을 선택하는 것
		일정 영역의 자료를 갖고오는 3
		paragraph를 선택한다, 없으면 맨처음부터
		"""
		paragraph = self.activedoc.Paragraphs(input_index)
		# 맨앞에서 몇번째부터, 얼마의 길이를 선택할지를 선정
		x_no = paragraph.Range.Start + x - 1
		y_no = paragraph.Range.Start + x + length - 1
		result = self.activedoc.Range(x_no, y_no).Text
		return result

	def read_text_in_selection(self):
		"""
		선택된 영역의 값을 갖고오는 것
		"""
		result = self.word_program.Selection.range.Text
		return result

	def read_text_in_table_by_lxly(self, table_index, lxly):
		"""
		테이블 번호에서 값을 읽어오는것
		"""
		table = self.activedoc.Tables(table_index)
		result = table.Cell(Row=lxly[0], Column=lxly[1]).Range.Text
		#str문자들은 맨 마지막에 끝이라는 문자가 자동으로 들어가서, 이것을 없애야 표현이 잘된다
		return result[:-1]

	def replace_text_for_selection_text(self, input_value):
		"""
		선택한 영역의 글자를 변경하는 것
		"""
		self.word_program.Selection.Delete()
		self.word_program.Selection.InsertBefore(input_value)

	def save(self):
		"""
		저장
		"""
		self.activedoc.Save()

	def save_as(self, file_name=""):
		"""
		화일 다른이름으로 저장
		"""
		self.activedoc.SaveAs(file_name)

	def select_document_by_name(self, input_name):
		"""
		현재 open된 문서중 이름으로 active문서로 활성화 시키기
		"""
		self.activedoc = self.word_program.Documents(input_name)
		#self.activedoc.Visible = True
		self.activedoc.Activate()
		#self.activedoc.Select()


	def select_xlen(self, x, lengh):
		"""
		영역을 선택하는 것
		맨앞에서 몇번째부터，얼마의 길이를 선택할지를 선정
		"""
		self.activedoc.Range(x, x+lengh).Select()

	def select_xlen_from_cursor(self, x, length):
		"""
		현재커서의 위치에서 몇번째 문자로 에서부터 선택시작
		"""
		self.word_program.Selection.Start = x
		self.word_program.Selection.End = x + length - 1

	def select_xlen_from_paragraph(self, para_no, y, length):
		"""
		문단 번호로 문단 전체의 영역을 선택하는 것
		paragraph 를 선택한다, 없으면 맨처음부터
		"""
		paragraph = self.activedoc.Paragraphs(para_no)
		#맨앞에서 몇번째부터，얼마의 길이를 선택할지를 선정
		x = paragraph.Range.Start+y-1
		y = paragraph.Range.Start+y+length-1
		self.vars["new_range"] = self.activedoc.Range(x, y).Select()

	def set_base_doc_as_activedocument(self):
		"""
		현재 활성화된 문서를 기본 문서로 설정
		"""
		self.activedoc = self.word_program.ActiveDocument

	def set_font_name_for_selection(self, input_no="Georgia"):
		"""
		선택한 영역의 글씨체를 설정
		"""
		self.word_program.Selection.Font.Name = input_no

	def set_font_name_for_table_xy(self, table_index, cell_index, input_no="Georgia"):
		"""
		테이블의 xy의 폰트를 설정
		"""
		table = self.word_program.Tables(table_index)
		table(cell_index).Font.Name = input_no

	def set_font_size_for_selection(self, input_no=10):
		"""
		선택한것의 폰트 크기
		"""
		self.word_program.Selection.Font.Size = input_no

	def set_font_size_for_table(self, table_index, font_size=10):
		"""
		표에 대한 글자크기를 설정
		"""
		table = self.activedoc.Tables(table_index)
		table.Font.Size = font_size

	def set_margin_bottom_for_page_setup(self, input_value=20):
		"""
		페이지셋업 : 아래쪽 띄우기
		"""
		self.activedoc.PageSetup.BottomMargin = input_value

	def set_margin_left_for_page_setup(self, input_value=20):
		"""
		페이지셋업 : 왼쪽 띄우기
		"""
		self.activedoc.PageSetup.LeftMargin = input_value

	def set_margin_right_for_page_setup(self, input_value=20):
		"""
		페이지셋업 : 오른쪽 띄우기
		"""
		self.activedoc.PageSetup.RightMargin = input_value

	def set_margin_top_for_page_setup(self, input_value=20):
		"""
		페이지셋업 : 위쪽 띄우기
		"""
		self.activedoc.PageSetup.TopMargin = input_value

	def set_new_selection_by_lxly(self, lxly=[1,8]):
		"""
		현재선택된것에서 위치에서 몇번째 문자로 에서부터 선택시작
		"""
		self.word_program.Selection.Start = lxly[0]
		self.word_program.Selection.End = lxly[1]

	def set_orientation_for_page_setup(self, input_value=20):
		"""
		페이지의 회전을 설정
		"""
		self.activedoc.PageSetup.Orientation = input_value

	def set_selection_by_lxly(self, lx, ly):
		"""
		맨앞에서 몇번째 글자를 선택하는 것
		"""
		self.word_program.Selection.Start = lx
		self.word_program.Selection.End = ly

	def set_selection_by_range(self):
		"""
		range 객체의 일정부분을 영역으로 선택
		"""
		self.selection = self.activedoc.Range(0, 0)

	def set_selection_in_table_by_xy(self, table_index, table_xy, x, lengh):
		"""
		테이블안의 셀안의 값을 선택하는 방법
		"""
		table = self.activedoc.Tables(table_index)
		range = table.Cell(table_xy[0], table_xy[1]).Range.Characters(x)
		range.End = table.Cell(table_xy[0], table_xy[1]).Range.Characters(x + lengh - 1).End
		range.Select()

	def set_style_for_selection(self, input_no="제목 1"):
		"""
		스타일 지정하는 코드
		"""
		self.word_program.Selection.Style = self.activedoc.Styles(input_no)

	def write_text_at_left_for_selection(self, input_value):
		"""
		선택한것의 앞에 글씨넣기
		"""
		self.word_program.Selection.InsertBefore(input_value)

	def write_text_at_right_for_selection(self, input_value):
		"""
		선택한것의 뒤에 글씨넣기
		"""
		self.word_program.Selection.InsertAfter(input_value)

	def write_text_in_table_by_cell_index(self, table_index, input_no=1, input_text=""):
		"""
		테이블의 셀의 index로 값입력하기
		"""
		table = self.activedoc.Tables(table_index)
		table(input_no).Range.Text = input_text
	def write_text_in_table_by_xy(self, table_index="", xy="", input_text=""):
		"""
		테이블의 셀에 글씨 입력하기
		"""
		table = self.activedoc.Tables(table_index)
		table.Cell(xy[0], xy[1]).Range.Text = input_text

	############################################################

	def get_no_of_paragraphs_in_document(self):
		result = self.activedoc.Paragraphs.Count
		return result

	def read_text_by_paragraph_no(self, input_no):
		# paragraph번호에 해당하는 모든 text를 갖고오는것
		aaa = self.activedoc.Paragraphs(input_no)
		result = aaa.Range.Text
		return result

	def set_selection(self, para_no, y, length):
		# 영역을 선택하는 것
		# paragraph를 선택한다, 없으면 맨처음부터
		vars["paragraph"] = self.activedoc.Paragraphs(para_no)
		# 맨앞에서 몇번째부터, 얼마의 길이를 선택할지를 선정
		x = vars["paragraph"].Range.Start + y - 1
		y = vars["paragraph"].Range.Start + y + length - 1
		vars["new_range"] = self.activedoc.Range(x, y).Select()

	def read_text_by_position(self, para_no, y, length):
		# 일정 영역의 자료를 갖고오는 것
		# paragraph를 선택한다, 없으면 맨처음부터
		vars["paragraph"] = self.activedoc.Paragraphs(para_no)
		# 맨앞에서 몇번째부터, 얼마의 길이를 선택할지를 선정
		x = vars["paragraph"].Range.Start + y - 1
		y = vars["paragraph"].Range.Start + y + length - 1
		result = self.activedoc.Range(x, y).Text
		return result


	def read_value_in_selection(self):
		# 선탹된 영역의 값을 갖고오는 것이다
		result = self.self.word_program.Selection.range.Text
		return result

	def get_paragraph_no_for_selection(self):
		# 선탹된 영역의 값을 갖고오는 것이다
		result = self.self.word_program.Selection.Range.Information(10)  # paragraph no를 돌려준다
		return result


	def insert_table(self, para_no=2):
		myRange = self.activedoc.Paragraphs(1).Range
		myTable = self.activedoc.Tables.Add(myRange, 5, 5)
		myTable.AutoFormat(36)

	def read_text_in_range(self, x, y):
		result = self.activedoc.Range(x, y).Text

	def set_font_size_in_selection(self, input_no):
		# 선택한 영역의 문자크기를 설정
		self.activedoc.Selection.Font.Size = input_no

	def set_font_in_selection(self, input_no):
		# 선택한 영역의 문자크기를 설정
		self.activedoc.Selection.Font.Name = input_no

	def get_current_paragraph(self):
		# 현재 커서가 있는 영역의 첫번째 문단의 text를 돌려준다
		result = self.activedoc.Selection.Paragraphs(1).Range.Text
		return result

	def change_word(self, before, after):
		self.activedoc.Selection.GoTo(What=win32.constants.wdGoToSection, Which=win32.constants.wdGoToFirst)
		self.activedoc.Selection.Find.Text = "찾을 단어"  # 찾을 단어를 찾는다.
		self.activedoc.Selection.Find.Replacement.Text = ""  # 찾을 단어를 지운다.
		self.activedoc.Selection.Find.Execute(Replace=1, Forward=True)
		self.activedoc.Selection.InsertAfter("Sucess")  # 해당 위치에 삽입하고자 하는 단어를 입력한다.

	def select_current_paragraph(self):
		current_paragraph = 0
		self.activedoc.Selection.StartOf(Unit := current_paragraph)
		self.activedoc.Selection.MoveEnd(Unit := current_paragraph)
		self.activedoc.Selection.Copy()

	def write_text_at_cursor_to_right(self, input_value):
		# 선택한것의 뒤에 글씨넣기
		self.activedoc.Selection.InsertAfter(input_value)

	def write_text_at_cursor_to_left(self, input_value):
		# 선택한것의 뒤에 글씨넣기
		self.activedoc.Selection.InsertBefore(input_value)

	def read_selection(self):
		# 현재 커서가 위치한곳의 뒷글자 하나를 나타낸다
		# 선택한 영역이 떨어져있으면 하나로 인식
		rng_obj = self.word_program.Selection
		# 선택한것중 제일 나중에 선택된것을 갖는다
		print("제일 나중에 선택된것은 ==> ", rng_obj.Text)
		ddd = self.word_program.Selection.Characters
		print("aaa ==> ", ddd.Count, ddd(1).Item)

		# 커서를 한줄 이동시킨다
		# rng_obj.MoveDown()

		# 선택한것중 제일 나중에 선택된것을 갖는다
		print("제일 나중에 선택된것은 ==> ", rng_obj.Text)

		paras_obj = rng_obj.Paragraphs
		# 선택한 영역안의 파라그래프의 숫자
		print("선택한 문장의 갯수 ==> ", paras_obj.Count)

		for no in range(paras_obj.Count):
			new_rng_obj = rng_obj.Paragraphs(no + 1).Range
			print("첫번째 ==> ", new_rng_obj)

		for one in rng_obj.Paragraphs:
			print("번호", one)
			self.word_program.Selection.Start = one.Range.Start
			self.word_program.Selection.End = one.Range.End
			print("제일 나중에 선택된것은 ==> ", self.word_program.Selection.Text)

		for one in range(paras_obj.Count):
			print(paras_obj(one + 1))
		rng_1_obj = paras_obj(1)
		print(rng_obj, rng_obj.Start, rng_obj.End, paras_obj.Count, rng_1_obj)


	def get_paragraph_by_no(self, input_no):
		vars["paragraph"] = self.word_program.Selection.Paragraphs(input_no)

	def select_all_text(self):
		self.selection = self.word_program.Selection.WholeStory

	def set_selection_by_field_no(self, input_no):
		self.selection = self.word_program.Paragraphs(input_no).Selection()

	def write_value(self, input_text="hfs1234234234;lmk"):
		# 문서의 제일 뒷부분에 글을 넣는것
		self.activedoc.Content.InsertAfter(input_text)

	def write_range_value(self, para_no=1, input_text="hfs1234234234;lmk"):
		# 문서의 제일 뒷부분에 글을 넣는것
		self.activedoc.Paragraphs(para_no).Content.InsertAfter(input_text)

	def release_selection(self):
		# selection을 해제해 주는것
		self.activedoc.Selection.Collapse(win32com.client.constants.wdCollapseEnd)

	def get_current_cursor(self):
		result = self.word_program.Selection.Character.Count  # 커서의 현재위치 확인
		print("현재 커서위치는 ==> ", result)
		return result

	def get_range_text(self):
		result = self.activedoc.Range().Text
		print("모든 text ==> ", result)
		return result

	def set_range(self, start_no, end_no):
		self.range = self.activedoc.Range(start_no, end_no)

	def write_range_value_1(self, start_no, end_no, input_text):
		aaa = self.activedoc.Paragraphs(int(vars["para_no"])).Selection.Start

	# self.activedoc.Paragraphs(vars["para_no"]).Selection.End = end_no
	# self.activedoc.Selection.InsertAfter(input_text)

	def selection(self):
		pass

	def InsertAfter(self):
		self.activedoc.Selection.InsertAfter("커서 뒤에 삽입되었어요")

	def InsertBefore(self):
		self.activedoc.Selection.InsertBefore("커서 앞에 삽입되었어요")

	def no_of_letters(self):
		result = self.activedoc.Selection.Characters.Count
		return result

	def move_cursor_from_start(self, input_no=8):
		self.activedoc.Selection.Start = input_no

	def move_cursor_from_end(self, input_no=8):
		self.activedoc.Selection.End = input_no

	def set_font_name(self, input_no="Georgia"):
		self.activedoc.Selection.Font.Name = input_no

	def set_style(self, input_no="제목 1"):
		self.activedoc.Selection.Style = self.activedoc.Styles(input_no)  # 스타일 지정하는 코드

	def set_selection_by_paragraph(self):
		self.word_program.Selection = self.activedoc.Range(0, 0)

	def move_cursor_by_bookmark(self):
		pass

	def write_xy_value(self, xy, input_text):
		self.table.Cell(int(xy[0]), int(xy[1])).Range.Text = str(input_text)

	def set_table_position(self, xy, input_text):
		pass

	def make_table(self, xy):
		self.table = self.range.Tables.Add(self.range, xy[0], xy[1])

	def set_orientation(self, input_value=20):
		# 페이지의 회전을 설정
		self.activedoc.PageSetup.Orientation = input_value

	def set_LeftMargin(self, input_value=20):
		# 왼쪽 띄우기
		self.activedoc.PageSetup.LeftMargin = input_value

	def set_TopMargin(self, input_value=20):
		self.activedoc.PageSetup.TopMargin = input_value

	def set_BottomMargin(self, input_value=20):
		self.activedoc.PageSetup.BottomMargin = input_value

	def set_RightMargin(self, input_value=20):
		self.activedoc.PageSetup.RightMargin = input_value

	def set_font_size(self, input_no=10):
		# 선택한것의 폰트 크기
		self.activedoc.Selection.Font.Size = input_no

	def move_next_line(self, input_no=1):
		# 다음 줄로 이동하는 것
		self.activedoc.Selection.MoveRight(Unit=win32com.client.constants.wdSentence, Count=input_no)

	def read_range_text(self):
		start = self.activedoc.Paragraphs(1).Range.Start
		end = self.activedoc.Paragraphs(10).Range.End
		result = self.activedoc.Range(start, end).Text

	def check_table(self, file_name=""):
		self.table = self.activedoc.Paragraphs

	def cell_text(self, input_no="abc"):
		self.table(input_no).Range.Text = input_no

	def cell_font_size(self, input_no=1):
		self.table(input_no).Font.Size = input_no

	def cell_font_name(self, input_no="Georgia"):
		self.table(input_no).Font.Name = input_no

	def get_all_tables(self):
		vars["all_table_objects"] = self.activedoc.Tables

	def select_table_by_no(self, input_no=1):
		self.table = vars["all_table_objects"][input_no]

	def save(self, file_name):
		self.activedoc.SaveAs(file_name)

	def saveas(self, file_name):
		self.activedoc.SaveAs(file_name)

	def cloase(self):
		self.activedoc.Close()

	def new_word(self):
		self.activedoc = self.word_program.Documents.Add()

	def get_basic_properties(self):
		doc_name = self.activedoc.Name
		doc_fullname = self.activedoc.FullName
		doc_path = self.activedoc.Path
		return [doc_name, doc_fullname, doc_path]

	def doc_nos(self):
		aaa = self.word_program.Documents.Count
		# Application.Documents(1).Name
		return aaa