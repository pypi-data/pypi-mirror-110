"""
`wallaroo` -- Python SDK for Wallaroo
======================================
"""

import json
import logging
import requests
import os
import sys
import pickle
import onnx
import time
import datetime
import re

# temporarily here while the bundle storage is migrated to minio
from google.cloud import storage


def _validate_dns_name_fn(name):
    regex = re.compile('^(?![0-9]+$)(?!-)[a-zA-Z0-9-]{,63}(?<!-)$')
    valid = regex.match(name) is not None
    assert valid , '''model_id must be a valid DNS-1123 subdomain. It must consist of lower
                        case alphanumeric characters, \'-\' or \'.\', and must start and end with
                        an alphanumeric character (e.g. \'example.com\', regex used for validation
                        is \'[a-z0-9]([-a-z0-9]*[a-z0-9])?(\\.[a-z0-9]([-a-z0-9]*[a-z0-9])?)*\''''

class Engine:
    def __new__(cls, **kwargs):
        # Future work - To be replaced by Fitzroy handshake
        if 'host' in kwargs:
            host = kwargs["host"]
        else: host = 'engine-lb'
        if 'debug' in kwargs:
            debug = kwargs["debug"]
        else: debug = False
        if 'rest_port' in kwargs:
            rest_port = kwargs["rest_port"]
        else: rest_port = 23352
        if 'data_port' in kwargs:
            data_port = kwargs["data_port"]
        else: data_port = 29502
        if 'scheme' in kwargs:
            scheme = kwargs["scheme"]
        else: scheme = 'http'
        if 'interactive' in kwargs:
            interactive = kwargs["interactive"]
        else: interactive = False

        url = f'{scheme}://{host}:{rest_port}'

        # Set up Logging
        logger = logging.getLogger()
        while logger.hasHandlers():
            logger.removeHandler(logger.handlers[0])

        logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
        logger = logging.getLogger()

        fileHandler = logging.FileHandler("wl_log.log")
        fileHandler.setFormatter(logFormatter)
        logger.addHandler(fileHandler)

        consoleHandler = logging.StreamHandler((sys.stdout))
        consoleHandler.setFormatter(logFormatter)

        if (debug):
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)
        # Also print to std out
        if (interactive):
            logger.addHandler(consoleHandler)

        try:
            r = requests.get(url)
            if r.status_code == 400:
                logger.info(f'ok: {url} ready')
                # allocate Wallaroo object only if handshake succeeds
                return super().__new__(cls)
        except:
            logger.error(f'fail: {url} endpoint is down')
            return None

    def __init__(self, host='engine-lb', debug=False, interactive=False, rest_port=23352, data_port=29502, scheme='http'):
        """Configure the connection to the Wallaroo API

        Args:
            host (str): IP address of the Wallaroo model-server.
            debug (bool, optional): SDK debug mode. Defaults to False.
            rest_port (int, optional): Port for model upload and managent. Defaults to 23352.
            data_port (int, optional): Port for data ingestion. Defaults to 29502.
            scheme (str, optional): Protocol to be used for the inference generation (tcp/http). Defaults to 'http'.
        """
        self.host = host
        self.rest_port = rest_port
        self.data_port = data_port
        self.scheme = scheme
        self.debug = debug
        self.interactive = interactive
        self.log = logging.getLogger()

    def upload_model(self, model_id, model_version, model_path):
    #  runtime='onnx'): Pending fix in the API
        """Uploads a model from the local file system to the Wallaroo model-storage

        Args:
            model_id (str): Model storage unique identifier
            model_version (str): Model version
            model_path (str): location of the model in the local file system
        """
        _validate_dns_name_fn(model_id)
        #TODO: call the model_conversion tool to automatically determine if the model can be converted to ONNX
        url = f'{self.scheme}://{self.host}:{self.rest_port}/models'

        try:
            with open(model_path, 'rb') as model_filehandle:
                files = { 'upload': model_filehandle }
                data = { 'model_id': model_id,
                         'model_version': model_version }
                        #  'runtime': runtime } Pending fix to the API
                r = requests.post(url, files=files, data=data)

                if self.debug:
                    self.log.debug(model_path)
                    self.log.debug(files.items())
                    self.log.debug(data.items())
                    # self.log.debug(curlify.to_curl(r.request,compressed=True))

                if r.status_code == 200:
                    self.log.info(f'ok: {url} -> {r.status_code}, {r.text}')
                else:
                    self.log.error(f'fail: {url} -> {r.status_code}, {r.text}')

        except OSError as err:
            self.log.exception(f'Error uploading model {model_path}:\n -- {err}')

    def update_model_config(self, model_id, *tensor_fields):
        """Updates the configuration of an existing model in the Wallaroo model storage

        Args:
            model_id (str): Model storage unique identifier
            tensor_fields (list): List of names of tensor fields available in the input data.
        """
        _validate_dns_name_fn(model_id)
        url = f'{self.scheme}://{self.host}:{self.rest_port}/model_config'
        data = {'model_id': model_id,
                'tensor_fields': tensor_fields}
        r = requests.post(url, json=data)

        if r.status_code == 200:
            self.log.info(f'ok: {url} -> {r.status_code}, {r.text}')
        else:
            self.log.error(f'fail: {url} -> {r.status_code}, {r.text}')

    # Filters Fitzroy output looking only for the "data" fields and returns a list of lists, one list per each model output.
    def __filter_data(self, raw_data):
        out = []
        for x in raw_data:
            for item, value in x.items():
                for attribute,v in value.items():
                    if attribute == 'data':
                        out.append(v)
        return(out)

    def http_inference_tensor(self, model_id, tensor, data_type='Float', show_result=False):
        """Sends a tensor object (in json format) to score in the model-server

        Args:
            model_id (str): Model storage unique identifier
            tensor (str): json object containing the expected inputs of the model
            data_type (str): (Float/Double) defines the precision of the tensor fields
            show_result (bool, optional): prints the model-server response on screen when set to 'True'
        """

        _validate_dns_name_fn(model_id)
        #TODO: validate data_type possible inputs to Float/Double only
        url = f'{self.scheme}://{self.host}:{self.data_port}/models/{model_id}'
        r = requests.post(url, json=tensor)
        data = []
        elapsed = r.elapsed.total_seconds()

        r_txt = json.loads(r.text)
        if(r_txt):
            if r.status_code == 200:
                    if any(tag == 'error' for tag in r_txt[0] ):
                        self.log.error(r_txt[0]['error'])
                        # r_txt[0]['outputs'][0]['Float']['data']
                    else:
                        self.log.info(f'ok: {url} -> {r.status_code}')
                        self.log.info(f'elapsed time: {elapsed}')
                        raw_data = r_txt[0]['outputs']
                        data = self.__filter_data(raw_data)
                        if show_result == True:
                            print(r.text)
        else:
            self.log.error(f'fail: {url} -> {r.status_code}, {r.text}')

        if show_result == True:
            print(r.text)

        return (data, elapsed)

    def http_inference_file(self, model_id, data_path, data_type='Float', show_result=False):
        """Sends a file containing a tensor object (in json format) to score in the model server

        Args:
            model_id (str): Model storage unique identifier
            data_path (str): location of the model in the local file system
            data_type (str): (Float/Double) defines the precision of the tensor fields
            show_result (bool, optional): prints the model-server response on screen when set to 'True'
        """
        _validate_dns_name_fn(model_id)
        #TODO: validate data_type possible inputs to Float/Double only
        url = f'{self.scheme}://{self.host}:{self.data_port}/models/{model_id}'

        try:
            with open(data_path, 'r') as data_filehandle:
                r = requests.post(url, json=json.load(data_filehandle))
        except OSError as err:
            self.log.exception(f'Error uploading model {data_path}:\n -- {err}')
            # print(f'Upload model: {r.text}')

        data = []
        elapsed = r.elapsed.total_seconds()

        r_txt = json.loads(r.text)
        if(r_txt):
            if r.status_code == 200:
                if any(tag == 'error' for tag in r_txt[0] ):
                    self.log.error(r_txt[0]['error'])
                # r_txt[0]['outputs'][0]['Float']['data']
                else:
                    self.log.info(f'ok: {url} -> {r.status_code}')
                    self.log.info(f'elapsed time: {elapsed}')
                    raw_data = r_txt[0]['outputs']
                    data = self.__filter_data(raw_data)
                    if show_result == True:
                        print(r.text)
        else:
            self.log.error(f'fail: {url} -> {r.status_code}, {r.text}')

        if show_result == True:
            print(r.text)

        return (data, elapsed)

