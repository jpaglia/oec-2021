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

		# Add infection rate columns to teacher df
		self.teacher_df['Infection Rate P1'] = 0.0
		self.teacher_df['Infection Rate P2'] = 0.0
		self.teacher_df['Infection Rate P3'] = 0.0
		self.teacher_df['Infection Rate P4'] = 0.0

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

	def get_extra_list(self):
		activities = self.student_df['Extracurricular Activities'].tolist()
		activities = list(set(activities))
		return activities

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

	# Updates infection % value for an entire column for a specific period
	def update_infection_column(self, period, column):
		infection_col_name = 'Infection Rate P' + str(period)
		self.student_df[infection_col_name] = column

	def print_df_head(self):
		print(self.student_df.head)

	def get_same_grade_students(self, grade):
		query = self.student_df.loc[self.student_df['Grade'] == grade]
		students_list = query['Student Number'].values.tolist()
		return students_list

	# Get all infections in period 2
	def get_infections_in_lunch(self, grade):
		# Get infection rates from the column for period 2
		infection_col_name = 'Infection Rate P2'

		students_in_class = self.student_df.loc[self.student_df['Grade'] == str(grade)]
		student_list = students_in_class['Student Number'].values.tolist()

		# Get the infection values for a specific period for a specific class
		student_infection_list = []

		for i in student_list:
			rowindex = i - 1
			infection_value = self.student_df.at[rowindex, infection_col_name]
			student_infection_list.append((i, infection_value))

		return student_infection_list

	def get_infections_after_school(self, extracurricular):
		# Get infection rates from the column for period 2
		infection_col_name = 'Infection Rate P4'

		students_after_school = self.student_df.loc[self.student_df['Extracurricular Activities'] == str(extracurricular)]
		student_list = students_after_school['Student Number'].values.tolist()

		# Get the infection values for a specific period for a specific class
		student_infection_list = []

		for i in student_list:
			rowindex = i - 1
			infection_value = self.student_df.at[rowindex, infection_col_name]
			student_infection_list.append((i, infection_value))

		return student_infection_list

	def get_infections_in_class(self, classname, prev_period, curr_period):
		# Shift col index based on period number

		period_col_name = 'Period ' + str(curr_period) + ' Class'
		infection_col_name = 'Infection Rate P' + str(prev_period)

		students_in_class = self.student_df.loc[self.student_df[period_col_name] == classname]
		student_list = students_in_class['Student Number'].values.tolist()

		# Get the infection values for a specific period for a specific class
		student_infection_list = []

		for i in student_list:
			rowindex = i - 1
			infection_value = self.student_df.at[rowindex, infection_col_name]
			student_infection_list.append((i, infection_value))

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

	def get_rate_increase(self, student_list):
		rate_increase_list = []
		# Iterate through student list
		for i in student_list:
			rowindex = i - 1
			increase_value = 1.0

			grade_level = self.student_df.at[rowindex, "Grade"]
			health_conditions = self.student_df.at[rowindex, "Health Conditions"]
			
			increase_value = increase_value + (0.25 * (grade_level - 9))
			
			if str(health_conditions) != "nan":
				increase_value = increase_value + 0.7

			rate_increase_list.append(increase_value)

		# print(str(rate_increase_list))
		return rate_increase_list
