import pandas as pd
import plotly.express as px
import glob 
import mysql.connector as mysql
import os
import re
from datetime import datetime as d
from plotly.subplots import make_subplots
import plotly.graph_objects as go

path = os.path.dirname(os.path.abspath(__file__)) + '/data'

def all_file_read():
	col_lst=[]
	all_data = glob.glob(path + '/*.csv')
	for file in all_data:
		df = pd.read_csv(file, error_bad_lines=False, skiprows = 9, sep = ';', usecols=[0,1,2])
		for col in df.columns:
			colname = col.lower()
		col_lst.append(colname)

	return col_lst

def list_print(col_lst):
	atr_string = ''
	return atr_string.join(col_lst)

def find_file_path(atr_lst2, path):
	file_lst = []
	dir_lst = os.listdir(path)
	for atr in atr_lst2:
		file_lst.append(dir_lst[atr-1])
	return file_lst

def df_create(file_lst, path):
	tmp_df_dict = {}
	date_dict = {}
	df_dict = {}
	df_lst = []
	for file in file_lst:
		new_path = path + '/' + file
		df = pd.read_csv(new_path, error_bad_lines=False, skiprows = 9, sep = ';', usecols=[0,1,2])
		df['Datum'] = df['Datum'] + ' ' + df['Tid (UTC)']
		del df['Tid (UTC)']
		df_dict[file] = df
		date_dict['{}'.format(file)] = df.iloc[0, df.columns.get_loc('Datum')]
	for key, value in sorted(date_dict.items(), key=lambda item: item[1]):
		tmp_df_dict[key] = value
		df_lst.append(df_dict[key])
	dfs = [df.set_index('Datum') for df in df_lst]
	finished_df = pd.concat(dfs, axis = 1, sort = True)
	return finished_df

def validate_date(date1, date2):
    try:
        d.strptime(date1, '%Y-%m-%d')
        d.strptime(date2, '%Y-%m-%d')
        return True
    except ValueError:
        return False
def validate_year(year):
	try:
		d.strptime(year, '%Y')
		return True
	except ValueError:
		return False

def get_buttons(df, fig):
	col_lst = list(df.columns)
	updatemenus = list([
		dict(
			buttons=list([
				dict(
					args=[{'visible': [True if col2 == col else False for col2 in col_lst]}],
					label=col,
					method='update' 
					) 
				for col in col_lst ] + 
				[dict(
					args=[{'visible': [True  for col in col_lst]}],
					label='Alla',
					method='update' 
					)
				]),
			direction='down',
			active=0,
			x=0.57,
			y=1.2,
			)
		])
	xaxis=dict(
    rangeslider=dict(
        visible=True
    ),
    type="date"
)
	fig.update_layout(
		updatemenus=updatemenus,
		xaxis=xaxis
		)
	return fig
def year_graph(df, year, atr_lst):
	str_str = ''
	for atr in atr_lst:
		str_str += '-' + atr 
	file_name = year + '-' + str_str	
	count = 0
	slice_lst = []
	for index in df.index:
		if year in index:
			slice_lst.append(count)
			count += 1
		else:
			count += 1
	df = df.iloc[slice_lst[0]:slice_lst[-1]]
	fig = go.Figure()
	for col in df.columns:
		fig.add_trace(go.Scatter(x=df.index, y=df[col], mode='lines', name=col))
	fig = get_buttons(df, fig)
	fig.show()
	now = d.now()
	df.to_csv(os.path.dirname(os.path.abspath(__file__)) + '/generatedcsv' + '/{}.csv'.format(file_name))
	fig.write_html(os.path.dirname(os.path.abspath(__file__)) + '/generatedcsv' + '/{}.html'.format(file_name))

def graph(df, start_date, end_date, atr_lst):
		str_str = ''
		for atr in atr_lst:
			str_str += '-' + atr 
		file_name = start_date + '-' + end_date + str_str
		for index in df.index:
			if start_date in index:
				start_date = index
				break
		for index in df.index:
			if end_date in index:
				end_date = index
				break
		count = 0
		start_slice = 0
		end_slice = 0
		for index in df.index:
			if start_date == index:
				start_slice = count
				count += 1
			if end_date == index:
				end_slice = count
				count += 1
			else:
				count += 1
		df = df.iloc[start_slice:end_slice]
		fig = go.Figure()
		for col in df.columns:
			fig.add_trace(go.Scatter(x=df.index, y=df[col], mode='lines', name=col))
		fig = get_buttons(df, fig)
		fig.show()
		df.to_csv(os.path.dirname(os.path.abspath(__file__)) + '/generatedcsv' + '/{}.csv'.format(file_name))
		fig.write_html(os.path.dirname(os.path.abspath(__file__)) + '/generatedcsv' + '/{}.html'.format(file_name))

