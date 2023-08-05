from django.urls import path
from django.urls import include
from . import ToolCtrl

urlpatterns = [
    path('tools/find', ToolCtrl.find, name='find')

]
