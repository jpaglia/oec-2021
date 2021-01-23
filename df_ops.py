import sys
import csv
import json
import plotly
import plotly.graph_objects as go
import pandas as pd
import numpy as np

class DfWrapper:
	def __init__(self, student_df, teacher_df, ta_df, zby1_df):
		self.student_df = student_df[student_df['Student Number'].notna()]
		self.teacher_df = teacher_df[teacher_df['Teacher Number'].notna()]
		self.ta_df = ta_df[ta_df['Last Name'].notna()]
		self.zby1_df = zby1_df[zby1_df['Student ID'].notna()]

		# Add infection rate columns to student df
		self.student_df['Infection Rate P1'] = 0
		self.student_df['Infection Rate P2'] = 0
		self.student_df['Infection Rate P3'] = 0
		self.student_df['Infection Rate P4'] = 0

		# Print the resulting dataframe
		print(str(self.student_df))


	# sibilings of person X
	# common classes of person X in period Y
	# common afterschool activities of person X
	# all people in grade X
	# all people in class C for period Y

	def getsiblings(self, studentid):
		rowindex = studentid - 1
		lastname = self.student_df.at[rowindex, 'Last Name']
		
		siblings = self.student_df.loc[self.student_df['Last Name'] == lastname]
		siblings_list = siblings['Student Number'].values.tolist()
		siblings_list.remove(studentid)

		return siblings_list

	# Get a list of all the classes within a period `period`
	# `period` must be in {1,2,3,4}
	# returns a list of class names
	def get_class_list(self, period):
		# Generate column header
		period_col_header = "Period " + str(period) + " Class" 

		classes = self.student_df[period_col_header].tolist()
		return classes


	def printStudentHead(self):
		print(self.student_df.head)


