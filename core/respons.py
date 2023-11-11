# import abs
import json
import os
import pathlib
from django.http import FileResponse
from django.shortcuts import render
import pandas as pd
from django.core.paginator import Paginator
from core.data import *
import shutil

def human_format(num):
    try:
        num = int(num)
    except:
        return num
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])


def reformat(ser: pd.Series):
    return ser.apply(human_format)


class Context:
    def __init__(self,variable=0,filter=False,page=1,
                 pagination_count=20,pages=[],pagination_count2=300,
                 page2=1,pages2=[]) -> None:
        
        self.variable         =variable
        self._filter           =filter
        self.page             =page
        self.page2             =page2
        self.pagination_count =pagination_count
        self.pagination_count2 =pagination_count2
        self.pages            =pages
        self.pages2            =pages2
    
    @property
    def filter(self):
        return self._filter
    
    @filter.setter
    def filter(self,fltr):
        if fltr in ['false',0,'0'] :
            self._filter = False
        else:
            self._filter = fltr

class Downloads:
    tmp_dir = 'tmp'
    name =''
    @classmethod
    def check(cls, request) -> None:
        download_list = request.GET.getlist('download_list',False)
        if download_list:
            return download_list    
        download = request.GET.get('download',False)
        if download:
            return [download]
        return False
        
    @classmethod
    def _download(cls,var_list, context):
        _filter = ''
        name    = context['name']
        page    = context['page']
        cls.clean_tmp_dir()
        if len(var_list)>1:
            name = name+'_data'
        name = f"{cls.tmp_dir}/{name}_p{page}{_filter}.xlsx"
        writer = pd.ExcelWriter(name, engine = 'xlsxwriter')
        for var in var_list:
            if not var:
                continue
            var = int(var)
            data:pd.DataFrame = cls.get_data(var=var)
            if isinstance(int(var),int):
                sheet_name = cls.get_sheet_name(var)
            else:
                sheet_name = var
            
            data.to_excel(writer, sheet_name=sheet_name)
        writer.close()
        return download_file(name)
    
    @classmethod
    def clean_tmp_dir(cls):
        os.makedirs(cls.tmp_dir, exist_ok=True)
        for i in pathlib.Path(cls.tmp_dir).glob("*.xlsx"):
            os.remove(i)
            
class BaseRespons(Downloads, Filters):
    name = ''
    c = Context(pagination_count=50)
    stocks = get_stocks()
    request_items= {
        'filter':   c.filter,
        'page':     c.page,
        'pagination_count': c.pagination_count,
        'variable'        :c.variable,
        
        
    }
    paginator = Paginator(stocks, per_page=int(c.pagination_count))   
    
    # @classmethod
    def download(cls, download_list):
        context=cls.context()
        return cls._download(download_list, context) 
    
    @classmethod
    def get_sheet_name(cls, i:int):
        v = cls.db.vars[i].spaced
        v = f'{i}_{v[:10]}'
        return v
    
    @classmethod
    def data_delivery(cls)->pd.DataFrame: 
        return cls._data
    
    @property
    def headers(self):
        return self._headers
    
    @classmethod
    def get_or_set_request_item(cls, item, request):
        req_item = request.GET.get(item)
        if req_item:
            setattr(cls.c,item,req_item)
    
    @classmethod
    def update_state(cls, request):
        for i in cls.request_items:
            cls.get_or_set_request_item(i, request)

    @classmethod
    def filters(cls):
        return [Filter(k,v) 
                        for k,v in  Filters.get_filter_and_sections().items()
                        if k != 'currency'
                        ]
    
    @classmethod
    def ajax_respons(cls):
        stocks = cls.paginator.page(int(cls.c.page)).object_list
        data = cls.db.page_data(
            stocks,
            var = cls.c.variable
        )
        data = data.to_json(orient='records')
        data = json.loads(data)
        js = {
            'data': [
                list(i.values()) for i in data
            ]
        }
        return js
        

