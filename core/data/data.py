import os
import pathlib
import pandas as pd
from joblib import Memory

if True:
    _db_path = 'dataBase'
    _income_path  = f'{_db_path}/income.csv'
    _cash_path    = f'{_db_path}/cash.csv'
    _balance_path = f'{_db_path}/balance.csv'
    
    _profile_path = f'core/data/profile.csv'
    _dates_path   = f'core/data/dates.csv'
    _stocks_path  = f'core/data/stocks.csv'
    _1mo_path     = f'core/data/1mo.csv'
    _1wk_path     = f'core/data/1wk.csv'
    _1d_path      = f'core/data/1d.csv'
    CACHE_DIR     = 'CACHE_DIR'

    memory = Memory(CACHE_DIR,verbose=0)

@memory.cache
def read_csv(args, **kwargs):
    return pd.read_csv(args, **kwargs)

def put_space(i:str):
    i = str(i)
    if i.startswith('quarterly'):
        i = i[9:]
    i90 = ''
    for x, i9 in enumerate(str(i)):
        if x > 0:
            if i9.isupper():
                if x != len(i) - 1:
                    if not i[x + 1].isupper():
                        i90 += " "
                    elif i[x - 1].islower():
                        i90 += " "
        i90 += i9
    return i90

class Db:
    income_var    = read_csv(f'core/data/var/income_var.csv')
    cash_var      = read_csv(f'core/data/var/cash_var.csv')
    balance_var   = read_csv(f'core/data/var/balance_var.csv')
    # print('cachin income data')
    income        = read_csv(_income_path, index_col=['name', 'date'])
    # print('cachin cach data')
    cash          = read_csv(_cash_path, index_col=['name', 'date'])
    # print('cachin balance data')
    balance       = read_csv(_balance_path, index_col=['name', 'date'])
    dates         = read_csv(_dates_path, index_col=0)
    stocks        = read_csv(_stocks_path, index_col=0)
    profile       = read_csv(_profile_path, index_col=0)
    _1mo_dates    = read_csv(_1mo_path,index_col=0)
    _1wk_dates    = read_csv(_1wk_path,index_col=0)
    _1d_dates     = read_csv(_1d_path,index_col=0)
    # print(_1mo_dates)
    
    
    @classmethod
    def df(cls,name):
        match name:
            case 'income':
                df = cls.income
            case 'cash':
                df = cls.cash
            case 'balance':
                df = cls.balance
        return df

class Dates:
    def __init__(self, df: pd.DataFrame):
        self.dates = df.sort_index(ascending=False)
        self.index = self.dates.index
        self.df = pd.DataFrame(columns=self.dates.index)



    def last(self):
        # cls.dt:pd.DataFrame
        return self.dates.max().date().year

    def first(self):
        return self.dates.min().date().year

    def dates_after(self, date):
        d = str(date)
        return self.dates[self.dates > d]

class Var:
    def __init__(self, var, number) -> None:
        self._var = var
        self.number = number
        self.spaced = put_space(self._var)
        

    def __str__(self):
        _v = self._var
        if not _v.startswith("quarterly"):
            _v = f"quarterly{_v}"
        return _v

class Vars:

    def __init__(self, variables: list):
        self._variables = variables
        self.variables = [Var(var=i, number=_x)
                          for _x, i in enumerate(self._variables)]

    def __iter__(self):
        for i in self.variables:
            yield i

    def __len__(self):
        return len(self.variables)

    def __getitem__(self, item: int):
        item = int(item)
        _v = self.variables[item]
        if _v.number == item:
            return _v
        raise ValueError(f"item not found: {item}")

class Profile:
    db = Db.profile
    stocks = db.index.to_list()
    
    @classmethod
    def get_page_data(cls,stocks,headers):
        return cls.db.loc[stocks,headers]

