import sys
import csv
import json
import plotly
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import df_ops
import twilio_client as sms
import probs

# def plot_from_csv(filename):
# 	csv_data = pd.read_csv(filename)
# 	data = [go.Scatter(
# 		x = csv_data[1],
# 		y = csv_data[2],
# 		mode = 'markers',
# 		#text = csv_data['word']
# 	)]
	
# 	fig = go.Figure(data)
	
# 	fig.update_layout(
# 		xaxis_title='Word from CSV',
# 		yaxis_title='Number from CSV',
# 		font=dict(
# 			family='Arial, monospace',
# 			size=16
# 			#color="#7f7f7f"
# 		),
# 		title = {
#         'text': 'A Plot for Sample Data from data.csv',
#         'y':0.9,
#         'x':0.5,
#         'xanchor': 'center',
#         'yanchor': 'top'}
# 	)

# 	graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
# 	return graphJSON

SCHOOL_SIZE = 580	
	
def main():
	# PARSE THE STUDENT RECORDS
	#csv_to_json(student_csv)
	#print(result)
	student_df, teacher_df, ta_df, zby1_df = create_dataframes()

	dfwrapper = df_ops.DfWrapper(student_df, teacher_df, ta_df, zby1_df)


	# Insert initial infections
	dfwrapper.update_infection_value(531, 1, 1.0)
	dfwrapper.update_infection_value(86, 1, 1.0)
	dfwrapper.update_infection_value(131, 1, 1.0)
	
	#dfwrapper.update_infection_value(1, 5, 0.6)
	period_arr = [2, 2.5, 3, 4]
	for i in range(len(period_arr)):
		period = period_arr[i]
		prev_period = period_arr[i] - 1
		all_students = [0] * SCHOOL_SIZE
		if period == 3:
			prev_period = 2.5
		if period == 2.5:
			# Special case for lunch logic
			all_grades = [9, 10, 11, 12]
			for grade in all_grades:
				grade_list = dfwrapper.get_infections_in_lunch(grade)
				student_ids = [i[0] for i in grade_list]
				infected_set = [i[1] for i in grade_list]
				unique_increase = dfwrapper.get_rate_increase(student_ids)
				new_probs = probs.get_new_class_infection_probs(infected_set, unique_increase)
				for i in range(0, len(new_probs)):
					all_students[student_ids[i]-1] =  new_probs[i]
			dfwrapper.update_infection_column(period, all_students)
		else:
			all_classes = dfwrapper.get_class_list(period)
			for class_name in all_classes:
				class_list = dfwrapper.get_infections_in_class(class_name, prev_period, period)
				student_ids = [i[0] for i in class_list]
				infected_set = [i[1] for i in class_list]
				unique_increase = dfwrapper.get_rate_increase(student_ids)
				new_probs = probs.get_new_class_infection_probs(infected_set, unique_increase)
				for i in range(0, len(new_probs)):
					all_students[student_ids[i]-1] =  new_probs[i]
			dfwrapper.update_infection_column(period, all_students)
		print(dfwrapper.student_df)
	# dfwrapper.get_class_list(1)
	# dfwrapper.get_student_activity(27)
	# dfwrapper.get_activity_students("Band")
	# dfwrapper.get_same_grade_students(11)

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
def notify_sms(infected_set):
	for i in range(len(infected_set)):
		studentname = ''
		phone_num = ''
		risk = '' + '%'
		client = Client(sms.ACCOUNT_SID, sms.AUTH_TOKEN)
		msg = 'Hello ' + patient.get('first_name') + '. You may have been exposed to ZBY1. There is a ' + str('') + ' chance that you have been infected.'
		# NOTE: Only the phone number for Sean Klocko (SN #1) will be notified, as it is the only registered number in the free trial
		try:
			client.messages.create(to='+1'+phone_num, from_=sms.TRIAL_NUMBER, body=msg)
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
		





