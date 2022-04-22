import webbrowser
import pandas as pd 
import csv
import requests
import glob, os
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (20,7)
import numpy as np
import time
import urllib.request, json 
import seaborn as sns
sns.set()


api_key_1 = '' 
# can get API key from https://financialmodelingprep.com/



input_string_2 = input('What do you want to analyze? BalanceSheets = Press 1, IncomeStatements = Press 2, CashFlowStatments = Press 3(notready yet), FinancialRatios = Press 4, KeyMetrics = Press 5, Exit = 6   ')
option = input_string_2
# all data to be analyzed will be based on quarterly statements


input_string_1 = input('What tickers do you want to analyze? (Max 3 companies at a time.) ') # AMD, INTC, NVDA
tickers = input_string_1.upper().split(", ")


# print(len(tickers))


def download_files():
	if option == str(1):
		for tick in tickers:
			with urllib.request.urlopen('https://financialmodelingprep.com/api/v3/balance-sheet-statement/'+tick+'?period=quarter&limit=400&apikey='+api_key_1) as url:
				data = json.loads(url.read().decode())
				with open(tick+'.json', 'w') as outfile:
					json.dump(data, outfile)

	elif option == str(2):
		for tick in tickers:
			with urllib.request.urlopen('https://financialmodelingprep.com/api/v3/income-statement/'+tick+'?period=quarter&limit=400&apikey='+api_key_1) as url:
				data = json.loads(url.read().decode())
				with open(tick+'.json', 'w') as outfile:
					json.dump(data, outfile)

	elif option == str(3):
		for tick in tickers:
			with urllib.request.urlopen('https://financialmodelingprep.com/api/v3/cash-flow-statement/'+tick+'?period=quarter&limit=400&apikey='+api_key_1) as url:
				data = json.loads(url.read().decode())
				with open(tick+'.json', 'w') as outfile:
					json.dump(data, outfile)

	elif option == str(4):
		for tick in tickers:
			with urllib.request.urlopen('https://financialmodelingprep.com/api/v3/ratios/'+tick+'?period=quarter&limit=140&apikey='+api_key_1) as url:
				data = json.loads(url.read().decode())
				with open(tick+'.json', 'w') as outfile:
					json.dump(data, outfile)

	elif option == str(5):
		for tick in tickers:
			with urllib.request.urlopen('https://financialmodelingprep.com/api/v3/key-metrics/'+tick+'?period=quarter&limit=130&apikey='+api_key_1) as url:
				data = json.loads(url.read().decode())
				with open(tick+'.json', 'w') as outfile:
					json.dump(data, outfile)
	

	elif option == str(6):
		print('Thank you.')


download_files()


path = r'/Users/Cashmanzero/Downloads/*.json'
list_of_files = glob.glob(path) # * means all if need specific format then *.csv
sorted_files = sorted(list_of_files, key=os.path.getmtime)


def label_files():
	global newest_file
	global second_newest_file
	global third_newest_file
	if len(tickers) == 1:
		newest_file = sorted_files[-1]
		# print(newest_file) # AMD test
		return newest_file

	elif len(tickers) == 2:
		newest_file = sorted_files[-1]
		second_newest_file = sorted_files[-2]
		# print(newest_file) # INTC test
		# print(second_newest_file) # AMD
		return newest_file, second_newest_file

	elif len(tickers) == 3:
		newest_file = sorted_files[-1]
		second_newest_file = sorted_files[-2]
		third_newest_file = sorted_files[-3]
		# print(newest_file) # NVDA
		# print(second_newest_file) # INTC
		# print(third_newest_file) # AMD
		return newest_file, second_newest_file, third_newest_file


label_files()