class Bundle:
    # def __init__(self,prep_queries,work_table_name,prep_fn,data_treatment,post_fn,model_vars,prediction_column,target_var,model):
        # """Contains a pre-trained model, data queries to generate data from the "work" table and optional pre/post scoring functions.

        # Args:
        #     prep_queries (list): List of queries to be applied to the "work" table
        #     work_table_name (str]): Name of the "work" table to be used to obtain the data
        #     prep_fn (marshal function): Function to be applied to the data before scoring takes place
        #     data_treatment (unsupervisedTreatment): Pre-score data transformation function
        #     post_fn (marshal function): Function to be applied to the data after scoring takes place
        #     model_vars (list): Names of the columns of interest in the dataset
        #     prediction_column (str): Name of the variable to be predicted
        #     target_var (str): Name of the target variable
        #     model (model_object): Model object in a format supported by Wallaroo (sklearn/tensorflow)
        # """
        # self.prep_queries = prep_queries
        # self.work_table_name = work_table_name
        # self.prep_fn = prep_queries
        # self.data_treatment = data_treatment
        # self.post_fn = post_fn
        # self.model_vars = model_vars
        # self.prediction_column = prediction_column
        # self.target_var = target_var
        # self.model = model

    # NiFi API wrapper to retrieve the ID of a NiFi processor in the current flow
    @staticmethod
    def __retrieve_id(component_name):
        url = f'http://nifi-service:8081/nifi-api/flow/search-results?q={component_name}'
        r = requests.get(url)
        if r.status_code == 200:
            results = json.loads(r.text)['searchResultsDTO']['processorResults']
            for elem in results:
                if elem['name'] == component_name:
                    id = elem['id']
        return(id)
    # NiFi API wrapper to retrieve the errors present in the current NiFi flow
    @staticmethod
    def __get_bulletins(component_id=''):
        bulletin_list = []
        url = f'http://nifi-service:8081/nifi-api/flow/bulletin-board'
        r = requests.get(url)
        if r.status_code == 200:
