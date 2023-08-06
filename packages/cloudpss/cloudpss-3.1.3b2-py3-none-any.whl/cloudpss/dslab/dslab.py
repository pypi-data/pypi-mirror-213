import json
from ..utils import request
from ..model.model import Model
from .dataManageModel import DSLabDataManageModel
from .financialAnalysisModel import DSLabFinancialAnalysisModel
from  .DSLabFinancialResult import DSLabResult

class DSLab(object):
    def __init__(self, project={}):
        '''
            初始化
        '''
        self.id = project.get('id', None)
        self.resource = project.get('resource', None)
        self.name = project.get('name', None)
        self.__modelRid = project.get('model', None)
        if self.__modelRid is not None:
            self.model = Model.fetch(self.__modelRid)
        self.dataManageModel = DSLabDataManageModel(self.resource)
        self.financialAnalysisModel = DSLabFinancialAnalysisModel(self.resource)
        self.dsLabResult = DSLabResult(self.resource)

    @staticmethod
    def fetch(simulationId):
        '''
            获取算例信息

            :params: simulationId string类型，代表数据项的算例id

            :return: DSLab
        '''
        try:
            r = request(
                'GET', 'api/ies/rest/simulation/{0}'.format(simulationId))
            project = json.loads(r.text)
            return DSLab(project)
        except Exception as e:
            if 'Unauthorized' in str(e): 
                raise Exception('token 无效')
            else:
                raise Exception('未查询到当前算例')

    def run(self, job=None, name=None):
        '''
            调用仿真 

            :params job:  调用仿真时使用的计算方案，不指定将使用算例保存时选中的计算方案
            :params name:  任务名称，为空时使用项目的参数方案名称和计算方案名称

            :return: 返回一个运行实例
        '''
        if job is None:
            currentJob = self.model.context['currentJob']
            job = self.model.jobs[currentJob]

        job['args']['simulationId'] = self.id
        return self.model.run(job, name=name)
    
    def dsLabRun(self):
        '''
            生成方案优选算例

            :return: 方案优选运行实例
        '''
    pass