def read_json_files():
	global df1
	global df2
	global df3
	if len(tickers) == 1:
		df1 = pd.read_json(newest_file)
		print(df1) # AMD
		return df1
	
	elif len(tickers) == 2:
		df1 = pd.read_json(newest_file)
		df2 = pd.read_json(second_newest_file)
		print(df1) # INTC
		print(df2) # AMD
		return df1, df2
		
	elif len(tickers) == 3:
		df1 = pd.read_json(newest_file)
		df2 = pd.read_json(second_newest_file)
		df3 = pd.read_json(third_newest_file)
		print(df1) # NVDA
		print(df2) # INTC
		print(df3) # AMD
		return df1, df2, df3


read_json_files()


def drop_columns(dataframe):
	if option == str(1) or option == str(2) or option == str(3): # balance sheet columns	
		dataframe = dataframe.drop([dataframe.columns[1], dataframe.columns[2], dataframe.columns[3], dataframe.columns[4], dataframe.columns[-1], dataframe.columns[-2]], axis='columns')
		return dataframe
		print(dataframe)

	elif option == str(4): # Financial ratio columns
		dataframe = dataframe.drop([dataframe.columns[0]], axis='columns')
		return dataframe
		print(dataframe)

	elif option == str(5): # Key metric columns
		dataframe = dataframe.drop([dataframe.columns[0]], axis='columns')
		return dataframe
		print(dataframe)

	elif option == str(6):
		print('Thanks')
	


def drop_for_existing_dataframes():
	global df1_sorted
	global df2_sorted
	global df3_sorted
	if len(tickers) == 1:
		df1_sorted = drop_columns(df1).sort_values(by=['date'], ascending=1) # AMD
		print(df1_sorted)
		return df1_sorted
	
	elif len(tickers) == 2:
		df1_sorted = drop_columns(df1).sort_values(by=['date'], ascending=1) # INTC
		df2_sorted = drop_columns(df2).sort_values(by=['date'], ascending=1) # AMD
		print(df1_sorted)
		print(df2_sorted)
		return df1_sorted, df2_sorted
	
	elif len(tickers) == 3:
		df1_sorted = drop_columns(df1).sort_values(by=['date'], ascending=1) # NVDA
		df2_sorted = drop_columns(df2).sort_values(by=['date'], ascending=1) # INTC
		df3_sorted = drop_columns(df3).sort_values(by=['date'], ascending=1) # AMD
		print(df1_sorted)
		print(df2_sorted)
		print(df3_sorted)
		return df1_sorted, df2_sorted, df3_sorted


drop_for_existing_dataframes()


def create_new_df():
	global list_iterator
	global df4
	global columns
	df4 = pd.DataFrame()
	columns = df1_sorted.columns
	list_iterator = iter(columns)
	next(list_iterator)
	df4['DATE'] = df1_sorted['date']
	print(df4)
	return list_iterator
	return df4


create_new_df()


def combine_stocks_dfs():
	if len(tickers) == 1:
		for metric in list_iterator:
			df4[tickers[0]+' '+metric] = df1_sorted[metric] # AMD ROW
		print(df4)
		return df4
			
	elif len(tickers) == 2:
		for metric in list_iterator:
			df4[tickers[1]+' '+metric] = df1_sorted[metric] # AMD ROW
			df4[tickers[0]+' '+metric] = df2_sorted[metric] # INTC ROW
		print(df4)
		return df4

	elif len(tickers) == 3:
		for metric in list_iterator:
			df4[tickers[2]+' '+metric] = df1_sorted[metric] # AMD ROW
			df4[tickers[1]+' '+metric] = df2_sorted[metric] # INTC ROW
			df4[tickers[0]+' '+metric] = df3_sorted[metric] # NVDA ROW
		print(df4)
		return df4


combine_stocks_dfs()


