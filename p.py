import os,pathlib
data = {
    'dataBase/income.csv' :'https://drive.google.com/uc?id=1-JD_AB53qvMBwMEGdc1e46DWRucGaJGj',
    'dataBase/balance.csv':'https://drive.google.com/uc?id=1-7fkmMoBiXQlEgJo0-59s0WGdcm0tzSt',
    'dataBase/cash.csv'   :'https://drive.google.com/uc?id=1-EntmCXZEluV4hpQ_hSOZCtr4GEot9o_',
    'dataBase/history.zip':'https://drive.google.com/uc?id=1hPKc_OP4VPMdiFX-Nql4l72Nq86wxmGb'
}
from gdown import download
# def download(i):
os.makedirs('dataBase',exist_ok=True)
    
def check(i):
    if not pathlib.Path(i).exists():
        print(i)
        download(url=data[i],output=i)

for i in data:
    check(i)

from tqdm.auto import tqdm
import zipfile
def unzip_history():
    path_to_zip_file = 'dataBase/history.zip'
    directory_to_extract_to = 'dataBase'
    
    if pathlib.Path(path_to_zip_file).exists():
        with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
            for member in tqdm(zip_ref.infolist(), desc='Extracting '):
                try:
                    zip_ref.extract(member,directory_to_extract_to)
                except zipfile.error as e:
                    pass

def count(path):
         
    data_path_count=0
    for root,dir,data_list in os.walk(path):
        if data_list:
            data_path_count+=len(data_list)
    return data_path_count

if count('dataBase/history')<29524:
    unzip_history()
        
from core.data import History
from core.data.data import read_csv
def cach(stocks,name):
    print(f'caching history - {name}')
    for i in tqdm(stocks):
        read_csv(f'dataBase/history/{name}/{i}.csv',index_col=0)

data = {
    
'1d' : History.one_d,
'1wk' : History.one_weak,
'1mo' : History.one_month
}
if count('CACHE_DIR')<59000:
    for k,v in data.items():
        stocks = v.stocks
        cach(stocks,k)
# print('cach length :',count('CACHE_DIR'))
    