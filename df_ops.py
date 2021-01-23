import sys
import csv
import json
import plotly
import plotly.graph_objects as go
import pandas as pd
import numpy as np

class DfWrapper:
	def __init__(self, student_df, teacher_df, ta_df, zby1_df):
		self.student_df = student_df
		self.teacher_df = teacher_df
		self.ta_df = ta_df
		self.zby1_df = zby1_df

		# Add infection rate column to student df
		student_df['Infection Rate'] = 0


	# sibilings of person X
	# common classes of person X in period Y
	# common afterschool activities of person X
	# all people in grade X
	# all people in class C for period Y

	def getsiblings(self, studentid):
		rowindex = studentid - 1
		lastname = self.student_df.iat[rowindex, 1]
		
		siblings = self.student_df.loc[self.student_df['Last Name'] == lastname]
		siblings_list = siblings['Student Number'].values.tolist()
		siblings_list.remove(studentid)
		return siblings_list

	def get_same_grade_students(self, grade):
		query = self.student_df.loc[self.student_df['Grade'] == grade]
		students_list = query['Student Number'].values.tolist()
		return students_list

	def printStudentHead(self):
		print(self.student_df.head)