def export_one_csv():
	if option == str(1):
		export_csv = df4.to_csv (r"/Users/Cashmanzero/Desktop/StockComparisons/"+tickers[0]+" BalanceSheets.csv", index = None, header=True)
		print('Done Cloning The Data Frame!')
		os.mkdir("/Users/Cashmanzero/Desktop/StockComparisons/"+tickers[0]+" BalanceSheet Plots/")

	elif option == str(2):
		export_csv = df4.to_csv (r"/Users/Cashmanzero/Desktop/StockComparisons/"+tickers[0]+" IncomeStmt.csv", index = None, header=True)
		print('Done Cloning The Data Frame!')
		os.mkdir("/Users/Cashmanzero/Desktop/StockComparisons/"+tickers[0]+" IncomeStmt Plots/")

	elif option == str(3):
		export_csv = df4.to_csv (r"/Users/Cashmanzero/Desktop/StockComparisons/"+tickers[0]+" vs. "+tickers[1]+" CFStmt.csv", index = None, header=True)
		print('Done Cloning The Data Frame!')
		os.mkdir("/Users/Cashmanzero/Desktop/StockComparisons/"+tickers[0]+" CFStmt Plots/")

	elif option == str(4):
		export_csv = df4.to_csv (r"/Users/Cashmanzero/Desktop/StockComparisons/"+tickers[0]+" FinancialRatios.csv", index = None, header=True)
		print('Done Cloning The Data Frame!')
		os.mkdir("/Users/Cashmanzero/Desktop/StockComparisons/"+tickers[0]+" FinancialRatios Plots/")

	elif option == str(5):
		export_csv = df4.to_csv (r"/Users/Cashmanzero/Desktop/StockComparisons/"+tickers[0]+" KeyMetrics.csv", index = None, header=True)
		print('Done Cloning The Data Frame!')
		os.mkdir("/Users/Cashmanzero/Desktop/StockComparisons/"+tickers[0]+" KeyMetrics Plots/")


def export_two_csv():
	if option == str(1):
		export_csv = df4.to_csv (r"/Users/Cashmanzero/Desktop/StockComparisons/"+tickers[0]+" vs. "+tickers[1]+" BalanceSheets.csv", index = None, header=True)
		print('Done Cloning The Data Frame!')
		os.mkdir("/Users/Cashmanzero/Desktop/StockComparisons/"+tickers[0]+" vs. "+tickers[1]+" BalanceSheet Plots/")

	elif option == str(2):
		export_csv = df4.to_csv (r"/Users/Cashmanzero/Desktop/StockComparisons/"+tickers[0]+" vs. "+tickers[1]+" vs. "+tickers[2]+" IncomeStmt.csv", index = None, header=True)
		print('Done Cloning The Data Frame!')
		os.mkdir("/Users/Cashmanzero/Desktop/StockComparisons/"+tickers[0]+" vs. "+tickers[1]+" IncomeStmt Plots/")

	elif option == str(3):
		export_csv = df4.to_csv (r"/Users/Cashmanzero/Desktop/StockComparisons/"+tickers[0]+" vs. "+tickers[1]+" CFStmt.csv", index = None, header=True)
		print('Done Cloning The Data Frame!')
		os.mkdir("/Users/Cashmanzero/Desktop/StockComparisons/"+tickers[0]+" vs. "+tickers[1]+" CFStmt Plots/")

	elif option == str(4):
		export_csv = df4.to_csv (r"/Users/Cashmanzero/Desktop/StockComparisons/"+tickers[0]+" vs. "+tickers[1]+" FinancialRatios.csv", index = None, header=True)
		print('Done Cloning The Data Frame!')
		os.mkdir("/Users/Cashmanzero/Desktop/StockComparisons/"+tickers[0]+" vs. "+tickers[1]+" FinancialRatios Plots/")

	elif option == str(5):
		export_csv = df4.to_csv (r"/Users/Cashmanzero/Desktop/StockComparisons/"+tickers[0]+" vs. "+tickers[1]+" KeyMetrics.csv", index = None, header=True)
		print('Done Cloning The Data Frame!')
		os.mkdir("/Users/Cashmanzero/Desktop/StockComparisons/"+tickers[0]+" vs. "+tickers[1]+" KeyMetrics Plots/")


