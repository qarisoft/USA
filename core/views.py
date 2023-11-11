from django.http import JsonResponse
from django.shortcuts import redirect, render
from .data import Filter, Filters
from .respons import HomeRespons, FinanceRespons, HistoryRespons, BaseRespons

def download_req(request):
    download = request.GET.get('download',False)
    if download:
        return download

    



# def _respons(request,name):
class Respons(BaseRespons):
    _home = HomeRespons()
    @classmethod
    def router(cls,name,request=None):
        if name =='profile':
            return cls._home
            
        elif name in ['income','balance','cash']:
            return FinanceRespons(name,request)
        
        elif name in ['1d','1wk','1mo']:
            return HistoryRespons(name,request)
    
    @classmethod
    def download(cls,download_target):
        return cls.respons_cls.download(download_target)
    
    @classmethod
    def _render(cls,request,template):
        context = cls.respons_cls.context()
        return render(
            request,
            template,
            context
        )
    
    @classmethod
    def manager(cls,request,name,template):
        cls.respons_cls = cls.router(name,request)
        if not isinstance(cls.respons_cls,BaseRespons):
            raise ValueError("class not base respons")
        
        cls.respons_cls.update_state(request)
        target = cls.check(request)
        if target:
            return cls.download(target)
        else:
            return cls._render(
                request,
                template              
            )
    
    @classmethod
    def ajax_respons(cls):
        assert isinstance(cls.respons_cls,BaseRespons)
        try:
            data = cls.respons_cls.ajax_respons() 
        except Exception as e:
            print(e)
            data= {"data":f"{e}"}
        return data 
        # if data:
        
# data = HomeRespons().ajax_respons()
def ajax_respons(request):
        return JsonResponse (Respons.ajax_respons())

def finance(request, department):  
    return  Respons.manager(request=request,
                        name=department,
                        template='finance.html'
                        )  
    
def history(request,department):
    # return finance(request,department)
    return  Respons.manager(request=request,
                    name=department,
                    template='history.html'
                    )  
    
def index(request):
    name = 'profile'
    return  Respons.manager(request=request,
                            name=name,
                            template='index.html'
                            )



def filter_respons(filter_list,cs):
    assert len(filter_list)>0
    assert cs
    match cs:
        case 'inner':
            respons = Filters.join_all(filter_list,Filters.inner)
        case 'outer':
            respons = Filters.join_all(filter_list,Filters.outter)
        case 'all':
            respons = Filters.join_all(filter_list,Filters.union)
    return list(respons)

def filter_ajax(request):
    cs = request.GET.get('crostype',False)
    if cs:
        filter_list = request.GET.getlist('filtr_with_sec[]',[])
        respons = ''
        if len(filter_list)>0: 
            respons=filter_respons(filter_list, cs)
        # respons = list(respons) 
        return JsonResponse({'data':respons})

def delet_filter(request,filter):
    if request.method=='POST':
        filter_to_del = request.POST.get('delet_filter_sure_yes',False)
        if filter_to_del:
            Filters.remove(filter_to_del)
            return redirect(to='filter')
    return render(request,'delet_filter.html',{'filter':filter})
    
def filter(request):
    if request.method=='POST':
        filter_list = request.POST.getlist('filtr_list',[])
        new_filter = request.POST.get('new_filtr',False)
        cs = request.POST.get('crostype',False)
        if len(filter_list)>0 and new_filter:
            respons=filter_respons(filter_list, cs)
            Filters.create(respons,new_filter)
    
    # filters
    c ={
        'name':'filter',
        # 'filters' : filters,
        'filter_sections' : [Filter(k,v) 
                for k,v in  Filters.get_filter_and_sections().items()
                if k != 'currency'
                ]
    }
    try:
        filters = [Filter(v,Filters.get_stocks_by_filter(v)) for v in  Filters.get_filter_and_sections()['User']
                    # if k != 'currency'
                    ]
        c['filters'] = filters
    except:
        pass

    return render(
        request, 'filter.html', c
    )


