import pandas as pd
import os
from tqdm.auto import tqdm
# from joblib import Memory
# class Filter:
#     def __init__(self) -> None:
#         pass
# cachedir = 'data/cash_dir'
# os.makedirs(cachedir,exist_ok=True)
# memory = Memory(cachedir, verbose=0)
_db_path = 'core/data'


class Var:
    def __init__(self,var, number) -> None:
        # pass
        self._var = var
        self.spaced = self.putSpace(var)
        # self.non_spaced = non_spaced
        self.number = number
    
    @property
    def var(self):
        return self.putSpace(self._var)
    
    @property
    def var_(self):
        _v=self._var
        if not _v.startswith( "quarterly"):
            _v = f"quarterly{_v}"
        return _v
    
    @classmethod
    def putSpace(i):
        i90=''
        for x,i9 in enumerate(str(i)) :
            if x>0 :
                if i9.isupper()  :
                    if  x!=len(i)-1:
                        
                        if not i[x+1].isupper():
                            i90+=" "
                        elif i[x-1].islower():
                            i90+=" "
            i90+=i9
        return i90


class Db:
    income_var   =f'{_db_path}/var/income_var.csv'
    cash_var     =f'{_db_path}/var/cash_var.csv'
    balance_var  =f'{_db_path}/var/balance_var.csv'
    
    
    def __init__(self, path, name) -> None:
        self.path = path
        self.name = name
        self.vars = self.get_var(self.name)
        self.data = self.get_data(self.path)
    
    # @memory.cache
    def get_data(self, path):
        return self.get_df(path)


    @staticmethod
    def get_df(path):
        df = pd.read_csv(path)
        return df
    
    
    def get_var(self, name):
        var = ''
        match name:
            case 'balance':
                var = self.balance_var
            case 'cash':
                var = self.cash_var
            case 'income':
                var = self.income_var
            # finally:
        return self.get_df(var)
    

class Data:
    
    def __init__(self,df:pd.DataFrame) -> None:
        self.df = df
        self.html = self.df.set_index(['name','date']).unstack(level=0).to_html()
        print(self.html)
     
# @memory.cache
class Main:
    _income_path = 'core/data/income.csv'
    _dates_path = f'{_db_path}/dates.csv'
    dates = pd.read_csv(_dates_path,index_col=0)
    dates.set_index(pd.DatetimeIndex(dates.index).date,inplace=True)
    # dates = dates.sort_index(ascending=False)
    # print(dates)
    
    income = Db(_income_path, 'income')
    data = income.data
    
    @classmethod
    def get_data_var(cls, var:str):
        if not var.startswith("quarterly"):
            var = f"quarterly{var}"
        data = cls.data[['name','date',var]]
        # stocks = data['name'].unique()
        # print(stocks)
        # headers = data['name'].unique()
        return data
        
    
    @staticmethod
    def putSpace(i):
        i90=''
        for x,i9 in enumerate(str(i)) :
            if x>0 :
                if i9.isupper()  :
                    if  x!=len(i)-1:
                        
                        if not i[x+1].isupper():
                            i90+=" "
                        elif i[x-1].islower():
                            i90+=" "
            i90+=i9
        return i90
    
    @classmethod
    def response(cls, request):
        vars = cls.income.vars['vars'].to_list()
        statments = [tws(spaced= cls.putSpace(p),non_spaced=p,number=vars.index(p)) for p in vars]
        # var1,
        var = statments[0]
        # , statments[0].number
        data=''
        # data = cls.get_data_var(var.non_spaced)
        # data =     cls.get_data_var(var.non_spaced).set_index(['name','date']).unstack(level=0).to_html()
        # Data(
        #             ) 
        # for i in data.groups:
        #     print(i)
        # print(data)
        
        c = {
            'vars':statments,
            'var1':var.spaced,
            'var0':var.number,
            # 'companies':data.companies,
            'data':data,
            # "dates":cls.dates.index
        }
        
        return c
    # def __init__(self) -> None:
    #     pass

    
# class ResponseMain:
    # pass
    # def __init__(self) -> None:
    #     pass