def export_three_csv():
	if option == str(1):
		export_csv = df4.to_csv (r"/Users/Cashmanzero/Desktop/StockComparisons/"+tickers[0]+" vs. "+tickers[1]+" vs. "+tickers[2]+" BalanceSheets.csv", index = None, header=True)
		print('Done Cloning The Data Frame!')
		os.mkdir("/Users/Cashmanzero/Desktop/StockComparisons/"+tickers[0]+" vs. "+tickers[1]+" vs. "+tickers[2]+" BalanceSheet Plots/")

	elif option == str(2):
		export_csv = df4.to_csv (r"/Users/Cashmanzero/Desktop/StockComparisons/"+tickers[0]+" vs. "+tickers[1]+" vs. "+tickers[2]+" IncomeStmt.csv", index = None, header=True)
		print('Done Cloning The Data Frame!')
		os.mkdir("/Users/Cashmanzero/Desktop/StockComparisons/"+tickers[0]+" vs. "+tickers[1]+" vs. "+tickers[2]+" IncomeStmt Plots/")

	elif option == str(3):
		export_csv = df4.to_csv (r"/Users/Cashmanzero/Desktop/StockComparisons/"+tickers[0]+" vs. "+tickers[1]+" vs. "+tickers[2]+" CFStmt.csv", index = None, header=True)
		print('Done Cloning The Data Frame!')
		os.mkdir("/Users/Cashmanzero/Desktop/StockComparisons/"+tickers[0]+" vs. "+tickers[1]+" vs. "+tickers[2]+" CFStmt Plots/")

	elif option == str(4):
		export_csv = df4.to_csv (r"/Users/Cashmanzero/Desktop/StockComparisons/"+tickers[0]+" vs. "+tickers[1]+" vs. "+tickers[2]+" FinancialRatios.csv", index = None, header=True)
		print('Done Cloning The Data Frame!')
		os.mkdir("/Users/Cashmanzero/Desktop/StockComparisons/"+tickers[0]+" vs. "+tickers[1]+" vs. "+tickers[2]+" FinancialRatios Plots/")

	elif option == str(5):
		export_csv = df4.to_csv (r"/Users/Cashmanzero/Desktop/StockComparisons/"+tickers[0]+" vs. "+tickers[1]+" vs. "+tickers[2]+" KeyMetrics.csv", index = None, header=True)
		print('Done Cloning The Data Frame!')
		os.mkdir("/Users/Cashmanzero/Desktop/StockComparisons/"+tickers[0]+" vs. "+tickers[1]+" vs. "+tickers[2]+" KeyMetrics Plots/")


def export_based_number_of_stocks():
	if len(tickers) == 1:
		export_one_csv()

	elif len(tickers) == 2:
		export_two_csv()

	elif len(tickers) == 3:
		export_three_csv()


export_based_number_of_stocks()