def get_year(df):
	start_year = df.index[0][:4]
	end_year = df.index[-1][:4]
	year = input('Vilket år vill du visa för (YYYY)?\n' +
					'\nTidigaste år är ' + start_year +
					' och äldsta år är ' + end_year + '\n')
	return year, start_year, end_year
def date(df):
	start_date = df.index[0][:10]
	end_date = df.index[-1][:10]
	date1 = input('\nMellan vilka datum vill du visa data (YYYY-MM-DD)?' +
					  '\nTidigaste datum är ' + start_date +
					  ' och sista datum är ' + end_date + '\n')
	date2 = input()
	return start_date, end_date, date1, date2

def atr_print(col_lst):
	count2 = 1
	print('\nVilka parametrar vill du visa?' + '\nDu kan välja mellan:\n')
	for attribut in col_lst:
		print('{}'.format(count2) + '. ' + attribut)
		count2 += 1

def menu(path):
	col_lst = all_file_read()
	count = False

	while  count == False:
		choice = input('\nVälkommen till Väder17(MVP)' +
					   '\nVänligen välj vad du vill göra' +
					   '\n1. Visa väderdata för Karlskrona' +
					   '\n2. Visa väderdata för ett specifikt år över Karlskorna' + 
					   '\n3. Avsluta' +
					   '\n')
		try:	
			if choice == '1':
				check = True
				check2 = True
				atr_lst = []
				atr_lst2 = []
				atr_print(col_lst)
				while check == True:
					try:
						atr = int(input('\nSkriv in nummret på de den parameter du vill välja\n(0 för färdigt val)\n'))
						if atr > 6:
							print('Vänligen välj från 1 till 6')
						if atr in atr_lst:
								print('Du kan inte välja parameter ' + atr + ' flera gånger')
						if atr == 0:						
							if len(atr_lst) == 0:
								print('Du har inte valt några parametrar')
							else:
								file_lst = find_file_path(atr_lst2, path)
								df = df_create(file_lst, path)
								while check2 == True:
									start_date, end_date, date1, date2 = date(df)
									if validate_date(date1,date2) == True:
										if date1 >= start_date and date1 <= end_date and date1 < date2:
											graph(df, date1, date2, atr_lst)
											check = False
											check2 = False
										else:
											print('Vänligen ange två datum i intervallet ' + start_date + ' till ' + end_date)
									else:
										print('Vänligen ange rätt form på datum, YYYY-MM-DD')
						if atr > 0 and atr < 7:
							if atr in atr_lst2:
								print('Du kan inte välja parameter ' + str(atr) + ' flera gånger')
							else:
								atr_lst.append(col_lst[(atr-1)])
								atr_lst2.append(atr)
					except ValueError:
						print('Valet måste vara ett nummer')
			if choice == '2':
				check = True
				check2 = True
				atr_lst = []
				atr_lst2 = []
				atr_print(col_lst)
				while check == True:
					try:
						atr = int(input('\nSkriv in nummret på de den parameter du vill välja\n(0 för färdigt val)\n'))
						if atr > 6:
							print('Vänligen välj från 1 till 6')
						if atr in atr_lst:
								print('Du kan inte välja parameter ' + atr + ' flera gånger')
						if atr == 0:						
							if len(atr_lst) == 0:
								print('Du har inte valt några parametrar')
							else:
								file_lst = find_file_path(atr_lst2, path)
								df = df_create(file_lst, path)
								while check2 == True:
									year, start_year, end_year = get_year(df)
									if validate_year(year) == True:
										if year >= start_year and year <= end_year:
											year_graph(df, year, atr_lst)
											check = False
											check2 = False
										else:
											print('Vänligen ange två datum i intervallet ' + start_date + ' till ' + end_date)
									else:
										print('Vänligen ange rätt form på datum, YYYY-MM-DD')
						if atr > 0 and atr < 7:
							if atr in atr_lst2:
								print('Du kan inte välja parameter ' + str(atr) + ' flera gånger')
							else:
								atr_lst.append(col_lst[(atr-1)])
								atr_lst2.append(atr)
					except ValueError:
						print('Valet måste vara ett nummer')
			if choice == '3':
				count = True
			if choice not in ['1','2','3']:
				print('Fel typ av input')
		except:
			print('Fel typ av input')
#def graph():

def main(path):
	menu(path)
	exit()
if __name__ == '__main__':
	main(path)
