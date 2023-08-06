import json
import unittest
import argparse
import responses
import time
from unittest.mock import Mock
from ibm_ai_openscale_cli.ml_engines.watson_machine_learning import WatsonMachineLearningEngine
from ibm_watson_machine_learning import APIClient
from unittest.mock import patch
from ibm_ai_openscale_cli.openscale.openscale_client import OpenScaleClient
from ibm_ai_openscale_cli.utility_classes.fastpath_logger import FastpathLogger
from ibm_ai_openscale_cli.utility_classes.utils import jsonFileToDict

logger = FastpathLogger(__name__)

credentials = {
    'apikey': 'XXX-YYYY-ZZZZ', #pragma: allowlist secret
    'iam_apikey_description': 'Auto-generated for key XXX-YYY-ZZZ',
    'iam_apikey_name': 'openscale-fastpath-credentials',
    'iam_role_crn': 'crn:v1:bluemix:public:iam::::serviceRole:Writer',
    'iam_serviceid_crn': 'crn:v1:bluemix:public:iam-identity::a/24b635831eec4c8fb9b0a71fb3f37cbd::serviceid:ServiceId-8d8b193e-644f-4d5b-8cfc-99abb44b87d9', #pragma: allowlist secret
    'instance_id': '9ddf4149-9ddf4149-9ddf4149',
    'url': 'https://us-south.ml.cloud.ibm.com',
    'instance_name': 'fastpath_test_wml_instance',
    'instance_crn': 'crn:v1:bluemix:public:iam-identity::a/24b635831eec4c8fb9b0a71fb3f37cbd::serviceid:ServiceId-8d8b193e-644f-4d5b-8cfc-99abb44b87d9' #pragma: allowlist secret
}
cos_credentials = {
    "apikey": "apikey123", #pragma: allowlist secret
    "resource_instance_id": "resource123",
    "instance_name": "test_cos_instance"
}

class OpenScale:

    def timer(self, tag, seconds, count=1):
        logger.log_timer('{} in {:.3f} seconds'.format(tag, seconds))
    
    def get_datamart_id(self):
        return "123"

class Deployments:
    class ConfigurationMetaNames:
        NAME = "Artifact Deployment"
        DESCRIPTION = "Description of deployment"
        ONLINE = None

    def get_details(self, deployment_uid=None, limit=None):
        return
    
    def create(self, artifact_uid=None, name=u'Artifact deployment', description=u'Description of deployment', 
               asynchronous=False, deployment_type=u'online', 
               deployment_format='Core ML', meta_props=None, **kwargs):
        return {'metadata': {'guid': '7e1e74fe-db51-7e1e74fe-88823b367add',
                            'id': '7e1e74fe-db51-7e1e74fe-88823b367add'}, 
                'entity': {"status": {"online_url": {
                    "url": "https://us-south.ml.cloud.ibm.com/v2/deployments/7e1e74fe-db51-7e1e74fe-88823b367add/online"}}}}

    def delete(self, deployment_uid):
        return

    def score(self, scoring_url, payload, transaction_id=None):
        return

class Set:
    def default_space(self, space_id):
        return "SUCCESS"

class Spaces:
    class ConfigurationMetaNames:
        NAME = "test_fp_space"
    def create(self, ):
        return {"metadata":{"id": "test_fp_spaceid"}, "entity":{"name":"openscale-express-path-123"}}

    def store(self, meta_props):
        return {"metadata":{"id": "testspace123"},"entity":{"name":"openscale-express-path-123"}}
    
    def get_details(self):
        return {"resources":[
            {"metadata":{"id": "testspace123"},"entity":{"name":"openscale-express-path-123"}}]}
    

