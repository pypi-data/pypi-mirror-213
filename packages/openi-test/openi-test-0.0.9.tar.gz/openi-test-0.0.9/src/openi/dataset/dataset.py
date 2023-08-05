import os
import math
import emoji
import requests
import hashlib
from tqdm import tqdm
from collections import OrderedDict
from datetime import datetime

class DatasetUploadFile:
    """
    Build APIs calls for uploading a file to openi platform.
    This class will start upload process immediatelly once being initialized. 
    """
    def __init__(self, file, username, repository, token, cluster="NPU", app_url="https://openi.pcl.ac.cn/api/v1/"):
        """
        Args:
            file:       必填，文件路径(包含文件名)
            username:   必填，数据集所属项目用户名
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
        self.max_chunk_size = 67108864
        if cluster == "NPU":
            self.upload_type = 1
        else:
            self.upload_type = 0
        self.filename = self.filepath.split("/")[-1]
        self.size = os.path.getsize(self.filepath)
        self.chunks = dict()
        self.upload_url = dict()

    """
    APIs impleamentation
    """
    def getChunks(self):
        params = {
            "access_token":self.token,
            "dataset_id":self.dataset_id,
            "md5":self.md5,
            "file_name":self.filename,
            "type":self.upload_type,
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
            raise ConnectionRefusedError(f'{emoji.emojize(":cross_mark:")} <{x.status_code} {x.reason}> {x.text}')

    def getDatasetID(self):
        params = {"access_token": self.token}
        x = requests.get('{}datasets/{}/{}/'.format(self.app_url, self.username, self.repo), params=params)
        if x.status_code == 200:
            try:
                self.dataset_id = x.json()["data"][0]["id"]
            except:
                print(f'{emoji.emojize(":cross_mark:")} repo [{self.username}/{self.repo}]: dataset does not exist, please create dataset before uploading files.')
        else:
            raise ConnectionRefusedError(f'{emoji.emojize(":cross_mark:")} <{x.status_code} {x.reason}> {x.text}')

    def newMultipart(self):
        params = {
            "access_token":self.token,
            "dataset_id":self.dataset_id,
            "md5":self.md5,
            "file_name":self.filename,
            "type":self.upload_type,
            "totalChunkCounts":self.total_chunk_counts,
            "size":self.size
        }
        x = requests.get('{}attachments/new_multipart'.format(self.app_url), params=params)
        if x.json()["result_code"] == "0": 
            self.upload_id = x.json()["uploadID"]
            self.uuid = x.json()["uuid"]
        else:
            raise ConnectionRefusedError(f'{emoji.emojize(":cross_mark:")} <{x.status_code} {x.reason}> {x.json()["msg"]}')
        
    def getMultipartURL(self, chunk_number,chunk_size):
        params = {
            "access_token":self.token,
            "dataset_id":self.dataset_id,
            "file_name":self.filename,
            "type":self.upload_type,
            "chunkNumber":chunk_number,
            "size":chunk_size,
            "uploadID":self.upload_id,
            "uuid":self.uuid
        }
        x = requests.get('{}attachments/get_multipart_url'.format(self.app_url), params=params)
        if x.status_code == 200:
            self.upload_url[chunk_number] = x.json()["url"]
        else:
            raise ConnectionRefusedError(f'{emoji.emojize(":cross_mark:")} <{x.status_code} {x.reason}> {x.text}')
    
    def putUpload(self,chunk_number,start,chunk_size):
        headers = {"Content-Type": "text/plain"} if self.upload_type == 0 else {}
        file_chunk_data = None
        with open(self.filepath, 'rb') as f:
                f.seek(start)
                file_chunk_data = f.read(chunk_size)
        x = requests.put(self.upload_url[chunk_number], data=file_chunk_data, headers=headers)
        if x.status_code != 200:
            raise ConnectionRefusedError(f'{emoji.emojize(":cross_mark:")} <{x.status_code} {x.reason}> "upload chunk [{chunk_number}] failed."')  

    def completeMultipart(self):
        params = {
            "access_token":self.token,
            "dataset_id":self.dataset_id,
            "file_name":self.filename,
            "type":self.upload_type,
            "size":self.size,
            "uploadID":self.upload_id,
            "uuid":self.uuid
        }
        x = requests.post('{}attachments/complete_multipart'.format(self.app_url), params=params)
        if x.status_code != 200:
            raise ConnectionRefusedError(f'{emoji.emojize(":cross_mark:")} <{x.status_code} {x.reason}> {x.text}')
        if x.json()["result_code"] == "-1":
            raise ConnectionRefusedError(f'{emoji.emojize(":cross_mark:")} <{x.status_code} {x.reason}> {x.json()["msg"]}')


    """
    utils functions
    """
    def logging(self,message):
        asctime = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        print(f'{asctime} [{self.filename}-{self.cluster}]: {message}')

    def filePreprocess(self):
        # suffix1 = self.filename.split(".")[-1]
        # suffix2 = '.'.join(self.filename.split(".")[-2:])
        # if suffix1 != "zip" and suffix2 != "tar.gz":
        #     raise ValueError(f'{emoji.emojize(":cross_mark:")} [{self.filename}] File type is not zip or tar.gz')
        if self.size == 0:
            raise ValueError(f'{emoji.emojize(":cross_mark:")} [{self.filename}] File size is 0')
        if self.size > int(200**10): # 200GB
            raise ValueError(f'{emoji.emojize(":cross_mark:")} [{self.filename}] File size exceeds 200GB')

        if self.size > self.max_chunk_size:
            self.total_chunk_counts = math.ceil(self.size / self.max_chunk_size) 
        else:
            self.total_chunk_counts = 1

        for n in range(1, self.total_chunk_counts + 1):
            start = (n-1) * self.max_chunk_size
            end = self.size if n == self.total_chunk_counts else n * self.max_chunk_size
            self.chunks[n] = (start,end)
        
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
    def uploadProgressBar(self,chunks):
        u = len(self.chunks) - len(chunks)
        with tqdm(total= self.size, desc='Uploading', leave=True, unit='B', unit_scale=True, unit_divisor=1000)  as pbar:
            # checkpoint
            if u != 0: pbar.update(self.max_chunk_size * u)     

            # upload chunks
            for n, v in chunks.items():
                chunk_size = v[1] - v[0]
                self.getMultipartURL(n,chunk_size)
                #logging.info(f"[{self.filename}]: [CHUNK {n}] chunk index: {v[0]} to {v[1]}")

                # small file only 1 chunk
                if self.total_chunk_counts == 1:
                    self.putUpload(n,v[0],chunk_size)
                    pbar.update(chunk_size)

                # large file, divide into 10 pieces for each chunk for more acurrate progress bar
                else:
                    num_pieces = 10
                    piece_volume_mb = chunk_size // num_pieces  # Volume of each regular piece
                    extra_volume_mb = chunk_size % num_pieces  # Extra volume for the last piece
                    start_index = v[0]
                    for i in range(num_pieces):
                        if i == num_pieces - 1:  # Last piece
                            piece_volume_mb += extra_volume_mb
                        self.putUpload(n,start_index,piece_volume_mb)
                        start_index += piece_volume_mb
                        pbar.update(piece_volume_mb)
                        #logging.info(f"\t[{self.filename}]: [piece {i}] piece index: {start_index - piece_volume_mb} to {start_index}, volume: {piece_volume_mb}")

    def uploadMain(self):

        self.logging(f'{emoji.emojize(":light_bulb:")} dataset file processing & checking...')
        # preprocess
        self.filePreprocess()    
        # checking upload status
        self.getChunks()

        # upload starts
        if self.uuid != '':
            if self.uploaded:
                raise ValueError(f'{emoji.emojize(":cross_mark:")} Upload failed: [{self.filename} - {self.cluster}], already exists, cannot be uploaded again.')
            else:
                self.logging(f'{emoji.emojize(":light_bulb:")} continue upload...')
                uploaded_chunks = [int(i.split('-')[0]) for i in self.uploaded_chunks.split(',') if i != '']
                continue_chunks = { i:self.chunks[i] for i in self.chunks if i not in uploaded_chunks}
                # re-upload last chunk from checkpoint
                if uploaded_chunks != []:
                    last_chunk_index = max(uploaded_chunks)
                    continue_chunks[last_chunk_index] = self.chunks[last_chunk_index]
                continue_chunks =  OrderedDict(sorted(continue_chunks.items()))
                self.uploadProgressBar(continue_chunks)

        else:
            self.logging(f'{emoji.emojize(":light_bulb:")} start new upload...')
            self.newMultipart()
            self.uploadProgressBar(self.chunks)

        self.completeMultipart()        
        url = f"{self.app_url.split('api')[0]}{self.username}/{self.repo}/datasets"
        self.logging(f'{emoji.emojize(":party_popper:")} Successfully uploaded, view on link: {url}')

def upload_file(file, username, repository, token, cluster="", app_url=""):
    d = DatasetUploadFile(
        file = file, 
        username = username, 
        repository = repository, 
        token = token, 
        cluster = cluster, 
        app_url = app_url)
    d.uploadMain()