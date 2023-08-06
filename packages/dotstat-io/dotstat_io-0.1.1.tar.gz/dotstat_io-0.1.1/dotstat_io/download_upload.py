import os
import requests
import chardet
import xml.etree.ElementTree as ET

from pathlib import Path
from time import sleep


# class to download or upload data from/to .Stat Suite
class Download_upload():

    # Declare constants
    __ERROR  = "An error occurred: "
    __EXECUTION_IN_PROGRESS = "InProgress"
    __DOWNLOAD_SUCCESS = "Successful download"
    __UPLOAD_SUCCESS = "The request was successfully processed"

    __NAMESPACE_MESSAGE = "{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message}"
    __NAMESPACE_COMMON = "{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common}"
  
    # Initialise Download_upload
    def __init__(self, token):
        self.token = token

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.token = None


    # Download a file from .STAT
    def download_file(self, dotstat_url: str, content_format: str, file_path: Path):
        try:
            Returned_Message = ""

            if (self.token == None):
                Returned_Message = self.__ERROR  + "No token" + os.linesep
            else:
                headers = {
                   'accept': content_format,
                   'authorization': 'Bearer '+self.token
                }

                #
                response = requests.get(
                    dotstat_url, verify=True, headers=headers)

        except Exception as err:
            Returned_Message = self.__ERROR  + str(err) + os.linesep
        else:
            if response.status_code != 200:
                Returned_Message = self.__ERROR  + 'Error code: ' + \
                    str(response.status_code) + ' Reason: ' + str(response.reason)
                if len(response.text) > 0:
                    Returned_Message += os.linesep + 'Text: ' + response.text
            else:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                with open(file_path, "wb") as file:
                    file.write(response.content)
                    Returned_Message = self.__DOWNLOAD_SUCCESS
                file.close()
        finally:
            return Returned_Message


    # Download streamed content from .STAT
    def download_stream(self, dotstat_url: str, content_format: str):
        try:
            Returned_Message = ""

            if (self.token == None):
                Returned_Message = self.__ERROR  + "No token" + os.linesep
            else:
                headers = {
                    'accept': content_format,
                    'Transfer-Encoding': 'chunked',
                    'authorization': 'Bearer '+self.token
                }

                #
                return requests.get(dotstat_url, verify=True, headers=headers, stream=True)

        except Exception as err:
            Returned_Message = self.__ERROR  + str(err) + os.linesep
            return Returned_Message


    # Upload a file to .STAT
    def upload_file(self, transfer_url: str, file_path: Path, space: str):
        try:
            Returned_Message = ""

            if (self.token == None):
                Returned_Message = self.__ERROR  + "No token" + os.linesep
            else:
                headers = {
                    'accept': 'application/json',
                    'authorization': "Bearer "+self.token
                }

                payload = {
                    "dataspace": space,
                }

                files = {
                    'dataspace': (None, payload['dataspace']),
                    'file': (os.path.realpath(file_path), open(os.path.realpath(file_path), 'rb'), 'text/csv', '')
                }

                #
                response = requests.post(
                    transfer_url, verify=True, headers=headers, files=files)

        except Exception as err:
            Returned_Message = self.__ERROR  + str(err)
        else:
            if response.status_code != 200:
                Returned_Message = self.__ERROR  + 'Error code: ' + \
                    str(response.status_code) + ' Reason: ' + str(response.reason)
                if len(response.text) > 0:
                    Returned_Message = Returned_Message + os.linesep + 'Text: ' + response.text
            else:
                try:
                    Result = response.json()['message']
                    Returned_Message += os.linesep + Result

                    # Sleep a little bit before checking the request status
                    sleep(5)

                    # Check the request status
                    if (Result != "" and Result.find(self.__ERROR ) == -1):
                        # Extract the request ID the returned message
                        start = 'with ID'
                        end = 'was successfully'
                        requestId = Result[Result.find(
                            start)+len(start):Result.rfind(end)]
                        # This is a recursive function to check the execution status
                        Result = self.__check_request_status(
                            transfer_url, requestId, space)
                        Returned_Message = Returned_Message + os.linesep + Result

                except Exception as err:
                    if len(response.text) > 0:
                        Returned_Message = self.__ERROR  + 'Text: ' + response.text
        finally:
            return Returned_Message


    # Upload a structure to .STAT
    def upload_structure(self, transfer_url: str, file_path: Path):
        try:
            Returned_Message = ""

            # Detect the encoding used in file 
            file = open(file=file_path, mode="rb")
            detected_encoding = chardet.detect(file.read(10000))
            file.close()

            # Read file as a string "r+" with the detected encoding
            file = open(file=file_path, mode="r+", encoding=detected_encoding.get("encoding"))
            xml_data = file.read()
            file.close()

            # Make sure the encoding is "utf-8"
            tree = ET.fromstring(xml_data)
            xml_data = ET.tostring(tree, encoding="utf-8", method='xml', xml_declaration=True)

            if (self.token == None):
                Returned_Message = self.__ERROR  + "No token" + os.linesep
            else:
                headers = {
                    'Content-Type': 'application/xml',
                    'authorization': "Bearer "+self.token
                }

                #
                response = requests.post(
                    transfer_url, verify=True, headers=headers, data=xml_data)
        except Exception as err:
            Returned_Message = self.__ERROR  + str(err)
        else:
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                Returned_Message = f'Request failed with status code {response.status_code}: {e}'
            else:
                response_tree = ET.XML(response.content)
                for error_message in response_tree.findall("./{0}ErrorMessage".format(self.__NAMESPACE_MESSAGE)):
                    text_element = error_message.find("./{0}Text".format(self.__NAMESPACE_COMMON))
                    if (text_element is not None):
                        if Returned_Message == "":
                            Returned_Message = self.__UPLOAD_SUCCESS + os.linesep
                        Returned_Message = Returned_Message + text_element.text + os.linesep
        finally:
            return Returned_Message
        

    # Check request sent to .STAT status
    # This is a recursive function to check the execution status
    def __check_request_status(self, transfer_url, requestId, space):
        try:
            Returned_Message = ""

            headers = {
                'accept': 'application/json',
                'authorization': "Bearer "+self.token
            }

            payload = {
                'dataspace': space,
                'id': requestId
            }

            transfer_url = transfer_url.replace("import", "status")
            transfer_url = transfer_url.replace("sdmxFile", "request")

            response = requests.post(
                transfer_url, verify=False, headers=headers, data=payload)

        except Exception as err:
            Returned_Message = self.__ERROR  + str(err)
        else:
            if response.status_code != 200:
                Returned_Message = self.__ERROR  + 'Error code: ' + \
                    str(response.status_code) + ' Reason: ' + str(response.reason)
                if len(response.text) > 0:
                    Returned_Message = Returned_Message + os.linesep + 'Text: ' + response.text
            else:
                executionStatus = 'Execution status: ' + \
                    response.json()['executionStatus']
                if executionStatus == self.__EXECUTION_IN_PROGRESS:
                    self.__check_request_status(transfer_url, requestId, space)
                else:
                    Returned_Message = executionStatus + os.linesep + \
                        'Outcome: ' + response.json()['outcome']
                    index = 0
                    while index < len(response.json()['logs']):
                        Returned_Message = Returned_Message + os.linesep + 'Log' + \
                            str(index) + ': ' + response.json()['logs'][index]['message']
                        index += 1

        return Returned_Message
    