class Repository:

    class ModelMetaNames():
        NAME = "name"
        FRAMEWORK_NAME = ""
        FRAMEWORK_VERSION = ""
        FRAMEWORK_LIBRARIES = ""
        RUNTIME_NAME = "runtime_name"
        RUNTIME_VERSION = "runtime_version"
        TRAINING_DATA_SCHEMA = ""
        EVALUATION_METHOD = ""
        EVALUATION_METRICS = ""
        LABEL_FIELD = ""
        OUTPUT_DATA_SCHEMA = ""
        INPUT_DATA_SCHEMA = ""
        SOFTWARE_SPEC_UID = ""
        TYPE = ""
        
    def store_definition(self, training_definition, meta_props):
        return

    def get_model_details(self, model_uid=None, limit=None):
        return {'resources' : ''}

    def get_function_details(self, function_uid=None, limit=None):
        return {'resources' : ''}

    def delete(self, artifact_uid):
        return
    
    def get_model_uid(self, model_details):
        return 'bb5ab012-1718-bb5ab012-bb5ab012'
    
    def get_model_id(self, model_details):
        return 'bb5ab012-1718-bb5ab012-bb5ab012'

    def get_function_uid(function_details):
        return
    
    def store_function(self, function, meta_props):
        return
    
    def store_model(self, model, meta_props=None, training_data=None, training_target=None, pipeline=None, feature_names=None, label_column_names=None):
        return jsonFileToDict(filename = "openscale_fastpath_cli/tests/test_props/model_details.json")

    def list_models(self, limit=None):
        return

class ServiceInstance:

    def get_instance_id(self):
        return '7e1e74fe-db51-7e1e74fe-88823b367add'

def version():
    return '1.0.378'



#wmle = WatsonMachineLearningEngine(credentials, openscale_client = None, False, False)
openscale_client = OpenScale()
with patch('ibm_ai_openscale_cli.ml_engines.watson_machine_learning.APIClient') as MockClass:
    instance = MockClass.return_value
    instance.wml_credentials = credentials
    instance.version = version()
    instance.repository = Repository()
    instance.deployments = Deployments()
    instance.service_instance = ServiceInstance()
    instance.spaces = Spaces()
    instance.set = Set()

    wmle = WatsonMachineLearningEngine(credentials, openscale_client, cos_credentials=cos_credentials, is_v4=True)
    wmle._model_metadata = { 'model_file' : "openscale_fastpath_cli/tests/test_props/model_content.gzip", 'model_name': 'GermanCreditRiskModel', 'deployment_name' : 'GermanCreditRiskModel',
                            'model_metadata_file' :  "openscale_fastpath_cli/tests/test_props/model_meta.json" , 'deployment_description' : 'Created by Watson OpenScale Express Path'}

    class TestWatsonMachineLearning(unittest.TestCase):
        def test_reliable_create_model(self):
            response = wmle._reliable_create_model(model_file = "openscale_fastpath_cli/tests/test_props/model_content.gzip", model_props = jsonFileToDict(filename = "openscale_fastpath_cli/tests/test_props/model_props.json") )
            assert response == jsonFileToDict(filename = "openscale_fastpath_cli/tests/test_props/model_details.json")


        def test_create_model(self):
            model_metadata, model_guid, model_url = wmle._create_model(model_name= 'GermanCreditRiskModel', model_metadata_file = "openscale_fastpath_cli/tests/test_props/model_meta.json")
            assert model_metadata == jsonFileToDict(filename = "openscale_fastpath_cli/tests/test_props/model_meta.json")
            assert model_guid == 'bb5ab012-1718-bb5ab012-bb5ab012'
        

        def test_reliable_deploy_model(self):
            elapsed, response_deployment_details = wmle._reliable_deploy_model(model_guid = '2aebd3d1-43ae-43e4-a602-93e95ed23fe8', 
                                                            deployment_name = 'GermanCreditRiskModel',
                                                            deployment_description = 'Created by Watson OpenScale Express Path')
            assert response_deployment_details == {'metadata': {'guid': '7e1e74fe-db51-7e1e74fe-88823b367add', 'id': '7e1e74fe-db51-7e1e74fe-88823b367add'}, 'entity': {'status': {'online_url': {'url': 'https://us-south.ml.cloud.ibm.com/v2/deployments/7e1e74fe-db51-7e1e74fe-88823b367add/online'}}}}



        def test_deploy_model(self):
            response_deployment_guid, _ = wmle._deploy_model(model_guid = '2aebd3d1-43ae-43e4-a602-93e95ed23fe8', 
                                                            deployment_name = 'GermanCreditRiskModel',
                                                            deployment_description = 'Created by Watson OpenScale Express Path')
            assert response_deployment_guid == '7e1e74fe-db51-7e1e74fe-88823b367add'


        def test_create_model_and_deploy(self):
            response_model_deployment_dict = wmle.create_model_and_deploy()
            del response_model_deployment_dict["deployment_url"]
            del response_model_deployment_dict["model_url"]
            assert response_model_deployment_dict == jsonFileToDict(filename = "openscale_fastpath_cli/tests/test_props/model_deployment_dict.json")
        
