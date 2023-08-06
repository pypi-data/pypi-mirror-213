# -*- coding: utf-8 -*-

import win32com.client
import win32gui
from halmoney import scolor
from halmoney import basic_data

vars = {}  # 공통으로 사용할 변수들을 설정하는 것이다
basic = basic_data.basic_data()
common_data = basic.basic_data()

class pcell_dot:
	def __init__(self, file_name=""):
		vars["word"] = win32com.client.dynamic.Dispatch('Word.Application')
		vars["word"].Visible = 1

	def save(self):
		vars["doc"].SaveAs("test.docx")

	def saveas(self):
		vars["doc"].SaveAs("test.docx")

	def cloase(self):
		vars["doc"].Close()

	def quit(self):
		vars["doc"].Quit()

	class doc:
		def __init__(self, file_name=""):
			if file_name =="":
				vars["doc"] = vars["word"].ActiveDocument

		def new_word(self):
			vars["doc"] = vars["word"].Documents.Add()

		def set_font_size(self, input_value = 10):
			vars["doc"].Content.Font.Size = input_value

		def get_basic_properties(self):
			doc_name = vars["doc"].Name
			doc_fullname = vars["doc"].FullName
			doc_path = vars["doc"].Path
			return [doc_name, doc_fullname, doc_path]

		def doc_nos(self):
			aaa = vars["word"].Documents.Count
			#Application.Documents(1).Name
			return aaa

		def get_paragraph_by_no(self, input_no):
			aaa = vars["word"].Paragraphs(input_no)


	class page_setup:
		pass

		def set_orientation(self, input_value = 20):
			vars["doc"].PageSetup.Orientation = input_value

		def set_LeftMargin(self, input_value = 20):
			vars["doc"].PageSetup.LeftMargin = input_value

		def set_TopMargin(self, input_value = 20):
			vars["doc"].PageSetup.TopMargin = input_value

		def set_BottomMargin(self, input_value = 20):
			vars["doc"].PageSetup.BottomMargin = input_value

		def set_RightMargin(self, input_value = 20):
			vars["doc"].PageSetup.RightMargin = input_value

	class range:
		def __init__(self, file_name=""):
			if file_name =="":
				vars["doc"] = vars["word"].ActiveDocument
		def selection(self):
			pass

		def InsertAfter(self):
			vars["doc"].Selection.InsertAfter("커서 뒤에 삽입되었어요")

		def InsertBefore(self):
			vars["doc"].Selection.InsertBefore("커서 앞에 삽입되었어요")

		def no_of_letters(self):
			result = vars["doc"].Selection.Characters.Count
			return result

		def move_cursor_from_start(self, input_no = 8):
			vars["doc"].Selection.Start =input_no

		def move_cursor_from_end (self, input_no = 8):
			vars["doc"].Selection.End =input_no

		def set_font_size (self, input_no = 10):
			vars["doc"].Selection.Font.Size =input_no

		def set_font_name (self, input_no = "Georgia"):
			vars["doc"].Selection.Font.Name =input_no

		def set_style (self, input_no = "제목 1"):
			vars["doc"].Selection.Style = vars["doc"].Styles(input_no) # 스타일 지정하는 코드

		def move_next_line(self, input_no = 1):
			vars["doc"].Selection.MoveRight(Unit=win32com.client.constants.wdSentence, Count=input_no)

		def set_selection(self):
			vars["selection"] = vars["doc"].Range(0, 0)

		def set_selection_by_paragraph(self):
			vars["selection"] = vars["doc"].Range(0, 0)



		def read_range_text(self):
			start = vars["doc"].Paragraphs(1).Range.Start
			end = vars["doc"].Paragraphs(10).Range.End
			result = vars["doc"].Range(start, end).Text

	class table:
		def __init__(self, file_name=""):
			vars["table"] = vars["doc"].Paragraphs

		def cell_text(self, input_no = "abc"):
			vars["table"](input_no).Range.Text = input_no

		def cell_font_size(self, input_no = 1):
			vars["table"](input_no).Font.Size = input_no

		def cell_font_name(self, input_no = "Georgia"):
			vars["table"](input_no).Font.Name = input_no

		def get_all_tables(self):
			vars["all_table_objects"] = vars["doc"].Tables

		def select_table_by_no(self, input_no=1):
			vars["table"] = vars["all_table_objects"][input_no]


wordapp = win32com.client.Dispatch("Word.Application")
wordapp.Visible = 1
worddoc = wordapp.ActiveDocument
#worddoc.PageSetup.Orientation = 1
#worddoc.PageSetup.BookFoldPrinting = 1
#worddoc.Content.Font.Size = 11
#worddoc.Content.Paragraphs.TabStops.Add (150)
#worddoc.Content.Text = "Hello, I am a textaaa!"

start = worddoc.Paragraphs(1).Range.Start
end = worddoc.Paragraphs(1).Range.End
worddoc.Range(start, end).Text = 'asdasdasdasdasd\nsfsdfzxczxczxczxczxczxczxczxczxczxczxczxczxczxczxczxczxczxczxczxsdfsdf\nsdfsdf'

start = worddoc.Paragraphs(3).Range.Start
end = worddoc.Paragraphs(3).Range.End
worddoc.Range(start, end).Text = '2222222222222222'
print(worddoc.Paragraphs.Count)

#location = worddoc.Range()
#location.Collapse(1)
#location.Paragraphs.Add()
#location.Collapse(1)

#table = location.Tables.Add (location, 3, 4)
#table.ApplyStyleHeadingRows = 1
#table.AutoFormat(16)
#table.Cell(1,1).Range.InsertAfter("Teacher")
"""
location1 = worddoc.Range()
location1.Paragraphs.Add()
location1.Collapse(1)
table = location1.Tables.Add (location1, 3, 4)
table.ApplyStyleHeadingRows = 1
table.AutoFormat(16)
table.Cell(1,1).Range.InsertAfter("Teacher1")
#worddoc.Content.MoveEnd
worddoc.Close() # Close the Word Document (a save-Dialog pops up)
wordapp.Quit() # Close the Word Application
"""