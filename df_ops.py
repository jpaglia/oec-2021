import sys
import csv
import json
import plotly
import plotly.graph_objects as go
import pandas as pd
import numpy as np

class DfWrapper:
	def __init__(self, student_df, teacher_df, ta_df, zby1_df):
		student_df.dropna(subset=['Student Number'], inplace=True)
		teacher_df.dropna(subset=['Teacher Number'], inplace=True)
		ta_df.dropna(subset=['Last Name'], inplace=True)
		zby1_df.dropna(subset=['Student ID'], inplace=True)

		self.student_df = student_df
		self.teacher_df = teacher_df
		self.ta_df = ta_df
		self.zby1_df = zby1_df

		# Add infection rate columns to student df
		self.student_df['Infection Rate P1'] = 0.0
		self.student_df['Infection Rate P2'] = 0.0
		self.student_df['Infection Rate P2.5'] = 0.0
		self.student_df['Infection Rate P3'] = 0.0
		self.student_df['Infection Rate P4'] = 0.0
		self.student_df['Infection Rate P5'] = 0.0
		self.student_df['Infection Rate P6'] = 0.0

		# Print the resulting dataframe
		print(str(self.student_df))

	# sibilings of person X
	# common classes of person X in period Y
	# common afterschool activities of person X
	# all people in grade X
	# all people in class C for period Y

	def get_siblings(self, studentid):
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

	# Updates infection % value for a certain student for a certain period
	# `period` must be in {1, 2, 2.5, 3, 4, 5, 6}
	# Where 2.5 => lunch, 5 => extra curriculars, and 6 => after school
	def update_infection_value(self, studentid, period, value):
		rowindex = studentid - 1
		infection_col_name = 'Infection Rate P' + str(period)
		
		self.student_df.at[rowindex, infection_col_name] = str(value)
		
		# print(self.student_df.head)
		# print("Actual value:{}".format(str(self.student_df.at[rowindex, infection_col_name])))
		# print("col name:<{}>, value={}".format(infection_col_name, value))

	def print_df_head(self):
		print(self.student_df.head)

	def get_same_grade_students(self, grade):
		query = self.student_df.loc[self.student_df['Grade'] == grade]
		students_list = query['Student Number'].values.tolist()
		return students_list

	def get_infections_in_class(self, classname, period):
		# Shift col index based on period number

		period_col_name = 'Period ' + str(period) + ' Class'
		infection_col_name = 'Infection Rate P' + str(period)

		students_in_class = self.student_df.loc[self.student_df[period_col_name] == classname]
		student_list = students_in_class['Student Number'].values.tolist()

		# Get the infection values for a specific period for a specific class
		student_infection_list = []

		for i in student_list:
			rowindex = i - 1
			infection_value = self.student_df.at[rowindex, infection_col_name]
			student_infection_list.append((i, infection_value))

		# print(str(student_infection_list))
		return student_infection_list

	def get_student_activity(self, studentid):
		query = self.student_df.loc[self.student_df['Student Number'] == studentid]
		activity_name = query['Extracurricular Activities'].values.tolist()[0]
		# print(activity_name)
		return activity_name

	def get_activity_students(self, activity_name):
		query = self.student_df.loc[self.student_df['Extracurricular Activities'] == activity_name]
		students_list = query['Student Number'].values.tolist()
		# print(students_list)
		return students_list

	def print_student_head(self):
		print(self.student_df.head)


