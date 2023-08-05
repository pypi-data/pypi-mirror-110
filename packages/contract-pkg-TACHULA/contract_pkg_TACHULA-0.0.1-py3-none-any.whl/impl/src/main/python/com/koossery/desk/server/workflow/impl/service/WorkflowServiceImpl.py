from src.contract.src.main.python.com.koossery.desk.server.workflow.contract.exceptions.WorkflowServerException import \
    WorkflowSeverException
from src.contract.src.main.python.com.koossery.desk.server.workflow.contract.service.IWorkflowService import  IWorkflowService
from src.contract.src.main.python.com.koossery.desk.server.workflow.contract.dto.ResultDTO import ResultDTO

class WorkflowServiceImpl(IWorkflowService):
    def find(toolID: str) :
        #define function to find workflows from a tool ID
        raise WorkflowSeverException
        return [{"credential":null,"lazyLoadArrayList":null,"propertiesModified":[],"id":"wf1","toolID":"123","name":"workflow 1","description":"w1 desc","owner":"meli","public":true},{"credential":null,"lazyLoadArrayList":null,"propertiesModified":[],"id":"wf2","toolID":"123","name":"workflow 2","description":"w2 desc","owner":"Jerry","public":true}]

    def run(toolID: str, workflowID: str, ImageID):
        raise WorkflowSeverException
        result= ResultDTO()
        return result
