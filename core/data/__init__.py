import os
import pathlib

from django.http import FileResponse
from .data import Finance, Var,Profile,get_stocks
from .data import History as _History
from .filter import Filters
# data = Filters.get_filter_and_sections()
# def stocks()
class Filter:
    def __init__(self,sec_name, filter_list) -> None:
        
        self.sec_name = sec_name
        self.filter_list = filter_list
        self.length  = len(self.filter_list)
        
        
def download_file(file0):

    # if c==1:
    
    file_server = pathlib.Path(f"{file0}")
    file_to_download = open(str(file_server), 'rb')
    response = FileResponse(file_to_download, content_type='application/force-download')
    response['Content-Disposition'] = f'inline; filename={os.path.basename(file0)}'
    return response

class History:
    
    one_d  = _History('1d')
    one_d.page_count2 = 500
    one_month = _History('1mo')
    one_month.page_count2 = 900
    one_weak = _History('1wk')
    one_weak.page_count2 = 700
    


            