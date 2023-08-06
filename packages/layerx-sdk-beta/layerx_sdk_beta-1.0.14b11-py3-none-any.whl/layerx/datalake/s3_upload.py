from layerx.datalake.constants import MULTI_PART_UPLOAD_CHUNK_SIZE
from layerx.datalake.s3_interface import S3Interface


class S3Upload:

    def __init__(self, client, collection_name, upload_id, test_write_progress, add_fail_files, application_code):
        self._client = client
        self.collectionName = collection_name
        self.uploadId = upload_id
        self.write_progress = test_write_progress
        self.add_fail_files = add_fail_files
        self.application_code = application_code
        self.file_id = ""
        self.file_key = ""

    """"
    Initialize multipart upload
    """

    def initialize_multipart_upload(self, file_name: str):
        payload = {
            "fileName": file_name,
            "collectionName": self.collectionName,
            "uploadId": self.uploadId,
            "applicationCode": self.application_code
        }
        multipart_init_res = self._client.datalake_interface.get_file_id_and_key(payload)
        return multipart_init_res

    """"
    Multipart upload
    """

    def multi_part_upload(self, sub_list):

        for file in sub_list:

            '''Get file id and key'''
            multipart_init_res = self.initialize_multipart_upload(file["key"])

            if multipart_init_res["isSuccess"]:
                self.file_id = multipart_init_res["fileId"]
                self.file_key = multipart_init_res["fileKey"]
                #If isExisting is present and is true, then skip all operations to file because its already uploaded to datalake
                if "isExisting" in multipart_init_res and multipart_init_res["isExisting"]:
                    self.write_progress()
                    print(f'\nFile {self.file_key} already exists in datalake. Skipping upload')
                    continue
            else:
                file["is_all"] = True
                self.add_fail_files(file)
                continue

            pre_signed_url_pay_load = {
                "fileId": self.file_id,
                "fileKey": self.file_key,
                "parts": file["part_count"]
            }
            #print('Uploading file: ' + self.file_key + ' with ' + str(file["part_count"]) + ' parts')

            """"Get pre signed url"""
            pre_signed_url_response = self._client.datalake_interface.get_pre_signed_url(pre_signed_url_pay_load)
            url_array = []
            if pre_signed_url_response["isSuccess"]:
                if file["is_all"]:
                    if len(file["part_numbers"]) == 0:
                        url_array = pre_signed_url_response["parts"]
                    else:
                        for part_num in file["part_numbers"]:
                            index = next((index for (index, part) in enumerate(pre_signed_url_response["parts"]) if part["PartNumber"] == part_num), None)
                            url_array.append(pre_signed_url_response["parts"][index])
            else:
                file["is_all"] = True
                self.add_fail_files(file)
                continue

            # is_upload_success = True
            # part_index = 0
            uploaded_parts_arr = []
            for part in url_array:

                s3_interface = S3Interface()

                """"Upload s3 file"""
                next_byte = MULTI_PART_UPLOAD_CHUNK_SIZE * (part["PartNumber"] - 1)
                #Count of bytes to read for each chunck, in case of last part, read only remaining bytes
                max_read_count = MULTI_PART_UPLOAD_CHUNK_SIZE if (part["PartNumber"] - 1) < file["part_count"] - 1 else file["size"] - next_byte
                upload_s3_response = s3_interface.upload_to_s3(part["signedUrl"], file["path"], next_byte, max_read_count)

                if not upload_s3_response["isSuccess"]:
                    file["is_all"] = True
                    self.add_fail_files(file, part["PartNumber"])
                    # is_upload_success = False
                    # break
                    print(f'part number: {part["PartNumber"]} failed')
                else:
                    print(f'part number: {part["PartNumber"]} success')
                
                uploaded_parts_arr.append({
                    "PartNumber": part["PartNumber"],
                    "ETag": upload_s3_response["e_tag"]
                })
                
            # if not is_upload_success:
            #     self.add_fail_files(file["key"])
            #     #print('Failed to upload file: ' + file["key"])
            #     continue

            """"Finalize multipart upload"""
            finalize_payload = {
                "fileId": self.file_id,
                "fileKey": self.file_key,
                "parts": uploaded_parts_arr,
                "uploadId": self.uploadId
            }

            finalize_re = self._client.datalake_interface.finalize_upload(finalize_payload)

            if finalize_re["isSuccess"]:
                self.write_progress()
                print(f'\nFile {self.file_key} successfully uploaded to datalake')
            else:
                print('Failed to finalize upload file: ' + file["key"])
                file["is_all"] = False
                self.add_fail_files(file)