#             fobj1 = open('bulletin.json')
            bulletinBoard = json.loads(r.text)['bulletinBoard']
#             bulletinBoard = json.load(fobj1)['bulletinBoard']
            bulletins = bulletinBoard['bulletins']
            generated = bulletinBoard['generated']
            for bulletin in bulletins:
                if component_id:
                    if bulletin['bulletin']['sourceId'] == component_id:
                        bulletin_list.append(bulletin['bulletin'])
                else:
                    bulletin_list.append(bulletin['bulletin'])
            return bulletin_list, generated
    @staticmethod
    def upload_score_bundle_fn(gcp_bucket_name, bundle,model_id, model_ver, execution_freq='live', show_result=False, timeout_secs=120):
        """Uploads data bundles for scoring, which get scheduled for inference on a first-come
        first served basis. Optionally the bundles can be scheduled to be scored at pre-defined
        intervals: daily, monthly, weekly.

        Args:
            gcp_bucket_name (str): Name of a wallaroo-enabled gcp bucket in the cluster (a nifi flow needs to be enabled for this bucket)
            bundle (dict): Dictionary containing all required budle items: prep_queries,work_table_name,prep_fn,data_treatmetn,post_fn,model_vars,prediction_column,target_var,model.
            model_id (str): Model storage unique identifier
            model_ver (str): Model version
            execution_freq (str, optional): live/daily/weekly pre-defined intervals of time in which the model will be automatically scored. Defaults to 'live' (as soon as possible).
            show_results (bool): prints the job completion success message when set to 'True'
            timeout_secs (int): number of seconds to wait for successful completion or error (Note: the job is executed regardless). Default 2 minutes.
        """
        _validate_dns_name_fn(model_id)
        assert isinstance(bundle['model'], onnx.ModelProto), "Model is not in ONNX format'"

        success_msg = "Successfully put StandardFlowFileRecord"
        gcp_client = storage.Client()
        dir=(f'models/{execution_freq}/{model_id}/{model_ver}')
        bucket = gcp_client.get_bucket(gcp_bucket_name)
        blob=bucket.blob(dir)

        exec_script_comp_id = Bundle.__retrieve_id(f'ExecuteStreamCommand_{execution_freq}')
        gcs_put_comp_id = Bundle.__retrieve_id(f'PutGCSObject_{execution_freq}')
        # Check for pre-existing bulletins & save generation time
        bulletins, generated = Bundle.__get_bulletins()
        generated_t = time.strptime(generated, "%H:%M:%S UTC")

        # Do not accept duplicated file blobs identifiers
        blob.upload_from_string(pickle.dumps(bundle),if_generation_match=0)

        # Standard success message produced by the GCP API
        success_msg = "Successfully put StandardFlowFileRecord"
        timeout = timeout_secs # Default timeout of 2 minutes

        errors_present = False
        errors = ''
        msg = "Timeout ocurred"
        wait_until = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
        try:
            while True:
                bulletins, generated_new = Bundle.__get_bulletins()
                for bulletin in bulletins:
                #     print(bulletin['timestamp'])
                    if time.strptime(bulletin['timestamp'], "%H:%M:%S UTC") > generated_t:
#                         print(bulletin['timestamp'])
                        if bulletin['sourceId'] == gcs_put_comp_id:
                            if success_msg in bulletin['message']:
                                msg = bulletin['message']
                                if show_result == True:
                                    print(msg)
                                return
                        # If not finished successfully, look for errors
                        if bulletin['sourceId'] == exec_script_comp_id:
                            if bulletin['level'] == 'ERROR':
                                errors_present = True
                                errors += bulletin['message']
                                msg = errors
                time.sleep(2)
                if wait_until < datetime.datetime.now() or errors_present:
                    raise Exception(msg)
        except Exception as error:
            print(error)
