import pandas as pd
import numpy as np
class Filters:
    filter_data_path = 'core/data/filter_data.csv' 
    df = pd.read_csv(filter_data_path, index_col=0)
    stocks = list(df.columns)
    stocks.remove('filter_sec')

    @classmethod
    def get_sections(self):
        return self.df['filter_sec'].unique()

    @classmethod
    def _get_filters(self):
        for i in self.get_filter_and_sections().values():
            for fltr in i:
                yield  fltr
                
    @classmethod
    def get_filters(self):
        list(self._get_filters())
        
    @classmethod
    def get_sec_filters(self, sec):
        fltrs = self.df[
            self.df['filter_sec'] == sec
            ]
        return fltrs.index.to_list()

    
    @classmethod
    def get_filter_and_sections(self):
        data = dict()
        sections = self.get_sections()
        for sec in sections:
            data[sec] = self.get_sec_filters(sec)
        return data

    @classmethod
    def get_stocks_by_filter(self, fltr):
        stocks = self.stocks
        msk = self.df.loc[fltr, stocks]
        return self.df[stocks].columns[msk]

    @classmethod
    def mask(self, lst):
        msk = self.df.columns.isin(lst)
        return msk

    @classmethod
    def save(self, df):
        df.to_csv(self.filter_data_path)
        self.df = df

    @classmethod
    def create(self, lst, name):
        df = self.df.copy()
        msk = df.columns.isin(lst)
        df.loc[name] = msk
        df.loc[name, 'filter_sec'] = 'User'
        self.save(df)

    # def create(self, lst, name):
        # fltrs = list(self.get_filters())
        # if name not in fltrs:
            # return self._create(lst, name)
        # raise ValueError(f'filter name {name} already in use')
    @classmethod
    def remove(self, name):
        df = self.df[self.df.index != name]
        self.save(df)

    @classmethod
    def inner(self, d1, d2):
        return np.intersect1d(d1, d2)

    @classmethod
    def union(self, d1, d2):
        return d1.append(d2).drop_duplicates()

    @classmethod
    def outter(self, d1, d2):
        u = self.union(d1, d2)
        return u[~u.isin(self.inner(d1, d2))]
    
    @classmethod
    def join_all(self, filter_list, func=False):
            if not callable(func):
                func = self.union
            d = self.get_stocks_by_filter(filter_list[0])
            if len(filter_list)>1:
                for x,i in enumerate(filter_list[1:]):            
                    d2 = self.get_stocks_by_filter(i)
                    d = func(d,d2)
            return d
    


