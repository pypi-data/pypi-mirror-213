import os
import sys
import threading
import time
import copy
from multiprocessing.pool import ThreadPool

from layerx.datalake.constants import MAX_UPLOAD_RETRY_COUNT, MediaType, FILE_UPLOAD_THREADS, SUB_FILE_LENGTH, MULTI_PART_UPLOAD_CHUNK_SIZE
from layerx.datalake.s3_upload import S3Upload

imageExtensionList = ['jpg', 'jpeg', 'png']
videoExtensionList = ['mp4', 'mkv']


class FileUpload:
    def __init__(self, client: "DatalakeClient", application_code = None):
        self._client = client
        self.folder_upload = True
        self.path = ""
        self.upload_type = ""
        self.payload = ''
        self.objectKeyList = []
        self.file_list = []
        self.uploadId = ""
        self.collectionName = ''
        self.collectionId = ""
        self.key_name_array = []
        #Set of failed upload files as key-value map of file name - path
        self.fail_upload_set = []
        self.folder_path = ""
        self.total_keys = 0
        self.progress = 0
        self.count = 0
        self.failed_upload_count = 0
        self.application_code = application_code
        self.count_lock = threading.Lock()

    '''
    Split object key list
    '''

    def split_object_key_list(self, input_list, sub_size):
        sub_list = [input_list[i:i + sub_size] for i in range(0, len(self.key_name_array), sub_size)]
        return sub_list

    ''''
    Check media type
    '''

    def check_media_type(self, extension):
        #Convert extension to lower case for case insensitive comparison
        extension = extension.lower()
        if self.upload_type == MediaType.IMAGE.value and extension in imageExtensionList:
            return True
        elif self.upload_type == MediaType.VIDEO.value and extension in videoExtensionList:
            return True
        elif self.upload_type == MediaType.OTHER.value:
            return True
        else:
            return False

    ''''
    Get media file list
    '''

    def get_media_files_list(self):
        dir_list = []

        if self.folder_upload:
            dir_list = os.listdir(self.path)
            self.folder_path = self.path
        else:
            path_array = self.path.split("/")
            dir_list.append(path_array[-1])
            path_array.pop()

            index = 0
            for path_component in path_array:
                if index != 0:
                    self.folder_path += "/"

                self.folder_path += path_component

                index += 1

        # Filter according to upload type
        for file_name in dir_list:
            extension = file_name.split(".")[-1]

            if self.check_media_type(extension):
                #Get file size in bytes
                file_full_path = self.folder_path + "/" + file_name
                file_size = os.path.getsize(file_full_path)
                #Determine multi - part upload chunk count - take ceiling of file size / chunk size
                chunk_count = int(file_size / MULTI_PART_UPLOAD_CHUNK_SIZE) + 1
                self.objectKeyList.append(file_name)
                self.file_list.append(file_name)
                self.key_name_array.append({
                    "key": file_name,
                    "path": file_full_path,
                    "part_count": chunk_count,
                    "size": file_size,
                    "is_all": True,
                    "part_numbers": []
                })
                #print("File name: " + file_name + " File size: " + str(file_size) + " Chunk count: " + str(chunk_count))
        self.total_keys = len(self.key_name_array)

    '''
    Write progress
    '''

    def write_progress(self, count=True):
        if count:
            self.count_lock.acquire()
            try:
                self.count += 1
                self.progress = 100 * (self.count / self.total_keys)
                sys.stdout.write(
                    "\r" + "upload files: " + str(self.count) + f"/{self.total_keys}" + "     " + "progress: " +
                    str(round(self.progress, 2)) + " %")
                sys.stdout.flush()
            finally:
                self.count_lock.release()
        else:
            sys.stdout.write(
                "\r" + "upload files: " + str(self.count) + "     " + "progress: " +
                str(round(self.progress, 2)) + " %")
            sys.stdout.flush()

    ''''
    Add upload failed files into an array
    '''

    def add_fail_files(self, file, part_number = None):
        self.count_lock.acquire()
        try:

            index = next((index for (index, _file) in enumerate(self.fail_upload_set) if _file["key"] == file["key"]), None)

            if(index != -1):
                if(part_number != None):
                    self.fail_upload_set[index]["part_numbers"].append(part_number)
            else:
                # file_name = object_key.split("/")[-1]
                self.fail_upload_set[index]["part_numbers"] = []
                if(part_number != None):
                    self.fail_upload_set[index]["part_numbers"].append(part_number)
                self.fail_upload_set.append(file)
            #Set failed count from the key count of fail_upload_set
            self.failed_upload_count = len(self.fail_upload_set)
        finally:
            self.count_lock.release()

    ''''
    Parallel upload
    '''

    def parallel_upload(self, sublist):
        _upload = S3Upload(self._client, self.collectionName, self.uploadId, self.write_progress, self.add_fail_files, self.application_code)
        _upload.multi_part_upload(sublist)

    ''''
    File upload initiate     
    '''

    def file_upload_initiate(self, path, collection_type, collection_name, meta_data_object, meta_data_override):
       
        self.write_progress(False)

        self.path = path
        self.payload = {
            "collectionType": collection_type,
            "collectionName": collection_name,
            "metaDataObject": meta_data_object,
            "isOverrideMetaData": meta_data_override,
        }
        self.upload_type = collection_type
        self.collectionName = collection_name

        if not os.path.exists(self.path):
            raise Exception("Path does not exists")
        elif os.path.isdir(path):
            self.folder_upload = True
        elif os.path.isfile(path):
            self.folder_upload = False

        """ Get media file list"""
        self.get_media_files_list()
        self.payload["objectKeyList"] = self.objectKeyList

        """Upload metadata in collection"""
        upload_metadata_response = self._client.datalake_interface.upload_metadata_collection(self.payload)

        if not upload_metadata_response["isSuccess"]:
            msg = upload_metadata_response["message"]
            raise Exception("Can not upload meta data | " + msg )

        self.uploadId = upload_metadata_response["uploadId"]
        self.collectionId = upload_metadata_response["collectionId"]

        sub_list = self.split_object_key_list(self.key_name_array, SUB_FILE_LENGTH)

        process = ThreadPool(FILE_UPLOAD_THREADS)
        process.map(self.parallel_upload, sub_list)
        process.close()
        process.join()

        print(f"\n\nUpload failed count/total : {self.failed_upload_count}/{self.total_keys}")  
        retry_count = 0

        while self.failed_upload_count > 0 and retry_count < MAX_UPLOAD_RETRY_COUNT:
            print(f'Retrying {self.failed_upload_count} failed uploads.....')
            time.sleep(30)
            #Retry with half no of threads
            #Copy failed set to temp array and reset original
            temp_failed_arr = []
            for file in self.fail_upload_set:
                temp_failed_arr.append(file)
            #fail_sub_list = self.split_object_key_list(temp_failed_arr, SUB_FILE_LENGTH)
            self.fail_upload_set = []
            retry_count += 1
            print('Retry count: ' + str(retry_count) + ' of ' + str(MAX_UPLOAD_RETRY_COUNT)) 
            self.parallel_upload(temp_failed_arr)
            time.sleep(1)

        print('Finished processing failed uploads')
        #if self.progress != 0:
        complete_res = self._client.datalake_interface.complete_collection_upload(self.uploadId)
        if complete_res["isSuccess"]:
            print("\nComplete upload")
        else:
            print("\nError In complete upload")

        if len(self.fail_upload_set) != 0:
            print(f"\n\nupload failed files: {self.failed_upload_count}/{self.total_keys}")
            for file_name in self.fail_upload_set:
                print(f'{file_name["key"]}')
        
        return {
            "is_success": complete_res["isSuccess"],
            "job_id": upload_metadata_response["jobId"],
            "collection_id": self.collectionId
        }

    def get_upload_status(self, collection_name):
        if(collection_name == None):
            print('Invalid collection name')
        else:
            progress_response = self._client.datalake_interface.get_upload_status(collection_name)
            return progress_response