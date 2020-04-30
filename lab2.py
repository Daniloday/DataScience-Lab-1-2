from spyre import server
import pandas as pd
import json
import os
from downloadFiles import downloadFiles

class StockExample(server.App):
    def __init__(self,filesClass):
        self.filesClass = filesClass
        super(StockExample).__init__()
        
    title = "Data"

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
                    "action_id": "update_data"},
                    {"type":'dropdown',
                    "label": 'fromYear',
                    "options" : [ {"label": year+1, "value": year+1 } for year in range(1981,2020)],
                    "key": 'fromY',
                    "action_id": "update_data"},
                    {"type":'dropdown',
                    "label": 'toYear',
                    "options" : [ {"label": year+1, "value": year+1 } for year in range(1981,2020)],
                    "key": 'toY',
                    "action_id": "update_data"},
                    {"type":'dropdown',
                    "label": 'minWeek',
                    "options" : [ {"label": week+1, "value": week+1 } for week in range(52)],
                    "key": 'minWeek',
                    "action_id": "update_data"}
                    ]

    controls = [{    "type" : "hidden",
                    "id" : "update_data"}]

    tabs = ["Plot", "Table","Table2","Plot2"]

    outputs = [
    			{ "type" : "plot",
                    "id" : "plot",
                    "control_id" : "update_data",
                    "tab" : "Plot"},
                    { "type" : "plot",
                    "id" : "plot2",
                    "control_id" : "update_data",
                    "tab" : "Plot2"},
                { "type" : "table",
                    "id" : "table_id",
                    "control_id" : "update_data",
                    "tab" : "Table",
                    "on_page_load" : True },
                { "type" : "table",
                    "id" : "table_id2",
                    "control_id" : "update_data",
                    "tab" : "Table2",
                    "on_page_load" : True }]

    def plot(self, params):
        df = self.table_id(params)
        df.index = df.Year
        dfY = df[[params['ticker']]]
        plt_obj = dfY.plot()
        fig = plt_obj.get_figure()
        return fig

    def table_id(self, params):
        df = self.filesClass.getDF()
        region = params["region"]
        typ = params["ticker"]
        first = params["from"] 
        last = params["to"] 
        firstY = params["fromY"] 
        lastY = params["toY"]
        df = df[df.Region == int(region)]
        df = df[df.Week >= float(first)]
        df = df[df.Week <= float(last)]
        df = df[df.Year >= firstY]
        df = df[df.Year <= lastY]
        return df[['Year','Week',typ,'Region']]
    
    def table_id2(self, params):
        df = self.filesClass.getDF()
        region = params["region"]
        minWeek = params["minWeek"]
        df = df[df.Region == int(region)]
        nameDf = []
        for i in range(52):
        	df1 = df[df.Week == float(i+1)]
        	df2 = df1[df1.VHI == df1.VHI.min()]
        	# df2['VHIMin'] = df1.VHI.min()
        	df2['VHIMax'] = df1.VHI.max()
        	nameDf.append(df2)

        newDf = pd.concat(nameDf, ignore_index=True)
        newDf = newDf.rename(columns={'VHI': 'VHIMin'}) 
        first = params["from"] 
        last = params["to"]
        newDf = newDf[newDf.Week >= float(first)]
        newDf = newDf[newDf.Week <= float(last)]
        return newDf[['Week','VHIMin','VHIMax']]
    
    def plot2(self, params):
        df = self.table_id2(params)
        df.index = df.Week
        df = df[['VHIMin','VHIMax']]
        plt_obj = df.plot()
        fig = plt_obj.get_figure()
        return fig
        # esef

def main():
    filesClass = downloadFiles()
    app = StockExample(filesClass)
    app.launch(port=8081)

if __name__ == '__main__':
    main()
