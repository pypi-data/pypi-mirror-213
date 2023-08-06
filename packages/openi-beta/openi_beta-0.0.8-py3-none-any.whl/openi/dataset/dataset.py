import os
import math
import requests
import hashlib
from tqdm import tqdm
from collections import OrderedDict
from datetime import datetime
from ..constants import *

import logging

LOG_FORMAT = "%(asctime)s [%(levelname)s] - %(funcName)s() %(lineno)d: %(message)s"
DATE_FORMAT = "%Y/%m/%d %H:%M:%S"
logging.basicConfig(filename='openi.log', level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)


class DatasetUploadFile:
    """
    Build APIs calls for uploading a file to openi platform.
    This class will start upload process immediatelly once being initialized. 
    """

    def __init__(self, file, username, repository, token, cluster, app_url):
        """
        Args:
            file:       必填，文件路径(包含文件名)
            username:   必填，数据集所属项目的owner用户名
            repository: 必填，数据集所属项目名
            token:      必填，用户启智上获取的令牌token，并对该项目数据集有权限
            
            cluster:    选填，可填入GPU或NPU，不填写后台默认为NPU
            app_url:    选填, 默认为平台地址，开发测试用
        """
        self.filepath = file
        self.username = username
        self.repo = repository
        self.token = token
        self.cluster = cluster
        self.app_url = app_url

        # preset variables
        # self.max_chunk_size = MAX_CHUNK_SIZE
        if cluster == "NPU":
            self.upload_type = 1
        elif cluster == "GPU":
            self.upload_type = 0
        else:
            raise ValueError(
                f"❌ please enter a valid cluster name, 'GPU' or 'NPU'")

        if "\\" in self.filepath:
            self.filename = self.filepath.split("\\")[-1]
        else:
            self.filename = self.filepath.split("/")[-1]

        self.size = os.path.getsize(self.filepath)
        self.upload_url = dict()

    """
    APIs implementation
    """

    def getChunks(self):
        params = {
            "access_token": self.token,
            "dataset_id": self.dataset_id,
            "md5": self.md5,
            "file_name": self.filename,
            "type": self.upload_type,
        }
        x = requests.get('{}attachments/get_chunks'.format(self.app_url), params=params)
        if x.status_code == 200:
            self.upload_id = x.json()["uploadID"]
            self.uuid = x.json()["uuid"]
            self.uploaded_chunks = x.json()["chunks"]
            if x.json()["uploaded"] == '1':
                self.uploaded = True
            else:
                self.uploaded = False
        else:
            raise ConnectionRefusedError(
                f'❌ <{x.status_code} {x.reason}> {x.text}')

    def getDatasetID(self):
        params = {"access_token": self.token}
        x = requests.get('{}datasets/{}/{}/'.format(self.app_url, self.username, self.repo), params=params)
        if x.status_code == 200:
            try:
                self.dataset_id = x.json()["data"][0]["id"]
            except:
                print(
                    f'❌ repo [{self.username}/{self.repo}]: dataset does not exist, please create dataset before uploading files.')
        else:
            raise ConnectionRefusedError(
                f'❌ <{x.status_code} {x.reason}> {x.text}')

    def newMultipart(self):
        params = {
            "access_token": self.token,
            "dataset_id": self.dataset_id,
            "md5": self.md5,
            "file_name": self.filename,
            "type": self.upload_type,
            "totalChunkCounts": self.total_chunk_counts,
            "size": self.size
        }
        x = requests.get('{}attachments/new_multipart'.format(self.app_url), params=params)
        if x.json()["result_code"] == "0":
            self.upload_id = x.json()["uploadID"]
            self.uuid = x.json()["uuid"]
        else:
            raise ConnectionRefusedError(
                f'❌ <{x.status_code} {x.reason}> {x.json()["msg"]}')

    def getMultipartURL(self, chunk_number, chunk_size):
        params = {
            "access_token": self.token,
            "dataset_id": self.dataset_id,
            "file_name": self.filename,
            "type": self.upload_type,
            "chunkNumber": chunk_number,
            "size": chunk_size,
            "uploadID": self.upload_id,
            "uuid": self.uuid
        }
        x = requests.get('{}attachments/get_multipart_url'.format(self.app_url), params=params)
        if x.status_code == 200:
            self.upload_url[chunk_number] = x.json()["url"]
        else:
            raise ConnectionRefusedError(
                f'❌ <{x.status_code} {x.reason}> {x.text}')

    def putUpload(self, chunk_number, start, chunk_size):
        headers = {"Content-Type": "text/plain"} if self.upload_type == 0 else {}
        file_chunk_data = None
        with open(self.filepath, 'rb') as f:
            f.seek(start)
            file_chunk_data = f.read(chunk_size)
        x = requests.put(self.upload_url[chunk_number], data=file_chunk_data, headers=headers)
        if x.status_code != 200:
            raise ConnectionRefusedError(
                f'❌ <{x.status_code} {x.reason}> "upload chunk [{chunk_number}] failed."')

    def completeMultipart(self):
        params = {
            "access_token": self.token,
            "dataset_id": self.dataset_id,
            "file_name": self.filename,
            "type": self.upload_type,
            "size": self.size,
            "uploadID": self.upload_id,
            "uuid": self.uuid
        }
        x = requests.post('{}attachments/complete_multipart'.format(self.app_url), params=params)
        if x.status_code != 200:
            raise ConnectionRefusedError(
                f'❌ <{x.status_code} {x.reason}> {x.text}')
        if x.json()["result_code"] == "-1":
            raise ConnectionRefusedError(
                f'❌ <{x.status_code} {x.reason}> {x.json()["msg"]}')

    """
    utils functions
    """

    def stdOut(self, message=""):
        asctime = datetime.now().strftime("%H:%M:%S")
        return (f'{asctime}|{self.filename}|{self.cluster}|{message}')

    def filePreprocess(self):
        if self.size == 0:
            raise ValueError(
                f'❌ [{self.filename}] File size is 0')
        if self.size > MAX_FILE_SIZE:
            raise ValueError(
                f'❌ [{self.filename}] File size exceeds 200GB')

        chunk_size = SMALL_FILE_CHUNK_SIZE if self.size < SMALL_FILE_SIZE else LARGE_FILE_CHUNK_SIZE
        self.total_chunk_counts = math.ceil(self.size / chunk_size)
        self.chunks = {n: (n - 1) * chunk_size for n in range(1, self.total_chunk_counts + 1)}

        self.calculateMD5()
        self.getDatasetID()

    def calculateMD5(self):
        with open(self.filepath, 'rb') as f:
            data = f.read()
        self.md5 = hashlib.md5(data).hexdigest()

    """
    Main functions
    uploadProgressBar(): upload file with progress bar.
    uploadMain(): control flow function.
    """

    def uploadProgressBar(self, chunks):
        u = self.total_chunk_counts - len(chunks)

        bar_format = '{desc}{percentage:3.0f}%|{bar}{r_bar}'
        with tqdm(total=self.size, leave=True, unit='B', unit_scale=True, unit_divisor=1000, desc=self.stdOut(),
                  bar_format=bar_format) as pbar:
            chunk_size = SMALL_FILE_CHUNK_SIZE if self.size < SMALL_FILE_SIZE else LARGE_FILE_CHUNK_SIZE

            # checkpoint
            if u != 0:
                pbar.update(chunk_size * u)

            # upload chunks
            for n, v in chunks.items():
                chunk_size = min(self.size - v, self.size, chunk_size)
                self.getMultipartURL(n, chunk_size)
                self.putUpload(n, v, chunk_size)
                pbar.update(chunk_size)
                logging.info(f"[{self.filename}]: chunk {n} to {n + chunk_size}")

    def uploadMain(self):

        print(self.stdOut('dataset file processing & checking...'))
        # preprocess
        self.filePreprocess()
        # checking upload status
        self.getChunks()

        # upload starts
        if self.uuid != '':
            if self.uploaded:
                raise ValueError(
                    f'❌ Upload failed: [{self.filename} - {self.cluster}], already exists, cannot be uploaded again.')
            else:
                print(self.stdOut('continue upload...'))
                uploaded_chunks = [int(i.split('-')[0]) for i in self.uploaded_chunks.split(',') if i != '']
                continue_chunks = {i: self.chunks[i] for i in self.chunks if i not in uploaded_chunks}
                # re-upload last chunk from checkpoint
                if uploaded_chunks:
                    last_chunk_index = max(uploaded_chunks)
                    continue_chunks[last_chunk_index] = self.chunks[last_chunk_index]
                continue_chunks = OrderedDict(sorted(continue_chunks.items()))
                self.uploadProgressBar(continue_chunks)

        else:
            print(self.stdOut('start new upload...'))
            self.newMultipart()
            self.uploadProgressBar(self.chunks)

        self.completeMultipart()
        url = f"{self.app_url.split('api')[0]}{self.username}/{self.repo}/datasets"
        print(self.stdOut(f'🎉 Successfully uploaded, view on link: {url}'))


def upload_file(file, username, repository, token, cluster="NPU", app_url=APP_URL):
    d = DatasetUploadFile(
        file=file,
        username=username,
        repository=repository,
        token=token,
        cluster=cluster,
        app_url=app_url)
    d.uploadMain()