def plot_one_graph():
	if option == str(1):
		for metric in columns[1:]:
			df4.plot(kind='line', x='DATE', y=[tickers[0]+' '+metric])
			plt.title(metric)
			plt.grid()
			plt.savefig("/Users/Cashmanzero/Desktop/StockComparisons/"+tickers[0]+" BalanceSheet Plots/"+tickers[0]+metric+".png") 
			# plt.show(block=False)
			# plt.pause(1)
			# plt.close()
	
	elif option == str(2):
		for metric in columns[1:]:
			df4.plot(kind='line', x='DATE', y=[tickers[0]+' '+metric])
			plt.title(metric)
			plt.grid()
			plt.savefig("/Users/Cashmanzero/Desktop/StockComparisons/"+tickers[0]+" IncomeStmt Plots/"+tickers[0]+metric+".png") 
			# plt.show(block=False)
			# plt.pause(1)
			# plt.close()
	
	elif option == str(3):
		for metric in columns[1:]:
			df4.plot(kind='line', x='DATE', y=[tickers[0]+' '+metric])
			plt.title(metric)
			plt.grid()
			plt.savefig("/Users/Cashmanzero/Desktop/StockComparisons/"+tickers[0]+" CFStmt Plots/"+tickers[0]+metric+".png") 
			# plt.show(block=False)
			# plt.pause(1)
			# plt.close()
	
	elif option == str(4):
		for metric in columns[1:]:
			df4.plot(kind='line', x='DATE', y=[tickers[0]+' '+metric])
			plt.title(metric)
			plt.grid()
			plt.savefig("/Users/Cashmanzero/Desktop/StockComparisons/"+tickers[0]+" FinancialRatios Plots/"+tickers[0]+metric+".png") 
			# plt.show(block=False)
			# plt.pause(1)
			# plt.close()
	
	elif option == str(5):
		for metric in columns[1:]:
			df4.plot(kind='line', x='DATE', y=[tickers[0]+' '+metric])
			plt.title(metric)
			plt.grid()
			plt.savefig("/Users/Cashmanzero/Desktop/StockComparisons/"+tickers[0]+" KeyMetrics Plots/"+tickers[0]+metric+".png") 
			# plt.show(block=False)
			# plt.pause(1)
			# plt.close()


def plot_two_graphs():
	if option == str(1):
		for metric in columns[1:]:
			df4.plot(kind='line', x='DATE', y=[tickers[0]+' '+metric , tickers[1]+' '+metric])
			plt.title(metric)
			plt.grid()
			plt.savefig("/Users/Cashmanzero/Desktop/StockComparisons/"+tickers[0]+" vs. "+tickers[1]+" BalanceSheet Plots/"+tickers[0]+" vs. "+tickers[1]+metric+".png") 
			# plt.show(block=False)
			# plt.pause(1)
			# plt.close()
	
	elif option == str(2):
		for metric in columns[1:]:
			df4.plot(kind='line', x='DATE', y=[tickers[0]+' '+metric , tickers[1]+' '+metric])
			plt.title(metric)
			plt.grid()
			plt.savefig("/Users/Cashmanzero/Desktop/StockComparisons/"+tickers[0]+" vs. "+tickers[1]+" IncomeStmt Plots/"+tickers[0]+" vs. "+tickers[1]+metric+".png") 
			# plt.show(block=False)
			# plt.pause(1)
			# plt.close()
	
	elif option == str(3):
		for metric in columns[1:]:
			df4.plot(kind='line', x='DATE', y=[tickers[0]+' '+metric , tickers[1]+' '+metric])
			plt.title(metric)
			plt.grid()
			plt.savefig("/Users/Cashmanzero/Desktop/StockComparisons/"+tickers[0]+" vs. "+tickers[1]+" CFStmt Plots/"+tickers[0]+" vs. "+tickers[1]+metric+".png") 
			# plt.show(block=False)
			# plt.pause(1)
			# plt.close()
	
	elif option == str(4):
		for metric in columns[1:]:
			df4.plot(kind='line', x='DATE', y=[tickers[0]+' '+metric , tickers[1]+' '+metric])
			plt.title(metric)
			plt.grid()
			plt.savefig("/Users/Cashmanzero/Desktop/StockComparisons/"+tickers[0]+" vs. "+tickers[1]+" FinancialRatios Plots/"+tickers[0]+" vs. "+tickers[1]+metric+".png") 
			# plt.show(block=False)
			# plt.pause(1)
			# plt.close()
	
	elif option == str(5):
		for metric in columns[1:]:
			df4.plot(kind='line', x='DATE', y=[tickers[0]+' '+metric , tickers[1]+' '+metric])
			plt.title(metric)
			plt.grid()
			plt.savefig("/Users/Cashmanzero/Desktop/StockComparisons/"+tickers[0]+" vs. "+tickers[1]+" KeyMetrics Plots/"+tickers[0]+" vs. "+tickers[1]+metric+".png") 
			# plt.show(block=False)
			# plt.pause(1)
			# plt.close()


