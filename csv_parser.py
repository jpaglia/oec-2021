import sys
import csv
import json
import plotly
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import df_ops
from twilio.rest import Client
import twilio_client as sms
import probs
import matplotlib.pyplot as plt

SCHOOL_SIZE = 580	
	
def main():
	# PARSE THE STUDENT RECORDS
	#csv_to_json(student_csv)
	#print(result)
	student_df, teacher_df, ta_df, zby1_df = create_dataframes()

	dfwrapper = df_ops.DfWrapper(student_df, teacher_df, ta_df, zby1_df)
	
	dfwrapper.get_teachers_for_class("Physics A", 3, 4)
	# Insert initial infections
	# Holds the initial Data setup
	print('Processing Period 1')
	dfwrapper.update_infection_value(531, 1, 1.0)
	dfwrapper.update_infection_value(86, 1, 1.0)
	dfwrapper.update_infection_value(131, 1, 1.0)
	
	period_arr = [2, 2.5, 3, 4, 5]
	current_infections1 = [4]
	current_infections2 = [4]
	current_infections3 = [4]
	current_infections4 = [4]

	for i in range(len(period_arr)):
		period = period_arr[i]
		prev_period = period_arr[i] - 1
		all_students = [0] * SCHOOL_SIZE
		if period == 3:
			prev_period = 2.5
		if period == 2.5:
			print('Processing Lunch')
			# Special case for lunch logic
			all_grades = [9, 10, 11, 12]
			for grade in all_grades:
				grade_list = dfwrapper.get_infections_in_lunch(grade)
				student_ids = [i[0] for i in grade_list]
				infected_set = [i[1] for i in grade_list]
				unique_increase = dfwrapper.get_rate_increase(student_ids)
				new_probs = probs.get_new_class_infection_probs(infected_set, unique_increase, dfwrapper, '', 0, 0)
				for i in range(0, len(new_probs)):
					all_students[student_ids[i]-1] =  new_probs[i]
				
			dfwrapper.update_infection_column(period, all_students)
		elif period == 5:
			print('Processing After School')
			# Unique logic for after school activities
			all_activities = dfwrapper.get_extra_list()
			for after_school in all_activities:
				after_school_list = dfwrapper.get_infections_after_school(after_school)
				student_ids = [i[0] for i in after_school_list]
				infected_set = [i[1] for i in after_school_list]
				unique_increase = dfwrapper.get_rate_increase(student_ids)
				new_probs = probs.get_new_class_infection_probs(infected_set, unique_increase, dfwrapper, '', 0, 0)
				for i in range(0, len(new_probs)):
					all_students[student_ids[i]-1] =  new_probs[i]
			dfwrapper.update_infection_column(period, all_students)
		else:
			# Handles the  logic for each infectious Case per class
			print('Processing Period', period)
			all_classes = dfwrapper.get_class_list(period)
			for class_name in all_classes:
				class_list = dfwrapper.get_infections_in_class(class_name, prev_period, period)
				student_ids = [i[0] for i in class_list]
				infected_set = [i[1] for i in class_list]
				unique_increase = dfwrapper.get_rate_increase(student_ids)

				new_probs = probs.get_new_class_infection_probs(infected_set, unique_increase, dfwrapper, class_name, prev_period, period)
				for i in range(0, len(new_probs)):
					all_students[student_ids[i]-1] =  new_probs[i]
			dfwrapper.update_infection_column(period, all_students)
		
		# Get current Data
		threshold1 = 0.10
		threshold2 = 0.13
		threshold3 = 0.16
		threshold4 = 0.19

		infection_list = dfwrapper.get_infections_in_period(period)
		current_infections1.append(probs.get_thresh_hold_infected(threshold1, infection_list))
		current_infections2.append(probs.get_thresh_hold_infected(threshold2, infection_list))
		current_infections3.append(probs.get_thresh_hold_infected(threshold3, infection_list))
		current_infections4.append(probs.get_thresh_hold_infected(threshold4, infection_list))
	
	# print the plot using various thresholds
	plt.plot(['Period 1', 'Period 2', 'Lunch', 'Period 3', 'Period 4', 'After School'], current_infections1, color='red', label='Threshold 0.10')
	plt.plot(['Period 1', 'Period 2', 'Lunch', 'Period 3', 'Period 4', 'After School'], current_infections2, color='purple', label='Threshold 0.13')
	plt.plot(['Period 1', 'Period 2', 'Lunch', 'Period 3', 'Period 4', 'After School'], current_infections3, color='blue', label='Threshold 0.16')
	plt.plot(['Period 1', 'Period 2', 'Lunch', 'Period 3', 'Period 4', 'After School'], current_infections4, color='green', label='Threshold 0.19')
	plt.legend(loc='upper left')
	plt.xlabel('Period')
	plt.ylabel('Number of Exposures')
	plt.title('Period vs. Number of Exposures')
	plt.show()

	output_eod = dfwrapper.get_eod_infections()
	notify_sms(output_eod, threshold1)

def create_dataframes():
	# takes csv file name as arg[1]
	#student_csv = sys.argv[1]
	# FILL IN ARGS
	student_csv = 'Student_Records.csv'
	teacher_csv = 'Teacher_Records.csv'
	ta_csv = 'Teaching_Assistant_Records.csv'
	zby1_csv = 'ZBY1_Status.csv'

	#for csv_filename in sys.argv[1]:
	student_df = csv_to_dataframe(sys.argv[1])
	teacher_df = csv_to_dataframe(sys.argv[2])
	ta_df = csv_to_dataframe(sys.argv[3])
	zby1_df = csv_to_dataframe(sys.argv[4])
	
	return student_df, teacher_df, ta_df, zby1_df


def csv_to_dataframe(filename):
	dataframe = pd.read_csv(filename, error_bad_lines=False)
	return dataframe

	
def print_format():
	return False

# Notifies all people who may have been exposed with their current risk of infection via SMS message
def notify_sms(infected_set, threshold):
	for i in range(len(infected_set)):
		if (infected_set[i][1] > threshold):
			studentname = infected_set[i][3] + ' ' + infected_set[i][4]
			phone_num = infected_set[i][5]
			risk = str(round(infected_set[i][1],3) * 100) + '%'
			client = Client(sms.ACCOUNT_SID, sms.AUTH_TOKEN)
			msg = 'Hello ' + studentname + '. You may have been exposed to ZBY1. There is a ' + risk + ' chance that you have been infected.'
			# NOTE: Only the phone number for Sean Klocko (SN #1) will be notified, as it is the only registered number in the free trial
			try:
				# FOR THE PURPOSE OF THIS DEMO, WE CAN ONLY TEXT 1 PHONE NUMBER
				# THIS IS THE ONLY REASON WE HAVE THIS CONDITIONAL STATEMENT IN PLACE (SAME WITH THE BREAK)
				if (str(phone_num) == '6472341162'):
					client.messages.create(to='+1'+str(phone_num), from_=sms.TRIAL_NUMBER, body=msg)
					break
			except Exception as e:
				print('Student number is not included in the scope of the Twilio free trial') 

if __name__ == "__main__":
	# main()
	# app.run()
	# run command python csv_parser.py Student_Records.csv Teacher_Records.csv Teaching_Assistant_Records.csv ZBY1_Status.csv
	if (len(sys.argv) != 5):
		print('Please input data files in the following format:')
		print('<SCRIPT_NAME> <STUDENT_RECORDS.CSV> <TEACHER_RECORDS.CSV> <TA_RECORDS.CSV> <ZBY1_STATUS_RECORDS.CSV>')
	else:
		main()
		#app.run()
		





