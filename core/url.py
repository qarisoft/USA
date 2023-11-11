


from django.urls import path
from .views import *
urlpatterns = [
    path('',view=index,name='index'),
    path('filter',view=filter,name='filter'),
    path('filter_ajax/',view=filter_ajax,name='filter_ajax'),
    path('delet_filter/<str:filter>',view=delet_filter,name='delet_filter'),
    path('finance/<str:department>',view=finance,name='finance'),
    path('history/<str:department>',view=history,name='history'),
    path('ajax',view=ajax_respons,name='ajax'),
]