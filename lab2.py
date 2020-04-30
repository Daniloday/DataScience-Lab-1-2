from spyre import server
import pandas as pd
import urllib.request as urllib
import json
import os
import datetime
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
        df = self.getData(params)
        df = df[[params['ticker']]]
        plt_obj = df.plot()
        fig = plt_obj.get_figure()
        return fig

    def getData(self, params):
        df = self.filesClass.getDF()
        region = params["region"]
        typ = params["ticker"]
        first = params["from"] 
        last = params["to"] 
        df = df[df.Region == int(region)]
        df = df[df.Week >= float(first)]
        df = df[df.Week <= float(last)]
        return df[['Year','Week',typ,'Region']]
    

def main():
    filesClass = downloadFiles()
    app = StockExample(filesClass)
    app.launch(port=8081)

if __name__ == '__main__':
    main()
