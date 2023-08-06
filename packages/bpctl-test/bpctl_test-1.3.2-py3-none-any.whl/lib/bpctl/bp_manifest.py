from base import BaseBPCtl
from config import BP_YAML, BP_YML
import yaml
import json
import os
from sys import stderr, stdout


class BPManifest(BaseBPCtl):
    def __init__(self, args):
        super(BPManifest, self).__init__(args)

    def parse_files(self, current_path):
        if os.path.isfile(current_path):
            if self.validate_file(current_path):
                if self.args.debug:
                    print(current_path)
                return self.apply_manifest(current_path)
        elif os.path.isdir(current_path):
            for file in os.listdir(current_path):
                if file.endswith(BP_YAML):
                    self.parse_files(os.path.join(current_path, file))
                elif file.endswith(BP_YML):
                    self.parse_files(os.path.join(current_path, file))
                elif os.path.isdir(os.path.join(current_path, file)):
                    if self.args.recursive:
                        self.parse_files(os.path.join(current_path, file))
                    else:
                        continue
                else:
                    continue
        else:
            print(f"here is no bp.yaml file found in {current_path} path")
        return True

    # def apply_manifest(self, yml_file_path):
    #     file_contents = self.read_file_content(file_path_with_name=yml_file_path)
    #     print(file_contents)
    #     for file_content in file_contents:
    #         if self.args.debug:
    #             print(type(file_content))
    #             print("File content: "+str(file_content))
    #         bp_manifest_url = self.get_bp_manifest_url()
    #         request_data = self.yaml_parse_into_json(file_content=file_content)
    #         print(request_data)
    #         response = self.post_request(url=bp_manifest_url, request_data=request_data)
    #         if response.status_code == 200:
    #             self.response_handler(response_json=response.json())
    #         elif response.status_code == 400:
    #             self.error_response_handler(response_json=response.json(), request_data=request_data)
    #         elif response.status_code == 401:
    #             print('Invalid Credentials')
    #             quit()
    #             # TODO: needs to be implement re-login
    #         else:
    #             print('Login response code: '+str(response.status_code))
    #             quit()

    def apply_manifest(self, yml_file_path):
        file_contents = self.read_file_content(file_path_with_name=yml_file_path)
        bp_manifest_url = self.get_bp_manifest_url()
        request_data = self.yaml_parse_into_json(file_content=file_contents)
        response = self.post_request(url=bp_manifest_url, request_data=request_data)
        print(response.json())
        response_json = response.json()[0]
        print("******************8")
        print(request_data)
        
        print(response.status_code)
        if response.status_code == 200 and self.args.debug:
            print(f'Raw Response: {response_json}')
        elif response.status_code == 200 or response.status_code == 400:
            for key in response_json.keys():
                if key != 'execution_id' and len(response_json[key]) != 0:
                    if key == "kind_created" or key == "kind_updated":
                        for i in response_json[key]:
                            self.print_response(key, i)
                    if key == "kind_failed":
                        for i in response_json[key]:
                            print(f"Cannot perform create/update on {i['kind']}/{i['name']} due to the following error: {i['error']}")
        elif response.status_code == 401:
            print('Invalid Credentials')
            quit()
        else:
            print('Login response code: '+str(response.status_code))
            quit()

    # def response_handler(self, response_json):
    #     if self.args.debug:
    #         print(f'Raw Response: {response_json}')
    #     if isinstance(response_json, list):
    #         for res in response_json:
    #             self.print_response(res=res)
    #     elif isinstance(response_json, dict):
    #         self.print_response(res=response_json)
    #     else:
    #         print(f'Raw Response: {response_json}')

    # def error_response_handler(self, response_json, request_data):
    #     request_data_json = json.loads(request_data)
    #     print(f"{request_data_json['kind']}/{request_data_json['metadata']['name']}\t errors:")
    #     if isinstance(response_json, list):
    #         for res in response_json:
    #             print(res)
    #     elif isinstance(response_json, dict):
    #         for res in response_json.keys():
    #             print(f"\t{res}\t\t{response_json[res]}", file=stderr)

    # def print_response(self, res):
    #     """gitrepo/bp-gitlab-repo created"""
    #     if 'status' in res:
    #         created_at = res['status']['created_at'].split('.')[0]
    #         updated_at = res['status']['updated_at'].split('.')[0]
    #         if created_at == updated_at:
    #             flag = 'created'
    #         else:
    #             flag = 'updated'
    #         print(f"{res['kind']}/{res['metadata']['name']}\t{flag}")
    #     return True

    def print_response(self, key, i):
        if key == 'kind_created':
             print(f"Successfully created {i['kind']}/{i['name']}")
        else:
            print(f"Successfully updated {i['kind']}/{i['name']}")
        


    def yaml_parse_into_json(self, file_content):
        """
        version: api/v1
        kind: BPGitRepo
        metadata:
         name: manifest-git-repo
        spec:
         git_provider: github
         url: https://github.com
         credential: amit-gitlab
        """
        if isinstance(file_content, str):
            return json.dumps(yaml.safe_load(file_content))
        return json.dumps(file_content)

    def return_bp_yaml_meta_info(self):
        bp_yaml_dir_path = self.args.file
        if os.path.isfile(bp_yaml_dir_path):
            self.validate_file(bp_yaml_dir_path)
            return bp_yaml_dir_path
        if os.path.isdir(bp_yaml_dir_path):
            bp_yaml = os.path.join(bp_yaml_dir_path, BP_YAML)
            bp_yml = os.path.join(bp_yaml_dir_path, BP_YML)
            if os.path.isfile(bp_yaml):
                return bp_yaml
            elif os.path.isfile(bp_yml):
                return bp_yml
            else:
                print("Current working dir there is no bp.yaml file")
                quit()
        else:
            print("Current working dir there is no bp.yaml file")
            quit()

    def read_file_content(self, file_path_with_name):
        with open(file_path_with_name, 'r') as file:
            file_content = file.read()
        data = list(yaml.load_all(file_content, Loader=yaml.SafeLoader))
        return data