def plot_three_graphs():
	if option == str(1):
		for metric in columns[1:]:
			df4.plot(kind='line', x='DATE', y=[tickers[0]+' '+metric , tickers[1]+' '+metric, tickers[2]+' '+metric])
			plt.title(metric)
			plt.grid()
			plt.savefig("/Users/Cashmanzero/Desktop/StockComparisons/"+tickers[0]+" vs. "+tickers[1]+" vs. "+tickers[2]+" BalanceSheet Plots/"+tickers[0]+" vs. "+tickers[1]+" vs. "+tickers[2]+metric+".png") 
			# plt.show(block=False)
			# plt.pause(1)
			# plt.close()
	
	elif option == str(2):
		for metric in columns[1:]:
			df4.plot(kind='line', x='DATE', y=[tickers[0]+' '+metric , tickers[1]+' '+metric, tickers[2]+' '+metric])
			plt.title(metric)
			plt.grid()
			plt.savefig("/Users/Cashmanzero/Desktop/StockComparisons/"+tickers[0]+" vs. "+tickers[1]+" vs. "+tickers[2]+" IncomeStmt Plots/"+tickers[0]+" vs. "+tickers[1]+" vs. "+tickers[2]+metric+".png") 
			# plt.show(block=False)
			# plt.pause(1)
			# plt.close()
	
	elif option == str(3):
		for metric in columns[1:]:
			df4.plot(kind='line', x='DATE', y=[tickers[0]+' '+metric , tickers[1]+' '+metric, tickers[2]+' '+metric])
			plt.title(metric)
			plt.grid()
			plt.savefig("/Users/Cashmanzero/Desktop/StockComparisons/"+tickers[0]+" vs. "+tickers[1]+" vs. "+tickers[2]+" CFStmt Plots/"+tickers[0]+" vs. "+tickers[1]+" vs. "+tickers[2]+metric+".png") 
			# plt.show(block=False)
			# plt.pause(1)
			# plt.close()
	
	elif option == str(4):
		for metric in columns[1:]:
			df4.plot(kind='line', x='DATE', y=[tickers[0]+' '+metric , tickers[1]+' '+metric, tickers[2]+' '+metric])
			plt.title(metric)
			plt.grid()
			plt.savefig("/Users/Cashmanzero/Desktop/StockComparisons/"+tickers[0]+" vs. "+tickers[1]+" vs. "+tickers[2]+" FinancialRatios Plots/"+tickers[0]+" vs. "+tickers[1]+" vs. "+tickers[2]+metric+".png") 
			# plt.show(block=False)
			# plt.pause(1)
			# plt.close()
	
	elif option == str(5):
		for metric in columns[1:]:
			df4.plot(kind='line', x='DATE', y=[tickers[0]+' '+metric , tickers[1]+' '+metric, tickers[2]+' '+metric])
			plt.title(metric)
			plt.grid()
			plt.savefig("/Users/Cashmanzero/Desktop/StockComparisons/"+tickers[0]+" vs. "+tickers[1]+" vs. "+tickers[2]+" KeyMetrics Plots/"+tickers[0]+" vs. "+tickers[1]+" vs. "+tickers[2]+metric+".png") 
			# plt.show(block=False)
			# plt.pause(1)
			# plt.close()


def plot_based_number_of_stocks():
	if len(tickers) == 1:
		plot_one_graph()

	elif len(tickers) == 2:
		plot_two_graphs()

	elif len(tickers) == 3:
		plot_three_graphs()

	print('Plots Have Been Saved!')


plot_based_number_of_stocks()


def remove_downloaded_jsons():
	if len(tickers) == 1:
		os.remove(newest_file)

	elif len(tickers) == 2:
		os.remove(newest_file)
		os.remove(second_newest_file)

	elif len(tickers) == 3:
		os.remove(newest_file)
		os.remove(second_newest_file)
		os.remove(third_newest_file)

remove_downloaded_jsons()
