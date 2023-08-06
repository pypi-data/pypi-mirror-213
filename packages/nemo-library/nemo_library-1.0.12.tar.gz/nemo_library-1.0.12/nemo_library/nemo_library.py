import configparser
import json
import math
import os

import pandas as pd
import requests

from nemo_library.symbols import (
    ENDPOINT_URL_PROJECT_FILE_RE_UPLOAD_ABORT,
    ENDPOINT_URL_PROJECT_FILE_RE_UPLOAD_FINALIZE,
    ENDPOINT_URL_PROJECT_FILE_RE_UPLOAD_INITIALIZE,
    ENDPOINT_URL_PROJECT_FILE_RE_UPLOAD_KEEP_ALIVE,
    ENDPOINT_URL_PROJECT_PROPERTIES,
    ENDPOINT_URL_PROJECTS,
    ENDPOINT_URL_REPORT_RESULT,
    FILE_UPLOAD_CHUNK_SIZE,
)

NEMO_URL = "https://enter.nemo-ai.com"


class NemoLibrary:
    #################################################################################################################################################################

    def __init__(self):
        config = configparser.ConfigParser()
        config.read("config.ini")
        self._environment_ = config["nemo_library"]["environment"]
        self._userid_ = config["nemo_library"]["userid"]
        self._password_ = config["nemo_library"]["password"]
        self._nemo_url_ = config["nemo_library"]["nemo_url"]

        match self._environment_:
            case "demo":
                self._cognito_url_ = "https://cognito-idp.eu-central-1.amazonaws.com/eu-central-1_1ZbUITj21"
                self._cognito_appclientid = "7tvfugcnunac7id3ebgns6n66u"
                self._cognito_authflow_ = "USER_PASSWORD_AUTH"
            case "dev":
                self._cognito_url_ = "https://cognito-idp.eu-central-1.amazonaws.com/eu-central-1_778axETqE"
                self._cognito_appclientid = "4lr89aas81m844o0admv3pfcrp"
                self._cognito_authflow_ = "USER_PASSWORD_AUTH"
            case "prod":
                self._cognito_url_ = "https://cognito-idp.eu-central-1.amazonaws.com/eu-central-1_1oayObkcF"
                self._cognito_appclientid = "8t32vcmmdvmva4qvb79gpfhdn"
                self._cognito_authflow_ = "USER_PASSWORD_AUTH"
            case _:
                raise Exception(f"unknown environment '{self._environment_}' provided")

        super().__init__()

    #################################################################################################################################################################

    def _login(self):
        headers = {
            "X-Amz-Target": "AWSCognitoIdentityProviderService.InitiateAuth",
            "Content-Type": "application/x-amz-json-1.1",
        }

        authparams = {"USERNAME": self._userid_, "PASSWORD": self._password_}

        data = {
            "AuthParameters": authparams,
            "AuthFlow": self._cognito_authflow_,
            "ClientId": self._cognito_appclientid,
        }

        # login and get tokenb

        response_auth = requests.post(
            self._cognito_url_, headers=headers, data=json.dumps(data)
        )
        if response_auth.status_code != 200:
            raise Exception(
                f"request failed. Status: {response_auth.status_code}, error: {response_auth.text}"
            )
        tokens = json.loads(response_auth.text)
        return tokens["AuthenticationResult"]["IdToken"]

    #################################################################################################################################################################

    def _get_file_size_in_characters_(self,file_path):
        character_count = 0
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                character_count += len(line)
        return character_count

    #################################################################################################################################################################

    def _split_file_(self, file_path, chunk_size):
        with open(file_path, "r", encoding="utf-8") as file:
            while True:
                data = file.read(chunk_size)
                if not data:
                    break
                yield data

    #################################################################################################################################################################

    def getProjectList(self, token=None):
        if token is None:
            token = self._login()

        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }
        response = requests.get(
            self._nemo_url_ + ENDPOINT_URL_PROJECTS, headers=headers
        )
        if response.status_code != 200:
            raise Exception(
                f"request failed. Status: {response.status_code}, error: {response.text}"
            )
        resultjs = json.loads(response.text)
        df = pd.json_normalize(resultjs)
        return df

    #################################################################################################################################################################

    def UploadFile(self, projectname, filename):
        # define some variables
        token = None
        upload_id = None
        project_id = None
        headers = None

        try:
            token = self._login()

            print(
                f"upload of file '{filename}' into project '{projectname}' initiated..."
            )

            df = self.getProjectList(token=token)
            crmproject = df[df["displayName"] == projectname]
            if len(crmproject) != 1:
                raise Exception(f"could not identify project name {projectname}")
            project_id = crmproject["id"].to_list()[0]

            print("project id:", project_id)

            ####
            # start upload process

            # we need to upload file in chunks. Default is 6MB size chunks

            # usually we would get the file size with os.path.getsize(filename) - but this is
            # the size in Bytes, not in (UTF-8)-characters. So we have to calculate the size
            # by our own

            file_size = self._get_file_size_in_characters_(filename)
            total_chunks = math.ceil(file_size / FILE_UPLOAD_CHUNK_SIZE)

            print(f"file size: {file_size:,}")
            print(f"chunk size: {FILE_UPLOAD_CHUNK_SIZE:,}")
            print(f"--> total chunks: {total_chunks:,}")
            headers = {
                "accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            }
            data = {"projectId": project_id, "partCount": total_chunks}

            # initialize upload
            response = requests.post(
                self._nemo_url_ + ENDPOINT_URL_PROJECT_FILE_RE_UPLOAD_INITIALIZE,
                headers=headers,
                json=data,
            )
            if response.status_code != 200:
                raise Exception(
                    f"request failed. Status: {response.status_code}, error: {response.text}"
                )
            resultjs = json.loads(response.text)
            df = pd.json_normalize(resultjs)
            upload_id = resultjs["uploadId"]
            upload_urls = resultjs["urls"]
            partETags = pd.DataFrame({"partNumber": [None], "eTag": [None]})

            file_chunks = self._split_file_(filename, FILE_UPLOAD_CHUNK_SIZE)

            for index, url in enumerate(upload_urls, start=1):
                # post keep alive message

                karesponse = requests.post(
                    url=self._nemo_url_
                    + ENDPOINT_URL_PROJECT_FILE_RE_UPLOAD_KEEP_ALIVE.format(
                        projectId=project_id, uploadId=upload_id
                    ),
                    headers=headers,
                )
                if (
                    karesponse.status_code != 204
                ):  # this is the defined response that we expect, not 200
                    raise Exception(
                        f"request failed. Status: {karesponse.status_code}, error: {karesponse.text}"
                    )

                print(f"upload part {index}")
                headers_upload = {
                    "Content-Type": "text/csv",
                }
                data = next(file_chunks, None)

                response = requests.put(
                    url=url,
                    headers=headers_upload,
                    data=data.encode("utf-8"),
                )
                if response.status_code != 200:
                    raise Exception(
                        f"request failed. Status: {response.status_code}, error: {response.text}"
                    )

                partETags.at[index - 1, "partNumber"] = index
                partETags.at[index - 1, "eTag"] = response.headers["ETag"].strip('"')

            print("finalize upload")

            data = {
                "uploadId": upload_id,
                "projectId": project_id,
                "fieldDelimiter": ";",
                "recordDelimiter": "\n",
                "partETags": partETags.to_dict(orient="records"),
            }
            datajs = json.dumps(data, indent=2)
            response = requests.post(
                self._nemo_url_ + ENDPOINT_URL_PROJECT_FILE_RE_UPLOAD_FINALIZE,
                headers=headers,
                data=datajs,
            )
            if response.status_code != 204:
                raise Exception(
                    f"request failed. Status: {response.status_code}, error: {response.text}"
                )

            print("upload finished")

        except Exception as e:
            if token == None:
                raise Exception("upload stopped, no token available")

            if project_id == None:
                raise Exception("upload stopped, no project_id available")

            if upload_id == None:
                raise Exception("upload stopped, no upload_id available")

            # we are sure that all information to anbandon the upload are available, we do so now

            data = {"uploadId": upload_id, "projectId": project_id}
            response = requests.post(
                self._nemo_url_ + ENDPOINT_URL_PROJECT_FILE_RE_UPLOAD_ABORT,
                headers=headers,
                json=data,
            )
            if response.status_code != 204:
                raise Exception(
                    f"request failed. Status: {response.status_code}, error: {response.text}"
                )

            raise Exception("upload aborted")

    #################################################################################################################################################################

    def LoadReport(self, report_guid, max_pages=None):
        print(f"Loading report: {report_guid}")

        token = self._login()
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }

        page = 0
        result = pd.DataFrame()

        while True:
            page += 1

            print("loading page:", page)

            # INIT REPORT PAYLOAD (REQUEST BODY)
            report_params = {"report_id": report_guid, "page": page}

            response_report = requests.post(
                self._nemo_url_ + ENDPOINT_URL_REPORT_RESULT,
                headers=headers,
                json=report_params,
            )

            if response_report.status_code != 200:
                raise Exception(
                    f"request failed. Status: {response_report.status_code}, error: {response_report.text}"
                )

            # Parse REPORT Respone
            resultjs = json.loads(response_report.text)
            records = resultjs["records"]

            df = pd.json_normalize(records)
            if page == 1:
                result = df
            else:
                result = pd.concat([result, df], ignore_index=True)

            if resultjs["max_page"] <= page:
                break

            if not max_pages is None and max_pages <= page:
                break

        return result

    #################################################################################################################################################################

    def ProjectProperty(self, propertyname):
        token = self._login()
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }

        ENDPOINT_URL = self._nemo_url_ + ENDPOINT_URL_PROJECT_PROPERTIES.format(
            request=propertyname
        )

        response = requests.get(ENDPOINT_URL, headers=headers)

        if response.status_code != 200:
            raise Exception(
                f"request failed. Status: {response.status_code}, error: {response.text}"
            )

        return response.text
