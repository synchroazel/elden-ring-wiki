import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs


class EldenRingDb():

    def __init__(self):
        self.sets = self.__get_dbs__("https://eldenring.wiki.fextralife.com/Armor+Sets+Comparison+Table", type='set')
        self.helms = self.__get_dbs__("https://eldenring.wiki.fextralife.com/Helms", type='armor')
        self.chest = self.__get_dbs__("https://eldenring.wiki.fextralife.com/Chest+Armor", type='armor')
        self.gaunt = self.__get_dbs__("https://eldenring.wiki.fextralife.com/Gauntlets", type='armor')
        self.legs = self.__get_dbs__("https://eldenring.wiki.fextralife.com/Leg+Armor", type='armor')
        self.weapons = self.__get_dbs__("https://eldenring.wiki.fextralife.com/Weapons+Comparison+Tables",
                                        type='weapons')

    def __get_dbs__(self, url, type):

        payload = ""
        headers = {"Content-Type": "text/plain"}

        response = requests.request("GET", url, data=payload, headers=headers)

        soup = bs(response.text)

        table = list()

        for line in soup.find_all("th"):
            table.append(line.getText().strip())

        for line in soup.find_all("td"):
            table.append(line.getText().strip())

        features = {'set': 15,
                    'armor': 17,
                    'weapons': 24}

        n_feats = features[type]

        mat = np.array(table).reshape(len(table) // n_feats, n_feats)

        df = pd.DataFrame(mat)

        if type == 'set':
            df = pd.DataFrame(mat)
            df.iloc[0, :] = df.iloc[0, :].str.replace(' ', '_', regex=True).str.replace('.', '', regex=True)
            df.columns = df.iloc[0].str.replace('  ', '')
            df = df[1:]
            df = df.replace('--', 0)
            df.iloc[:, 1:] = df.iloc[:, 1:].astype(float)
            df["Pieces"] = df['Set_Name'].str.split('Pieces').str.get(0).str.slice(-2, -1).astype(int)
            df["Set_Name"] = df['Set_Name'].str.split('Pieces').str.get(0).str.slice(0, -3)

        if type == 'armor':
            df.columns = df.iloc[0]
            df = df[1:]
            df.iloc[:, :-2] = df.iloc[:, :-2].replace('--', 0).replace('-', 0).replace('', 0)
            df.iloc[:, 1:-2] = df.iloc[:, 1:-2].astype(float)

        if type == 'weapons':
            df.columns = df.iloc[0]
            df = df[1:]
            df.iloc[:, 2:-1] = df.iloc[:, 2:-1].replace('-', 0)
            df.iloc[:, 2:9] = df.iloc[:, 2:9].astype(float)

        return df