class HistoryRespons(BaseRespons):
    variables = ['Open','High','Low','Close','Adj Close','Volume']
    variables = [Var(i,x)for x,i in enumerate(variables)]
    
    c = Context(pagination_count=20,variable=0)
    # @classmethod
    
    request_items= {
        'filter':   c.filter,
        'page':     c.page,
        'page2':     c.page2,
        'variable':c.variable,
        'pagination_count': c.pagination_count,
        'pagination_count2': c.pagination_count2,
    }
    @classmethod
    def set_data(cls,name):
        # match name:
            if name == '1d':
                db= History.one_d
            elif name == '1wk':
                db= History.one_weak
            elif name =='1mo':
                db= History.one_month
            # print(db.dates.index)
            cls.db = db
            return db
    
    def __init__(self,name,request=False) -> None:
        self.name = name
        self.db=self.set_data(name)
        print(name)
        print(self.db.dates.index)
        self.stocks = self.db.stocks
        if request:
            self.update_state(request)
        self.paginator = Paginator(
            self.stocks, per_page=int(self.c.pagination_count))
        self.paginator2 = Paginator(
            self.db.dates.index.to_list(),per_page=int(self.c.pagination_count2))
        self._headers:list = self.paginator2.page(int(self.c.page2)).object_list
        self._headers.insert(0,'Company')
        
    
    @classmethod
    def get_data(self,var=False,name=False,page=False):
        stock_list = self.paginator.page(int(self.c.page)).object_list
        stock_list = list(stock_list)
        if not var:
            var = self.c.variable
        var = self.variables[int(var)]._var
        print('var              ',var)
        data = self.db.page_data(stocks=list(stock_list), var = var)
        data = data.transpose()
        return data
    
    def context(cls):
        return {
            'history':True,
            'name': cls.name,
            'headers': cls._headers,
            'vars': cls.db.vars,
            'variable': cls.c.variable,
            'page': cls.c.page,
            'page2': cls.c.page2,
            'pagination_count': cls.c.pagination_count,
            'paginator':cls.paginator,
            'paginator2':cls.paginator2,
            'filter':cls.c.filter,
            'stock_count':len(cls.paginator.object_list),
            'filters' : cls.filters
            
        }
    
    def ajax_respons(cls):
        stocks = cls.paginator.page(int(cls.c.page)).object_list
        right =  cls._headers[1]
        left =  cls._headers[-1]
        var = cls.db.variables[cls.c.variable]
        data = cls.db.page_data(
            stocks,
            var = var
        )
        dd = data[
            data.index <= right
        ]
        data=dd[dd.index >=left]
        data = data.transpose()
        data = data.apply(reformat)
        data = data.to_json(orient='table')
        data = json.loads(data)['data']
        js = {
            'data': [
                list(i.values()) for i in data
            ]
        }
        return js  

class HomeRespons(BaseRespons):
    db = Profile
    _headers = ['symbol','exchange','nasdac','longName','currency','industry','sector']    

    @classmethod
    def update_state(cls,request=False):
        stocks_data = cls.db.stocks
        if cls.c.filter:
            stocks_data = Filters.get_stocks_by_filter(cls.c.filter)
        cls.paginator = Paginator(stocks_data, per_page=int(cls.c.pagination_count))
        if request:
            super().update_state(request)
        
    def __init__(cls):
        cls.update_state()

    def download(cls,*args):
        name = f'tmp/profile_{cls.c.page}.xlsx'
        stocks = cls.paginator.page(int(cls.c.page)).object_list
        os.makedirs('tmp',exist_ok=True)
        cls.db.get_page_data(stocks=stocks,headers=cls.headers).to_excel(name)
        return download_file(name)
    def context(cls):
        # cls.set_data(request)
        return {
                'name'            :'profile',
                'headers'         : cls.headers,
                'filter'          : cls.c.filter,
                'page'            : int(cls.c.page),
                'pagination_count': cls.c.pagination_count,
                'paginator'       :cls.paginator,
                'stock_count'     :len(cls.paginator.object_list),
                'filters'         :cls.filters,
                'variable'        :1
        }
    
    @classmethod
    def ajax_respons(cls, name=False, var=False, page=None, request=None):
        stocks = cls.paginator.page(int(cls.c.page)).object_list
        headers = cls._headers
        assert isinstance(headers,list)
        data:pd.DataFrame = cls.db.get_page_data(stocks=stocks,headers=headers)
        
        data = data.to_json(orient='records')
        data = json.loads(data)
        js = {
            'data': [
                list(i.values()) for i in data
            ]
        }
        return js
        

class FinanceRespons(BaseRespons):
    
    
    @classmethod
    def get_data(cls,var=False,name=False,page=False):
        stock_list = cls.paginator.page(int(cls.c.page)).object_list
        stock_list = list(stock_list)
        if not var:
            var = cls.c.variable
        var = cls.variables[int(var)]
        data = cls.db.page_data(stocks=list(stock_list), var = var)
        return data
    
    @classmethod
    def set_data(cls, name):
        db                  = Finance(name)
        
        cls.name            = name
        cls.db              = db
        cls.headers         = list(
            cls.db.dates.index)
        cls.db.variables    = db.Vars.variables
        cls.variables       = db.Vars.variables
        stocks_data         = db.stocks.index
        if cls.c.filter :
            stocks_data     = Filters.get_stocks_by_filter(cls.c.filter)
        cls.paginator       = Paginator(stocks_data, per_page=int(cls.c.pagination_count))
    
    def __init__(self,name,request=False) -> None:
        if request:
            self.update_state(request)
        self.set_data(name)
        self.headers.insert(0,'Company')
        
    @classmethod
    def ajax(cls, *args, **kwargs):
        data = {}
        return data


    @classmethod
    def update_request(cls, request):
        cls.update_state(request)
        
    @classmethod
    def get_finance_context(cls):
        return {
            'name': cls.name,
            'headers': cls.headers,
            'vars': cls.db.variables,
            'variable': int(cls.c.variable),
            'page': cls.c.page,
            'pagination_count': cls.c.pagination_count,
            'paginator':cls.paginator,
            'filter':cls.c.filter,
            'stock_count':len(cls.paginator.object_list),
            'filters' : cls.filters
            }

    @classmethod
    def context(cls):
        c = cls.get_finance_context()
        return c

    @classmethod
    def ajax_respons(cls, name=False, var=False, page=None, request=None):

        data= cls.get_data(var,name,page)
        
        data = data.apply(reformat)
        data = data.to_json(orient='table')
        data = json.loads(data)['data']
        js = {
            'data': [
                list(i.values()) for i in data
            ]
        }
        return js