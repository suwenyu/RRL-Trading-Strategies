import json
import datetime, time
import os


from utils import tools
from config import project_config

import pandas as pd

class Crawler:
    def __init__(self):
        self.url = """https://api.gdax.com/products/BTC-EUR/candles?start={}&end={}&granularity={}"""
        self.days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        self.months = [i for i in range(1, 13)]
        self.years = [2015, 2016, 2017, 2018]

        self.df = None
        self.data_dir = os.path.dirname(os.path.realpath(__file__)) + "/data/"
        self.data_name = 'data.csv'


    def retrieve_daily_data(self, timepoint, duration):
        start_time = timepoint - duration * 96
        end_time = timepoint + duration * 192

        requests = tools.Request(project_config.CONFIG)
        res = requests.get(self.url.format(start_time.isoformat(), end_time.isoformat(), str(duration.seconds) ))
        # print(self.url.format(start_time.isoformat(), end_time.isoformat(), str(duration.seconds) ))
        if res['status'] == 200:
            data = json.loads(res['text'])

            data.reverse()

            for row in data:
                yield row

        time.sleep(1)

    def store_data(self, data):
        self.df = pd.DataFrame(data, columns=['timestamp', 'low', 'high', 'open', 'close', 'vol'])
        self.df['time'] = self.df['timestamp'].apply(lambda x : datetime.datetime.fromtimestamp(x).isoformat())
        
        self.df.to_csv(self.data_dir + self.data_name, mode='a', header=None, index=0)


    def run(self):

        if os.path.exists(self.data_dir + self.data_name):
            os.remove(self.data_dir + self.data_name)

        duration = datetime.timedelta(minutes = 5)
        timepoint = datetime.datetime(2020, 7, 10)

        data = self.retrieve_daily_data(timepoint, duration)
        self.store_data(data)


if __name__ == '__main__':

    crawler = Crawler()
    crawler.run()






