from spyre import server
import pandas as pd
import urllib.request as urllib
import json
import os
import datetime


def clear():
    mydir = os.path.dirname(os.path.abspath(__file__))
    filelist = [ file for file in os.listdir(mydir) if file.endswith(".csv") ]
    for file in filelist:
        os.remove(os.path.join(mydir, file))

def createFile(newIndex, year1, year2):
    regions = {1:(24,'Vin'),2:(25,'Vol'),3:(5,'Dnipro'),4:(6,'Donetsk'),5:(27,'Vin'),6:(23,'Vin'),7:(26,'Vin'),8:(7,'Vin'),9:(11,'Vin'),10:(13,'Vin'),11:(14,'Vin'),12:(15,'Vin'),13:(16,'Vin'),14:(17,'Sum'),15:(18,'Vin'),16:(19,'Vin'),17:(21,'Hmel'),18:(22,'Vin'),19:(8,'Vin'),20:(9,'Vin'),21:(10,'Vin'),22:(1,'Vin'),23:(3,'Vin'),24:(2,'Vin'),
               25:(4,'Vin')}
    index = regions[newIndex][0]
    now = datetime.datetime.now()
    url = f'https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={index}&year1={year1}&year2={year2}&type=Mean'
    vhi_url = urllib.urlopen(url)
    out = open(f'vhi_id_{newIndex}_{now.day}_{now.month}_{now.year}_{regions[newIndex][1]}.csv','wb')
    out.write(vhi_url.read())
    out.close()
    print (f'Region {newIndex}({index}) is downloaded.')

def readFile(path):
    df = pd.read_csv(path, sep = ',', header=1)
    df.columns = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'Trash']
    index = path.split('_')[2]
    df['Region'] = int(index)
    del df['Trash']
    return df

def getDF():
	mydir = os.path.dirname(os.path.abspath(__file__))
	filelist = [ file for file in os.listdir(mydir) if file.endswith(".csv")]
	df = pd.concat([readFile(file) for file in filelist], ignore_index=True)
	df = df[(df.Year != '</pre></tt>') & (df.VHI != -1)]
	return df

class StockExample(server.App):
    title = "Historical Stock Prices"

    inputs = [{        "type":'dropdown',
                    "label": 'Parameter',
                    "options" : [ {"label": "VHI", "value":'VHI'},
                                  {"label": "TCI", "value":'TCI'},
                                  {"label": "VCI", "value":'VCI'}],
                    "key": 'ticker',
                    "action_id": "update_data"},

                {"type":'dropdown',
                    "label": 'Region',
                    "options" : [ {"label": region+1, "value": region+1 } for region in range(25)],
                    "key": 'region',
                    "action_id": "update_data"},
    
                {"type":'dropdown',
                    "label": 'From',
                    "options" : [ {"label": week+1, "value": week+1 } for week in range(52)],
                    "key": 'from',
                    "action_id": "update_data"},

                {"type":'dropdown',
                    "label": 'To',
                    "options" : [ {"label": week+1, "value": week+1 } for week in range(52)],
                    "key": 'to',
                    "action_id": "update_data"}
                    ]

    controls = [{    "type" : "hidden",
                    "id" : "update_data"}]

    tabs = ["Plot", "Table"]

    outputs = [
    			{ "type" : "plot",
                    "id" : "plot",
                    "control_id" : "update_data",
                    "tab" : "Plot"},
                { "type" : "table",
                    "id" : "table_id",
                    "control_id" : "update_data",
                    "tab" : "Table",
                    "on_page_load" : True }]
    def getPlot(self, params):
        df = getDF()
        plt_obj = df.plot()
        plt_obj.set_ylabel(params["ticker"])
        fig = plt_obj.get_figure()
        return fig

    def getData(self, params):
        df = getDF()
        region = params["region"]
        typ = params["ticker"]
        first = params["from"] 
        last = params["to"] 
        df = df[df.Region == int(region)]
        df = df[df.Week >= float(first)]
        df = df[df.Week <= float(last)]
        return df[['Year','Week',typ,'Region']]
    

def main():
	# clear()
	# for i in range(25):
	# 	createFile(i+1, 1982, 2020)
	app = StockExample()
	app.launch(port=8080)

if __name__ == '__main__':
    main()
