import pandas as pd
import plotly.express as px
import glob 
import mysql.connector as mysql
import os
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots

db = mysql.connect(
	user='pa1450',  
    password='pa1450',    
    host='192.168.56.1',
    database='weatherdata'
    )

mycursor = mysql.connect()

path = os.path.dirname(os.path.abspath(__file__)) + '/data'
testpath1 = 'C:\\Users\\jdahl\\Desktop\\WeatherApp/data/smhi-karlskrona-nederbördsmängd.csv'
testpath2 = 'C:\\Users\\jdahl\\Desktop\\WeatherApp/data/smhi-karlskrona-lufttemperatur.csv'
all_data = glob.glob(path + '/*.csv')
print(all_data)
col_lst = []
for file in all_data:
	df = pd.read_csv(file, error_bad_lines=False, skiprows = 9, sep = ';', usecols=[0,1,2])
	for col in df.columns:
		colname = col
	#print('df_{}'.format(colname))
	col_lst.append(colname)
df1 = pd.read_csv(testpath1, error_bad_lines=False, skiprows = 9, sep = ';', usecols=[0,1,2])
df2 = pd.read_csv(testpath2, error_bad_lines=False, skiprows = 9, sep = ';', usecols=[0,1,2])

date1 = '2020-01-02'
date2 = '2020-02-02'
date3 = '2019-05-02'
date4 = '2020-01-02'
if date1 >= date4 and date2 < date1:
	print('det funkar')
else:
	print('fel')
df_lst = []
#df3 = pd.concat([df1, df2], axis=1)
df1['Datum'] = df1['Datum'] + ' ' + df1['Tid (UTC)']
del df1['Tid (UTC)']
df_lst.append(df1)
df2['Datum'] = df2['Datum'] + ' ' + df2['Tid (UTC)']
del df2['Tid (UTC)']
print(len(df1))
#df_lst.append(df2)
#df3 = pd.concat([df2, df1], axis=1)
#df3 = df2.join(df1, how='inner')
'''
df3 = df2.merge(df1, on='Datum', how='left')
dat_lst =  df3['Datum'].tolist()
ned_lst = df3['Nederbördsmängd'].tolist()
luft_lst = df3['Lufttemperatur'].tolist()
fig = px.line()
fig.add_scatter(x=df3['Datum'], y = df3['Lufttemperatur'], mode='lines', name='luft')
fig.add_scatter(x=df3['Datum'], y = df3['Nederbördsmängd'], mode='lines', name='ned')
x = df1.iloc[0, df1.columns.get_loc('Datum')]
y = df2.iloc[0, df2.columns.get_loc('Datum')]
print(x, y)

if x < y:
	print(x)
else:
	print(y)
''
#fig.add_trace(go.Scatter(x=dat_lst, y=luft_lst,
#                    mode='markers',
#                   name='luft'))
'''
'''
fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            #dict(count=1, label="1m", step="month", stepmode="backward"),
            #dict(count=6, label="6m", step="month", stepmode="backward"),
            #dict(count=1, label="YTD", step="year", stepmode="todate"),
            #dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
        ])
    )
)

'''
#fig.show()
'''
#fig = px.line(df3, x='Datum', y='Nederbördsmängd')
'''
'''
fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(
    px.line(df3, x='Datum', y='Nederbördsmängd'),
    secondary_y=False,
)
fig.add_trace(
    px.line(df3, x='Datum', y='Lufttemperatur'),
    secondary_y=True,
)
fig.update_layout(
    title_text="Double Y Axis Example"
)
'''


'''
print(df3)
#df3.to_csv(path + '/test.csv') 
#for atr in col_lst:
#	'df_{}'.dormate(colname) = pd.read_csv
	#mycursor.execute('CREATE TABLE (%s) (Datum DATETIME, Tid TIME, (%s))', (colname, colname))
	
	#df.to_csv(path + '/{}.csv'.format(colname))
	#print(df.to_string(index=False))
#result = []
'''
'''
'''
'''
testlist = ['hej','jim','vad','händer']

button_lst = []
for str in testlist:
	con_lst = []
	for x in testlist:
		con_lst.append(False)
	con_lst[testlist.index(str)] = True
	button_lst.append(dict(label=str,
         method="update",
         args=[{"visible": con_lst},
               {"title": str + 'över Karlskrona från ' + start_date + ' till ' + end_date,
                "annotations": []}]))
con_lst = []
buttons = []
for str in testlist:
	con_lst.append(True)
buttons.append(dict(label="Alla",
                     method="update",
                     args=[{"visible": con_lst},
                           {"title": 'Väderdata över Karlskrona från ' + start_date + ' till ' + end_date,
                            "annotations": []}]))
updatemenus=[
        dict(
            type="buttons",
            direction="right",
            active=0,
            x=0.57,
            y=1.2)]

buttons = list(button_lst)
updatemenus.append(buttons)
print(updatemenus)
'''
'''        
            buttons=list([
                dict(label="None",
                     method="update",
                     args=[{"visible": [True, False, True, False]},
                           {"title": "Yahoo",
                            "annotations": []}]),
                dict(label="High",
                     method="update",
                     args=[{"visible": [True, True, False, False]},
                           {"title": "Yahoo High",
                            "annotations": high_annotations}]),
                dict(label="Low",
                     method="update",
                     args=[{"visible": [False, False, True, True]},
                           {"title": "Yahoo Low",
                            "annotations": low_annotations}]),
                dict(label="Both",
                     method="update",
                     args=[{"visible": [True, True, True, True]},
                           {"title": "Yahoo",
                            "annotations": high_annotations + low_annotations}]),
            ])
'''
'''   
fig.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            direction="right",
            active=0,
            x=0.57,
            y=1.2,
            buttons=list([
                dict(label="None",
                     method="update",
                     args=[{"visible": [True, False, True, False]},
                           {"title": "Yahoo",
                            "annotations": []}]),
                dict(label="High",
                     method="update",
                     args=[{"visible": [True, True, False, False]},
                           {"title": "Yahoo High",
                            "annotations": high_annotations}]),
                dict(label="Low",
                     method="update",
                     args=[{"visible": [False, False, True, True]},
                           {"title": "Yahoo Low",
                            "annotations": low_annotations}]),
                dict(label="Both",
                     method="update",
                     args=[{"visible": [True, True, True, True]},
                           {"title": "Yahoo",
                            "annotations": high_annotations + low_annotations}]),
            ]),
        )
    ])

col_lst = list(df.columns)	
		vis_lst = []
		buttons = []
		for col in df.columns:
			vis_lst.append(True)
		buttons.append(dict(label="Alla",
		                    method="update",
		                    args=[{"visible": vis_lst},
		                           {"title": 'Väderdata över Karlskrona från ' + start_date + ' till ' + end_date,
		                            "annotations": []}]))	
		for col in df.columns:
			vis_lst = []
			for x in df.columns:
				vis_lst.append(False)
			vis_lst[col_lst.index(col)] = True
			buttons.append(dict(label=col,
		         				method="update",
		         				args=[{"visible": vis_lst},
		               				{"title": col + ' över Karlskrona från ' + start_date + ' till ' + end_date,
		                			"annotations": []}]))
		buttons = list(buttons)
		updatemenus=[dict(
            type="buttons",
            direction="right",
            active=0,
            x=0.57,
            y=1.2,
            buttons=list(buttons))]
'''
d = {'hej': 'hej'+'rip'}
print(d)