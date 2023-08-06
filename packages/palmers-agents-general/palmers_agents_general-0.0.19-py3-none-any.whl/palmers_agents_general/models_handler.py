import base64
import json
import os
import pickle
import sys
import requests


class ModelHandler:
    @classmethod
    def send_to_models(cls, data_dict, inference_url, inference_prefix, inference_protocol, message_max_size):
        # is there a room to release memory here?
        # release memory

        # preprocessed data
        # collect metrics

        inference_results = {}
        for store in data_dict.keys():
            store_data = data_dict[store]
            df = store_data['data']
            model_url = store_data['model_url'] #serve/model_100_endpoint

            data_size = sys.getsizeof(df)
            print(f'store: {store}, data size: {data_size}')
            if data_size > message_max_size:
                raise Exception(f'error: store {store} data size > {message_max_size / (1024 * 1024)} MB')

            # send to model
            pickled = pickle.dumps(df)
            pickled_b64 = base64.b64encode(pickled)
            data_str = pickled_b64.decode('utf-8')
            url = f'{inference_protocol}://{inference_url}/{inference_prefix}/{model_url}'  # Replace with your API endpoint

            if inference_protocol == 'http':
                data = {"body": {"features": data_str}}  # Data to be sent with the POST request

                response = requests.post(url, json=data)


            else:
                raise Exception('only http is supported')

            if response.status_code == 200:
                print(f'Model inference for store {store} successful!')
                response_dict = json.loads(response.text)
                predictions = pickle.loads(base64.b64decode(response_dict['body']['predictions'].encode()))
                inference_results[store] = predictions

            else :
                raise Exception(f'Model inference for store {store} failed!, status code: {response.status_code}')

        return inference_results