class History:
    forbiden = [
        # '2023-03-27',
        # '2023-03-23',
        # '2023-03-22',
        # '2023-03-21',
        # '2023-03-16',
        # '2023-03-15',
        # '2023-03-14',
        # '2023-03-09',
        # '2023-03-08',
        # '2023-03-07',
        # '2023-03-02',
        # '2023-03-01',
        # '2023-02-28',
        # '2023-02-23',
        # '2023-02-22',
        # '2023-02-21',
        # '2023-02-16',
        # '2023-02-15',
        # '2023-02-14',
        # '2023-02-09',
        # '2023-02-08',
        # '2023-02-07',
        # '2023-02-02',
        # '2023-02-01',
        # '2023-01-31',
        # '2023-01-26',
        # '2023-01-25',
        # '2023-01-24',
        # '2023-01-19',
        # '2023-01-18',
        # '2023-01-17',
    ]
    All_stocks = Db.stocks
    variables = ['Open','High','Low','Close','Adj Close','Volume']
    
    
    DIR = pathlib.Path('dataBase/history')
    def __init__(self, name) -> None:
        self.name   = name   
        self.data = {}
        self.DIR = self.DIR/self.name
        self.dates  = getattr(Db,
                              f'_{self.name}_dates').sort_index(
                                  ascending=False)
        # print(0000000000000000000,self.dates)
        # self.dates = self.dates[~self.dates.index.isin(self.forbiden)]
        self.stocks = [i[:-4]
                       for i in  os.listdir(self.DIR)
                       if i.endswith('.csv')]
        # self.headers = self.dates.index.to_list()[300:]
        

    vars = [
            Var(i,x ) for x,i in enumerate(
                variables
            )
        ]
    # def vars(self):
        
        # return 

    def _get_stock_data(self, stock):
        if stock not in self.data.keys():
            try:
                df = read_csv(f'{self.DIR}/{stock}.csv',
                            index_col=0,parse_dates=['Date'])
                df = df.set_index(['Date'])
                df = df.sort_index(ascending=False)
                # df = df.dropna(how)
            except:
                df = self.data[0]
            self.data[stock]=df
                
        df = self.data[stock]
        return df
    
    def _page_data(self, stocks: list, var: str):
        data = {}
        for stock in stocks:
            try:
                df:pd.DataFrame= self._get_stock_data(stock)
            except:
                continue
            df =df.loc[:,var]
            df = df.dropna()
            
            df = df.reindex_like(self.dates)
            data[stock]= df

        data = pd.concat(data.values(),keys=data.keys(),axis=1)
        # data['dates'] = pd.DatetimeIndex(data.index).to_period(freq='m')
        # data = data.loc[~data.dates.duplicated('last')]   
        # data.drop(['dates'],axis=1,inplace=True)
        # print(data)
        return data
    
    def page_data(self, stocks, var,headers=False):
        assert var in self.variables
        data = self._page_data(stocks, var)
        # print(data)
        # data = data.transpose()
        # if var in self.vars:
        # else:
            # data = self.dates.transform()
        return data
            

 

class Finance:
    dates = Dates(Db.dates)
    variables = []
    stocks = Db.stocks

    def __init__(self, name):

        self.df = Db.df(name)
        self.Vars = Vars([ i for i in self.df.columns if i !='Unnamed: 0'])
        self.variables = self.Vars.variables
        self.vars = self.Vars.variables

    def get_var_data(self, var):
        _df = self.df[str(var)].unstack(level='date')
        try:
            d=_df.columns#pd.DataFrame(index=)
            if len(self.dates.index)!= len(d):

                _df = pd.concat([_df,self.dates.df])
            _df = _df[self.dates.index]

        except:
            print('empty 0000000000000')
            _df = pd.DataFrame(columns=self.dates.index)
        df = pd.concat([_df, self.stocks], axis=1)
        return df

    def page_data(self, stocks: list, var: str):
        return self.get_var_data(var).loc[stocks]



def get_stocks():
    return Db.stocks.index.to_list()