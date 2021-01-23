import sys
import csv
import json
import plotly
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import df_ops

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
	
	
def main():

	# PARSE THE STUDENT RECORDS
	#csv_to_json(student_csv)
	#print(result)
	student_df, teacher_df, ta_df, zby1_df = create_dataframes()

	dfwrapper = df_ops.DfWrapper(student_df, teacher_df, ta_df, zby1_df)

	# dfwrapper.print_student_head()
	# result = dfwrapper.get_people_in_class('Functions A', 1)
	# print(result)

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

# OLD TEMPLATE CONTENT - TO BE REMOVED/MODIFIED
def csv_parser(filename, record_type):
	with open(filename) as csvfile:
	#with open(filename, newline='') as csvfile:
		reader = csv.DictReader(csvfile)
		for line in reader:
			# TO-DO: stuff for each type of dataset

			print(line['word'] + ' is ' + line['num'])
			#print(str(line))

# OLD TEMPLATE CONTENT - TO BE REMOVED/MODIFIED		
def csv_to_json(filename):
	#with open(filename) as csvfile:
	#	reader = csv.DictReader(csvfile)
		#Stores all contents of csv as json
	reader = reader(filename)
	result = json.dumps([row for row in reader])		
		#Stores array of all elements 'word'
		#result = json.dumps([row['word'] for row in reader])
	print(result)
		

def reader(filename):
	with open(filename) as csvfile:
		reader = csv.DictReader(csvfile)
		return reader
	
def write_to_file(filename):
	file = open(filename,'w+')
	for i in range(10): #CHANGE THIS BASED ON PROBLEM
		file.write('Writing this line...')
	file.close()
	
def append_to_file(filename):
	file = open(filename,'a+')
	for i in range(10): #CHANGE THIS BASED ON PROBLEM
		file.write('Appending this line...')
	file.close()
	
def print_format():
	return False
	
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
		





