import logging
from rest_framework.decorators import api_view
from django.http import JsonResponse
from src.impl.src.main.python.com.koossery.desk.server.workflow.impl.service.ToolServiceImpl import ToolServiceImpl
from src.contract.src.main.python.com.koossery.desk.server.workflow.contract.exceptions.ToolServerException import \
    ToolSeverException


@api_view(['GET'])
def find(request):
    name = request.GET.get('name')
    return JsonResponse(ToolServiceImpl.find(name), safe=False)
