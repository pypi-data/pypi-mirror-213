# -*- coding:utf-8 -*-
import requests
import json
import os
import logging
import hashlib
from urllib import parse
from datetime import datetime
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from qcloud_cos import CosServiceError
from qcloud_cos.cos_threadpool import SimpleThreadPool
# from qcloud_cos import CosClientError
# from sts.sts import Sts
import sys
# import json

# 正常情况日志级别使用 INFO，需要定位时可以修改为 DEBUG，此时 SDK 会打印和服务端的通信信息
logging.basicConfig(level=logging.INFO, stream=sys.stdout)


def requests_post(url, payload, append_header=None):
    # logging.debug(f"####requests_post url {url}")
    # logging.info(f"#### requests_post payload: {payload}")
    headers = {"content-type": "application/json", "Accept": "*/*"}
    if append_header:
        headers = dict(headers, **append_header)
    logging.debug(f"####requests_post headers: {headers}")
    res = requests.post(url, data=json.dumps(payload), headers=headers)
    return res


def requests_get(url, params, append_header=None):
    headers = {"content-type": "application/json", "Accept": "*/*"}
    if append_header:
        headers = dict(headers, **append_header)
    res = requests.get(url, params=params, headers=headers)
    return res


class DataTool:
    """
    获取停车场信息；
    上传停车场信息；
    获取停车场采集记录信息；
    上传停车场采集记录信息；
    """
    def __init__(self, name, code, host="http://127.0.0.1:8000/"):
        now = datetime.now().strftime("%m-%d-%Y:%H-%M-%S")
        self._log_file_name = f"./walk_{now}.log.txt"
        self.name = name               # 用户name
        self.code = code               # 用户code
        # self.uid = None                # 用户ID
        self.authorization = None
        # self.temp_carparking_name = "carparking_name"
        # self.temp_unique_time_string = "unique_time_string"
        self.host = host               # api Domain

        # assert self.temp_carparking_name, "请携带正确的停车场名称"
        # assert self.host, "请携带api host"

        self.car_parking_serial_id_url = parse.urljoin(self.host, "ods/car_parking_serial_id_handler/")
        self.collection_record_serial_id_url = parse.urljoin(self.host, "ods/collection_record_serial_id_handler/")
        self.check_code_url = parse.urljoin(self.host, "ods/check_code/")
        self.usercenter_token_url = parse.urljoin(self.host, "api/v1/usercenter/token/")
        self.update_code_url = parse.urljoin(self.host, "ods/update_code/")
        self.upload_video_analysis_record_url = parse.urljoin(self.host, "ods/video_analysis_record_handler/")
        self.collection_data_upload_url = parse.urljoin(self.host, "api/v1/ods/collection_data_upload/")
        self.frame_data_upload_url = parse.urljoin(self.host, "api/v1/ods/frame_data_upload/")
        self.annotation_data_upload_url = parse.urljoin(self.host, "api/v1/ods/annotation_data_upload/")
        self.car_parking_serial_id = None
        self.collection_record_serial_id = None

        self.qcloud_sts_url = parse.urljoin(self.host, "api/v1/cloud_sts/qcloud_sts/")
        # self.check_code()              # 用户校验
        self.check_set_token()           # 设置token
        # headers = {"Authorization":"bearer a809655f-e4bf-41b8-9088-85a1d3780d6d"}
        self.car_p_ser_path = {}
        self.error_car_p_ser_path = {}

    def check_set_token(self):
        res = requests_post(self.usercenter_token_url, {"username": self.name, "password": self.code})
        # {
        #     "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4MTk4OTkzMiwiaWF0IjoxNjgxOTAzNTMyLCJqdGkiOiI3ZWNlZmRjZGE4Y2Q0ZmFlYjhkZDRlNzVhZDRhNWNkNSIsInVzZXJfaWQiOjEwfQ.MtZ_vdnjTyVXaqqvFsvuyRjG4eUkZ20noyULz9znRHw",
        #     "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjgxOTA1MzMyLCJpYXQiOjE2ODE5MDM1MzIsImp0aSI6ImVkY2NiMzljODMxNDRhYzBhMmVmMDU0NGY0YmI4NDRmIiwidXNlcl9pZCI6MTB9.F6JH8JAHsuua0pR8kC7U6OjdUtzEIxggadDoaOW_HdM"
        # }
        logging.info(f"url: {self.usercenter_token_url}")
        logging.info(f"res: {res.status_code}")
        assert res.status_code == 200, f"请求有错, errmsg【{res.reason}】"
        json_data = json.loads(res.text)
        # assert json_data['code'] == 2000, f"请求有错, errmsg【{json_data['msg']}】"
        self.authorization = f"Bearer {json_data['access']}"
        return json_data

    def get_tmp_qcloud_id_key(self, target_file_path_key, md5):
        '''
        {
            "code": 2000,
            "data": {
                "expiredTime": 1681961930,
                "expiration": "2023-04-20T03:38:50Z",
                "credentials": {
                    "sessionToken": "iKuSbId56s5hP2x1B0SZC7d7anRhFy4a824add8464e17a1d156d2db539b3f69eVzUqbzXDkqiM5dNdJFFSdQfO5cgefEEPRBUgWv7-GTZqNAactSuFvHY6Vy_0Xw1DdSzOZ1KaSKw1wXtBZNCzghC057P7QL4eogSxfsPR10_sJE-Z9WnUuS0AULk0A_lrOYh6zIKzal9y0s9Eet0RRRhawbLx7M2jUmyTLkSav559bLWdToSq0mUEi_Z66hn7kk5sEbHZmdeujV_ZDSrd91UqyEM-hToAqsizkBflJal4-d1YcScY9Vpy-AJEJnkhdL3JJFi_qyGDb7xwXge-23g4o6cYteSPHGnL0Ra68--ZavXtrjU6b9ucoLBiv8aJQNNwZ6X_CIq8eA1NrU09A6hWnKija3VRksikHgnAZa7zYznMD6cfy_mWVQoj39hidOquEErGyhkX4xIF3MkgsTSH9ZWNDEpr4JnYGxsuidMqJUSUG79uVWZJnlpnK33ucGtV5xJ-mqsMp9-KN8CT01g9rojO2fVegnikgo2j-uUB0rD_bXgLX2cOUhun3e9-tttSsIpvaQlfaRP8hZk5uD0uhpj1xFLqPu5PP9aQQr8hM2RzQzE8_1v04ZyewGypnApRk4SZJkuxHvIBPQSfAQskf54o8PIxVa9YSziVnoLffR3V5fZx66mQhhqKOFuZmBbdgYYJMxmxt_6Dv2xShsx26Q7PEidFWg9JrVEOskE3VXdcWr5dx8L7b2ZMSC8TClphMAtO_w9V3zCqPzHeHHat6pZMGIMCgdqdiiNd2eE",
                    "tmpSecretId": "AKIDYGAaKYeYcUjE_GKHzm0c0s3sLTRhLzBDryfUf_ulMWat1JP397wsKdv1U18sIsXl",
                    "tmpSecretKey": "fKeBVPycknYCjENB890Jlu0UtcB7GQC6C64LqSO/h2c="
                },
                "requestId": "6b9d4fa2-3c93-4961-9eb6-8c29ef96ad5d",
                "startTime": 1681960130
            },
            "msg": ""
        }
        '''
        if not self.authorization:
            self.check_set_token()
        request_payload = {"cloud_type": "qcloud", "target_file_path_key": target_file_path_key, "md5": md5}
        res = requests_post(self.qcloud_sts_url, request_payload, {"Authorization": self.authorization})
        if res.status_code != 200:
            self.check_set_token()
            res = requests_post(self.qcloud_sts_url, request_payload, {"Authorization": self.authorization})
        assert res.status_code == 200, f"请求有错, errmsg【{res.reason}】"
        json_data = json.loads(res.text)
        logging.debug(f"#### get_tmp_qcloud_id_key: {json_data}")
        assert json_data['code'] == 2000, f"请求有错, errmsg【{json_data['msg']}】"
        return json_data['data']

    def check_code(self):
        # 用户校验
        res = requests_post(self.check_code_url, {"name": self.name, "code": self.code})
        assert res.status_code == 200, f"请求有错, errmsg【{res.reason}】"
        json_data = json.loads(res.text)
        assert json_data['code'] == 2000, f"请求有错, errmsg【{json_data['msg']}】"
        # self.uid = json_data['data']['uid']
        return json_data['data']

    def update_code(self, new_code):
        # 用户更新code
        assert 4 <= len(new_code) <= 10, "请输入长度为4~10的新code"
        res = requests_post(self.update_code_url, {"name": self.name, "code": self.code, "new_code": new_code})
        assert res.status_code == 200, f"请求有错, errmsg【{res.reason}】"
        json_data = json.loads(res.text)
        # self.uid = json_data['data']['uid']
        return json_data['data']

    def upload_car_parking_info(self, carparking_name, city="城市", district="区", address="地址", update=False):
        carparking_name = carparking_name.strip()
        if not carparking_name.endswith("停车场"):
            carparking_name = carparking_name + "停车场"
        res = requests_post(self.car_parking_serial_id_url, {
            "carparking_name": carparking_name,
            "city": city,
            "district": district,
            "address": address,
            "update": update,
            # "uid": self.uid
        }, {"Authorization": self.authorization})
        assert res.status_code == 200, f"请求有错, errmsg【{res.reason}】"
        json_data = json.loads(res.text)
        return json_data

    def get_car_parking_info(self, carparking_name):
        carparking_name = carparking_name.strip()
        if not carparking_name.endswith("停车场"):
            carparking_name = carparking_name + "停车场"
        res = requests_get(self.car_parking_serial_id_url, {"carparking_name": carparking_name}, {"Authorization": self.authorization})
        assert res.status_code == 200, f"请求有错, errmsg【{res.reason}】"
        json_data = json.loads(res.text)
        return json_data

    def upload_carparking_collection_record_info(self, carparking_serial, unique_time_string, other_data={}):
        payload = {
            "carparking_serial": carparking_serial,
            "unique_time_string": unique_time_string,
            # "uid": self.uid
        }
        payload.update(other_data)
        res = requests_post(self.collection_record_serial_id_url, payload, {"Authorization": self.authorization})
        assert res.status_code == 200, f"请求有错, errmsg【{res.reason}】"
        json_data = json.loads(res.text)
        return json_data

    def get_carparking_collection_record_info(self, carparking_serial, unique_time_string):
        res = requests_get(self.collection_record_serial_id_url, {
            "carparking_serial": carparking_serial,
            "unique_time_string": unique_time_string,
            # "uid": self.uid
        }, {"Authorization": self.authorization})
        json_data = json.loads(res.text)
        return json_data

    def upload_video_analysis_record(self, carparking_serial, collection_record_serial, person_name, analysis_date, analysis_result, model_version="", remark=""):
        payload = {
            "carparking_serial": carparking_serial,
            "collection_record_serial": collection_record_serial,
            "person_name": person_name,
            "model_version": model_version,
            "analysis_date": analysis_date,
            "analysis_result": analysis_result,
            "remark": remark,
        }
        res = requests_post(self.upload_video_analysis_record_url, payload, {"Authorization": self.authorization})
        assert res.status_code == 200, f"请求有错, errmsg【{res.reason}】"
        json_data = json.loads(res.text)
        return json_data

    def set_car_p_ser_handle_path(self, car_p_encoding, handle_type, handle_path):
        """
        car_p_ser_path = {}
        key: 停车场名称/时间戳
        value: carparking_serial
        value: collection_record_serial
        # value: relative dir for all files
        handle_type = 1 追势
        handle_type = 2 泽尔
        handle_type = 3 其他
        """
        if car_p_encoding in self.car_p_ser_path:
            return self.car_p_ser_path[car_p_encoding]
        elif car_p_encoding in self.error_car_p_ser_path:
            return False
        else:
            carparking_name = car_p_encoding.split("/")[0]
            unique_time_string = car_p_encoding.split("/")[1]
            try:
                carparking_serial = self.get_car_parking_info(carparking_name)["data"]["carparking_serial"]  # get_car_parking_info: {'code': 4004, 'data': '', 'msg': '暂无此停车场信息录入'}
                print(f"#### carparking_serial: {carparking_serial}  unique_time_string: {unique_time_string} #######")
                collection_record_serial = self.get_carparking_collection_record_info(carparking_serial, unique_time_string)["data"]["collection_record_serial"]
            except Exception as e:
                logging.info(f"######error: {e}#######")
                logging.info(f"get_car_parking_info: {carparking_name} {self.get_car_parking_info(carparking_name)}")
                logging.info(f"get_carparking_collection_record_info: {carparking_name} {self.get_carparking_collection_record_info(carparking_serial, unique_time_string)}")
                self.error_car_p_ser_path[car_p_encoding] = {
                    "carparking_name": carparking_name,
                    "unique_time_string": unique_time_string
                }
                return False
            self.car_p_ser_path[car_p_encoding] = {
                "carparking_name": carparking_name,
                "carparking_serial": carparking_serial,
                "unique_time_string": unique_time_string,
                "collection_record_serial": collection_record_serial,
                "handle_type": handle_type,
                "handle_path": handle_path,
                "handle_status": False
            }
        return True

    # def manual_walk_dir(self, origin_dir):
    #     """
    #     # 针对同一停车场的密集数据入库
    #     # 读取文件路径，获取停车场名称和唯一时间戳
    #     # walk记录运行到多少行, 跳过重复处理位置
    #     # 格式：
    #     # - 停车场名称
    #     #     - video1_name.mp4
    #     #     - video1_name.mp4
    #     """
    #     num = 0
    #     for root, dirs, files in os.walk(origin_dir, topdown=False):
    #         for file_name in files:
    #             full_f_name = os.path.join(root, file_name)
    #             if file_name.endswith("mp4"):
    #                 carparking_name = full_f_name.split(os.path.sep)[-2]
    #                 unique_time_string = file_name.split(".")[0]

    def walk_dir(self, origin_dir):
        """
        # 读取文件路径，获取停车场名称和唯一时间戳
        # walk记录运行到多少行, 跳过重复处理位置

        # 格式1:
        # - 追势自有格式
        # - - 停车场名称
        #     - 1、Raw_Video
        #         - video1_name.mp4
        #         - video2_name.mp4
        #         - ....
        #     - 2、Config
        #         - PC
        #             - smc_xxx.bin
        #     - 3、Map
        #     - 4、IMU

        # 格式2:
        # 。。。

        # 先读待处理文件夹
        # 然后挨个文件夹处理
        """
        num = 0
        suffix = origin_dir.replace(os.path.sep, "-")
        with open(f"./walk_log_{suffix}.log.txt", "a", encoding="utf-8") as f:
            for root, dirs, files in os.walk(origin_dir, topdown=False):
                for file_name in files:
                    num += 1
                    full_f_name = os.path.join(root, file_name)
                    f.write(f"#line{num}: {full_f_name}\n")
                    if file_name.endswith("mp4"):
                        # 格式检查
                        if "1、Raw_Video" in full_f_name:
                            # 追势自有格式
                            carparking_name = full_f_name.split(os.path.sep)[-3]
                            # unique_time_string = file_name.split(".")[0].replace("_", "-")
                            unique_time_string = f"{file_name[:8]}-{file_name[9:11]}-{file_name[11:13]}-{file_name[13:15]}"
                            handle_path = os.path.sep.join(full_f_name.split(os.path.sep)[:-2])
                            print(f"##### {carparking_name}/{unique_time_string}  {handle_path}")
                            self.set_car_p_ser_handle_path(f"{carparking_name}/{unique_time_string}", handle_type=1, handle_path=handle_path)
                        else:
                            # 追势自有格式错误
                            # todo log
                            f.write(f"#line{num}[WARNING]:{full_f_name}\n")
                            logging.warning(f"#line{num} {full_f_name}")  # 创建一条严重级别为WARNING的日志记录
                    elif file_name.endswith("avi"):
                        if f"input{os.path.sep}video" in full_f_name:
                            # 泽尔格式
                            carparking_name = full_f_name.split(os.path.sep)[-5]
                            unique_time_string = full_f_name.split(os.path.sep)[-4]
                            handle_path = os.path.sep.join(full_f_name.split(os.path.sep)[:-4])
                            self.set_car_p_ser_handle_path(f"{carparking_name}/{unique_time_string}", handle_type=2, handle_path=handle_path)
                        else:
                            # 泽尔格式错误
                            # todo log
                            logging.warning(f"#line{num}[WARNING]:{full_f_name}")  # 创建一条严重级别为WARNING的日志记录
            logging.info(f"#### 待处理停车场采集批次数量: {len(self.car_p_ser_path)}")
        return self.car_p_ser_path

    def handle_local(self):
        handle_num = 0
        total_num = 0
        car_p_ser_path_num = 0
        for car_p_ser in self.car_p_ser_path:
            car_p_ser_path_num += 1
            tmp_car_p_ser = self.car_p_ser_path[car_p_ser]
            logging.info(f"#### 处理第{car_p_ser_path_num}/{len(self.car_p_ser_path)} {car_p_ser}")
            if tmp_car_p_ser["handle_status"] is False:
                # 未处理过，进入处理模式
                # carparking_name = tmp_car_p_ser["carparking_name"]
                carparking_serial = tmp_car_p_ser["carparking_serial"]
                collection_record_serial = tmp_car_p_ser["collection_record_serial"]
                unique_time_string = tmp_car_p_ser["unique_time_string"]
                handle_type = tmp_car_p_ser["handle_type"]
                handle_path = tmp_car_p_ser["handle_path"]
                if handle_type == 1:  # zhuishi
                    raw_video_path = os.path.join(handle_path, "1、Raw_Video")
                    for root, dirs, files in os.walk(raw_video_path, topdown=False):
                        for file_name in files:
                            # _temp = unique_time_string.replace("-", "_")
                            _temp_list = unique_time_string.split("-")
                            _temp = f"{_temp_list[0]}_{_temp_list[1]}{_temp_list[2]}{_temp_list[3]}"
                            # print(f"#### local_file_name {_temp}")
                            if file_name == f"{_temp}.mp4":
                                full_f_name = os.path.join(root, file_name)
                                target_file_path_key = f"origin/{carparking_serial}-{collection_record_serial}/{carparking_serial}-{collection_record_serial}.mp4"
                                # # smc_file
                                # smc_file = self.try_get_smc(handle_path)
                                self.common_handle_file(full_f_name, target_file_path_key, carparking_serial, collection_record_serial)
                                handle_num += 1
                                total_num += 1
                            else:
                                total_num += 1
                                continue
                elif handle_type == 2:  # zeer
                    unique_time_string_path = os.path.join(handle_path, unique_time_string)
                    bus_blf_path = os.path.join(unique_time_string_path, f"input{os.path.sep}bus")
                    logging.debug(f"######## walk in {bus_blf_path}")
                    for file in os.listdir(bus_blf_path):
                        logging.debug(f"######## f: {file}")
                        if file.endswith(".blf"):
                            bus_blf_file = os.path.join(bus_blf_path, file)
                            target_file_path_key = f"origin/{carparking_serial}-{collection_record_serial}/{carparking_serial}-{collection_record_serial}-{file}"
                            self.common_handle_file(bus_blf_file, target_file_path_key, carparking_serial, collection_record_serial)
                            handle_num += 1
                            total_num += 1
                            break
                        else:
                            total_num += 1
                            continue
                    raw_csv_path = os.path.join(unique_time_string_path, f"input{os.path.sep}raw")
                    logging.debug(f"######## walk in {raw_csv_path}")
                    for file in os.listdir(raw_csv_path):
                        logging.debug(f"######## f: {file}")
                        if file.endswith(".csv"):
                            raw_csv_file = os.path.join(raw_csv_path, file)
                            target_file_path_key = f"origin/{carparking_serial}-{collection_record_serial}/{carparking_serial}-{collection_record_serial}-{file}"
                            self.common_handle_file(raw_csv_file, target_file_path_key, carparking_serial, collection_record_serial)
                            handle_num += 1
                            total_num += 1
                            break
                        else:
                            total_num += 1
                            continue
                    video_path = os.path.join(unique_time_string_path, f"input{os.path.sep}video")
                    logging.debug(f"######## walk in {video_path}")
                    for file in os.listdir(video_path):
                        logging.debug(f"######## f: {file}")
                        if file.endswith(".avi") or file.endswith(".csv"):
                            full_f_name = os.path.join(video_path, file)
                            target_file_path_key = f"origin/{carparking_serial}-{collection_record_serial}/{carparking_serial}-{collection_record_serial}-{file}"
                            self.common_handle_file(full_f_name, target_file_path_key, carparking_serial, collection_record_serial)
                            handle_num += 1
                            total_num += 1
                        else:
                            total_num += 1
                            continue
        return (handle_num, total_num)

    def common_handle_file(self, full_f_name, target_file_path_key, carparking_serial, collection_record_serial):
        # md5
        md5 = self.get_file_md5(full_f_name)
        # 后缀
        suffix = self.get_file_suffix(full_f_name)
        # size
        size = self.get_file_size(full_f_name)
        # upload
        # qcloud tmp key
        qcloud_res = self.get_tmp_qcloud_id_key(target_file_path_key, md5)
        tmp_secret_id = qcloud_res['credentials']['tmpSecretId']
        tmp_secret_key = qcloud_res['credentials']['tmpSecretKey']
        tmp_secret_token = qcloud_res['credentials']['sessionToken']
        qcloud_region = qcloud_res['qcloud_region']
        qcloud_bucket_name = qcloud_res['qcloud_bucket_name']
        if_ever = False
        qcloud_handle_instance = QCloudHandle(tmp_secret_id, tmp_secret_key, qcloud_region, qcloud_bucket_name, if_ever, tmp_secret_token)
        qcloud_handle_instance.upload_file(full_f_name, target_file_path_key)  # /Users/leo/Downloads/SEED-Ubuntu20.04.zip
        logging.debug(f"## qcloud_handle_instance ###full_f_name: {full_f_name} ###target_file_path_key: {target_file_path_key}")
        # 提交数据记录到数据管理平台
        requests_payload = {
            "carparking_serial": carparking_serial,
            "collection_record_serial": collection_record_serial,
            "qcloud_sts_request_key": qcloud_res["requestId"],
            "target_file_path_key": target_file_path_key,
            "md5": md5,
            "suffix": suffix,
            "size": size,
            "full_f_name": full_f_name,
        }
        res = requests_post(self.collection_data_upload_url, requests_payload, {"Authorization": self.authorization})
        res_reason = res.reason
        assert res.status_code == 200, f"请求有错, errmsg【{res_reason}】"
        json_data = json.loads(res.text)
        return json_data

    def frame_handle(self, file_name, frame_full_name, target_file_path_key):
        res = requests_get(self.frame_data_upload_url, {"file_name": file_name}, {"Authorization": self.authorization})
        assert res.status_code == 200, f"请求有错, errmsg【{res.reason}】"
        json_data = json.loads(res.text)
        if json_data['code'] == 2000:
            # 存在
            return json_data['data']['frame_id']
        elif json_data['code'] == 4004:
            # 无此记录
            md5 = self.get_file_md5(frame_full_name)
            # qcloud tmp key
            qcloud_res = self.get_tmp_qcloud_id_key(target_file_path_key, md5)
            tmp_secret_id = qcloud_res['credentials']['tmpSecretId']
            tmp_secret_key = qcloud_res['credentials']['tmpSecretKey']
            tmp_secret_token = qcloud_res['credentials']['sessionToken']
            qcloud_region = qcloud_res['qcloud_region']
            qcloud_bucket_name = qcloud_res['qcloud_bucket_name']
            if_ever = False
            qcloud_handle_instance = QCloudHandle(tmp_secret_id, tmp_secret_key, qcloud_region, qcloud_bucket_name, if_ever, tmp_secret_token)
            qcloud_handle_instance.upload_file(frame_full_name, target_file_path_key)
            requests_payload = {
                "qcloud_sts_request_key": qcloud_res["requestId"],
                "target_file_path_key": target_file_path_key,
                "md5": md5,
                "file_name": file_name,
            }
            res = requests_post(self.frame_data_upload_url, requests_payload, {"Authorization": self.authorization})
            res_reason = res.reason
            assert res.status_code == 200, f"请求有错, errmsg【{res_reason}】"
            json_data = json.loads(res.text)
            assert json_data['code'] == 2000, f"请求有错, errmsg【{res_reason}】"
            return json_data['data']['frame_id']
        else:
            raise ValueError(f"请求有错 {file_name}")

    def annotation_file_handle(self, annotation_payload):
        # annotation_payload = {
        #     "frame_name": item['frame_name'],
        #     "frame_id": frame_id_dict[item['frame_name']],
        #     "file_name": item['new_file_name'],
        #     "full_f_name": item['full_f_name'],
        #     "file_type": item['file_type'],
        #     "file_name_type": item['file_name_type'],
        #     "target_file_path_key": f"data/{item['file_dataset_code']}/{item['new_file_name']}",
        #     "file_dataset_code": item['file_dataset_code'],
        #     "file_dataset_name": item['file_dataset_name'],
        #     "task_code": task_code,
        # }
        # 上传annotation file
        md5 = self.get_file_md5(annotation_payload['full_f_name'])
        qcloud_res = self.get_tmp_qcloud_id_key(annotation_payload['target_file_path_key'], md5)
        tmp_secret_id = qcloud_res['credentials']['tmpSecretId']
        tmp_secret_key = qcloud_res['credentials']['tmpSecretKey']
        tmp_secret_token = qcloud_res['credentials']['sessionToken']
        qcloud_region = qcloud_res['qcloud_region']
        qcloud_bucket_name = qcloud_res['qcloud_bucket_name']
        if_ever = False
        qcloud_handle_instance = QCloudHandle(tmp_secret_id, tmp_secret_key, qcloud_region, qcloud_bucket_name, if_ever, tmp_secret_token)
        qcloud_handle_instance.upload_file(annotation_payload['full_f_name'], annotation_payload['target_file_path_key']) 
        # 提交annotation record
        requests_payload = {
            # "bucket_id": bucket_id,
            "file_name": annotation_payload['file_name'],
            "target_file_path_key": annotation_payload['target_file_path_key'],
            "md5": md5,
            "qcloud_sts_request_key": qcloud_res["requestId"],
            "frame_id": annotation_payload['frame_id'],
            "file_dataset_code": annotation_payload['file_dataset_code'],
            "file_dataset_name": annotation_payload['file_dataset_name'],
            "task_code": annotation_payload['task_code'],
            "file_type": annotation_payload['file_type'],
        }
        res = requests_post(self.annotation_data_upload_url, requests_payload, {"Authorization": self.authorization})
        res_reason = res.reason
        assert res.status_code == 200, f"请求有错, errmsg【{res_reason}】"
        json_data = json.loads(res.text)
        if json_data['code'] != 2000:
            raise ValueError(f"标注数据提交有错 {json_data['msg']}")
        return json_data

    def file_collection_data_upload(self, line, total_num, match_num, handle_num):
        total_num += 1
        if "/data/" in line:
            match_num += 1
            fir_split_line_texts = line.split("##")
            origin_full_file_path = fir_split_line_texts[1].replace("/ ", "/")
            full_f_name = "offline" + origin_full_file_path.replace("/data/", f"/data{fir_split_line_texts[0]}/")
            carparking_name = full_f_name.split(os.path.sep)[3]
            unique_time_string = full_f_name.split(os.path.sep)[4]
            car_p_encoding = f"{carparking_name}/{unique_time_string}"
            if car_p_encoding in self.car_p_ser_path:
                # self.car_p_ser_path[car_p_encoding] = {
                #     "carparking_name": carparking_name,
                #     "carparking_serial": carparking_serial,
                #     "unique_time_string": unique_time_string,
                #     "collection_record_serial": collection_record_serial,
                #     "handle_type": handle_type,
                #     "handle_path": handle_path,
                #     "handle_status": False
                # }
                carparking_serial = self.car_p_ser_path[car_p_encoding]['carparking_serial']
                collection_record_serial = self.car_p_ser_path[car_p_encoding]['collection_record_serial']
                handle_type = self.car_p_ser_path[car_p_encoding]['handle_type']
                md5 = fir_split_line_texts[2]
                suffix = fir_split_line_texts[3]
                size = fir_split_line_texts[4]
                file = full_f_name.split("/")[-1]
                if handle_type == 2:
                    if full_f_name.endswith(".blf"):
                        handle_num += 1
                        target_file_path_key = f"origin/{carparking_serial}-{collection_record_serial}/{carparking_serial}-{collection_record_serial}-{file}"
                        self.collection_data_upload(carparking_serial, collection_record_serial, target_file_path_key, md5, suffix, size, full_f_name)
                    elif full_f_name.endswith("raw.csv"):
                        if "/raw/" in full_f_name:
                            handle_num += 1
                            target_file_path_key = f"origin/{carparking_serial}-{collection_record_serial}/{carparking_serial}-{collection_record_serial}-{file}"
                            self.collection_data_upload(carparking_serial, collection_record_serial, target_file_path_key, md5, suffix, size, full_f_name)
                        else:
                            self.write_log(f"#file_collection_data_upload#0#{line}")
                            pass
                    elif full_f_name.endswith(".csv"):
                        if "/video/" in full_f_name:
                            handle_num += 1
                            target_file_path_key = f"origin/{carparking_serial}-{collection_record_serial}/{carparking_serial}-{collection_record_serial}-{file}"
                            self.collection_data_upload(carparking_serial, collection_record_serial, target_file_path_key, md5, suffix, size, full_f_name)
                        else:
                            self.write_log(f"#file_collection_data_upload#1#{line}")
                            pass
                    elif full_f_name.endswith("raw.avi"):
                        handle_num += 1
                        target_file_path_key = f"origin/{carparking_serial}-{collection_record_serial}/{carparking_serial}-{collection_record_serial}-{file}"
                        self.collection_data_upload(carparking_serial, collection_record_serial, target_file_path_key, md5, suffix, size, full_f_name)
                    else:
                        self.write_log(f"#file_collection_data_upload#2#{line}")
                        pass
                else:
                    self.write_log(f"#file_collection_data_upload#3#{line}")
            else:
                self.write_log(f"#file_collection_data_upload#4#{line}")
                # 当前停车场信息未入库
                pass
        return total_num, match_num, handle_num

    def collection_data_upload(self, carparking_serial, collection_record_serial, target_file_path_key, md5, suffix, size, full_f_name):
        requests_payload = {
            "carparking_serial": carparking_serial,
            "collection_record_serial": collection_record_serial,
            "qcloud_sts_request_key": None,
            "target_file_path_key": target_file_path_key,
            "md5": md5,
            "suffix": suffix,
            "size": size,
            "full_f_name": full_f_name,
        }
        res = requests_post(self.collection_data_upload_url, requests_payload, {"Authorization": self.authorization})
        res_reason = res.reason
        assert res.status_code == 200, f"请求有错, errmsg【{res_reason}】"
        json_data = json.loads(res.text)
        return json_data

    def try_get_smc(self, handle_path):
        smc_path = os.path.join(handle_path, f"2、Config{os.path.sep}PC")
        smc_file = None
        for file in os.listdir(smc_path):
            if file.endswith(".bin"):
                smc_file = os.path.join(smc_path, file)
                break
            else:
                continue
        return smc_file

    def get_file_suffix(self, fname):
        try:
            return fname.split(".")[-1]
        except Exception:
            return "error"

    def get_file_md5(self, fname):
        try:
            m = hashlib.md5()   # 创建md5对象
            with open(fname, 'rb') as fobj:
                while True:
                    data = fobj.read(4096)
                    if not data:
                        break
                    m.update(data)  # 更新md5对象
            return m.hexdigest()    # 返回md5对象
        except Exception:
            return "error"

    def get_file_size(self, fname):
        # os.stat_result(st_mode=33188, st_ino=14412668, st_dev=16777229, st_nlink=1, st_uid=501, st_gid=20, st_size=2515, st_atime=1681784164, st_mtime=1681784151, st_ctime=1681784163)
        # return os.stat(fname).st_size
        return os.path.getsize(fname)

    def walk_log_file(self, file_name):
        """
        1、先运行walk_log_file
        2、再运行walk_log_and_upload_info
        """
        total_num = 0
        match_num = 0
        handle_num = 0
        with open(file_name, 'r') as file:
            while True:
                line = file.readline()
                if line:
                    total_num, match_num, handle_num = self.line_handle(line, total_num, match_num, handle_num)
                    if total_num % 500 == 0:
                        logging.info(f"进度第{total_num}行")
                else:
                    break
        return total_num, match_num, handle_num

    def walk_log_and_upload_info(self, file_name):
        """
        1、先运行walk_log_file
        2、再运行walk_log_and_upload_info
        """
        total_num = 0
        match_num = 0
        handle_num = 0
        with open(file_name, 'r') as file:
            while True:
                line = file.readline()
                if line:
                    total_num, match_num, handle_num = self.file_collection_data_upload(line, total_num, match_num, handle_num)
                    if total_num % 500 == 0:
                        logging.info(f"进度第{total_num}行")
                else:
                    break
        return self.car_p_ser_path

    def write_log(self, to_write_text):
        f = open(self._log_file_name, "a+", encoding='utf-8')
        f.writelines(to_write_text+"\n")
        f.close()

    def line_handle(self, line, total_num, match_num, handle_num):
        total_num += 1
        if "/data/" in line:
            fir_split_line_texts = line.split("##")
            origin_full_file_path = fir_split_line_texts[1].replace("/ ", "/")
            full_f_name = "offline" + origin_full_file_path.replace("/data/", f"/data{fir_split_line_texts[0]}/")
            if full_f_name.endswith("mp4"):
                pass
                # # 格式检查
                # if "1、Raw_Video" in full_f_name:
                #     # 追势自有格式
                #     carparking_name = full_f_name.split(os.path.sep)[-3]
                #     unique_time_string = file_name.split(".")[0]
                #     handle_path = os.path.sep.join(full_f_name.split(os.path.sep)[:-2])
                #     self.set_car_p_ser_handle_path(f"{carparking_name}/{unique_time_string}", handle_type=1, handle_path=handle_path)
                # else:
                #     # 追势自有格式错误
                #     # todo log
                #     f.write(f"#line{num}[WARNING]:{full_f_name}\n")
                #     logging.warning(f"#line{num} {full_f_name}")  # 创建一条严重级别为WARNING的日志记录
            elif full_f_name.endswith("raw.csv"):
                match_num += 1
                if f"input{os.path.sep}raw" in full_f_name:
                    # 泽尔格式
                    carparking_name = full_f_name.split(os.path.sep)[3]
                    unique_time_string = full_f_name.split(os.path.sep)[4]
                    handle_path = os.path.sep.join(full_f_name.split(os.path.sep)[:5])  # 'offline/data/20220721/唯亭旺角停车场/20220721-19-58-42'
                    res = self.set_car_p_ser_handle_path(f"{carparking_name}/{unique_time_string}", handle_type=2, handle_path=handle_path)
                    if res:
                        handle_num += 1
                    else:
                        self.write_log(f"#line_handle#{line}")
                        pass
                else:
                    # 泽尔格式错误
                    # todo log
                    logging.warning(f"#{line}")  # 创建一条严重级别为WARNING的日志记录
        return total_num, match_num, handle_num

    # def annotation_result_handle(self, file_dir):
    #     for root, dirs, files in os.walk(file_dir, topdown=False):
    #         for file_name in files:
    #             if file_name.endswith(".json"):
    #                 full_file_path = os.path.join(root, file_name)
    #                 split_full_file_path_list = full_file_path.split("/")
    #                 output_dir_name = split_full_file_path_list[-2]
    #                 dataset_name = split_full_file_path_list[-3]


class QCloudHandle:
    '''
    # 功能点，读取文件路径，获取入库信息
    # 如果您一定要使用永久密钥来生成预签名，建议永久密钥的权限范围仅限于上传或下载操作，以规避风险。并且所生成的签名有效时长设置为完成本次上传或下载操作所需的最短期限，因为，当指定预签名 URL 的有效时间过期后，请求会中断；申请新的签名后，需要重新执行失败请求，不支持断点续传。
    # 分别封装永久密钥和临时密钥方案
    '''
    def __init__(self, secret_id, secret_key, region, bucket_name, if_ever=False, token=None):
        self.if_ever = if_ever            # 密钥状态，False: 临时, True: 永久
        self.secret_id = secret_id
        self.secret_key = secret_key
        self.region = region
        self.bucket_name = bucket_name
        self.token = token
        self.scheme = 'https'
        self.config = CosConfig(Region=self.region, SecretId=self.secret_id, SecretKey=self.secret_key, Token=self.token, Scheme=self.scheme)
        self.client = CosS3Client(self.config)

    def percentage(self, consumed_bytes, total_bytes):
        """
        ### 进度条回调函数，计算当前上传的百分比
        :param consumed_bytes: 已经上传/下载的数据量
        :param total_bytes: 总数据量
        """
        if total_bytes:
            rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
            logging.debug('\r{0}% '.format(rate))
            sys.stdout.flush()

    def upload_file(self, tmp_file_path, target_file_path, **append_headers):
        '''
        ### 高级上传接口（推荐）
        # 根据文件大小自动选择简单上传或分块上传，分块上传具备断点续传功能。
        '''
        if append_headers:
            meta_data = append_headers
        else:
            meta_data = {}
        response = self.client.upload_file(
            Bucket=self.bucket_name,      # Bucket='examplebucket-1250000000',
            LocalFilePath=tmp_file_path,  # 'local.txt'
            Key=target_file_path,         # 对象键（Key）是对象在存储桶中的唯一标识。例如，在对象的访问域名 examplebucket-1250000000.cos.ap-guangzhou.myqcloud.com/doc/pic.jpg 中，对象键为 doc/pic.jpg
            PartSize=1,                   # 分块上传的分块大小，默认为1MB
            MAXThread=10,                 # 分块上传的并发数量，默认为5个线程上传分块
            EnableMD5=True,              # 是否需要 SDK 计算 Content-MD5，默认关闭，打开后会增加上传耗时
            progress_callback=self.percentage,       # 上传进度的回调函数，可以通过自定义此函数，来获取上传进度
            Metadata=meta_data,                  # 用户自定义的对象元数据
        )
        return response

    def head_object(self, object_key):
        response = self.client.head_object(
            Bucket=self.bucket_name,
            Key=object_key
        )
        return response

    def list_objects(self, prefix):
        # 列举 folder1 目录下的文件：COS中的目录是'/'结尾的前缀名
        # 列举 folder1 目录下的文件和子目录
        response = self.client.list_objects(
            Bucket=self.bucket_name, Prefix=prefix, Delimiter='/')
        return response
        # {
        #     'Name': 'space-1316803438',
        #     'EncodingType': 'url',
        #     'Prefix': 'tmp/',
        #     'Marker': None,
        #     'MaxKeys': '1000',
        #     'Delimiter': '/',
        #     'IsTruncated': 'false',
        #     'CommonPrefixes': [{
        #         'Prefix': 'tmp/testdir/'
        #     }, {
        #         'Prefix': 'tmp/testdir2/'
        #     }],
        #     'Contents': [{
        #         'Key': 'tmp/',
        #         'LastModified': '2023-02-13T07:46:29.000Z',
        #         'ETag': '"d41d8cd98f00b204e9800998ecf8427e"',
        #         'Size': '0',
        #         'Owner': {
        #             'ID': '1316803438',
        #             'DisplayName': '1316803438'
        #         },
        #         'StorageClass': 'STANDARD'
        #     }, {
        #         'Key': 'tmp/73453.json',
        #         'LastModified': '2023-02-13T07:48:21.000Z',
        #         'ETag': '"75e4a2bd9429986f8b0ec52cf6498b75"',
        #         'Size': '11640',
        #         'Owner': {
        #             'ID': '1316803438',
        #             'DisplayName': '1316803438'
        #         },
        #         'StorageClass': 'STANDARD'
        #     }, {
        #         'Key': 'tmp/IMG_7308.jpg',
        #         'LastModified': '2023-02-21T07:10:03.000Z',
        #         'ETag': '"0fba7b2a1772a2a4ccff83afbab23805"',
        #         'Size': '1357726',
        #         'Owner': {
        #             'ID': '1316803438',
        #             'DisplayName': '1316803438'
        #         },
        #         'StorageClass': 'STANDARD_IA'
        #     }, {
        #         'Key': 'tmp/IMG_7308.jpg%3Fv=456.jpg',
        #         'LastModified': '2023-02-21T07:16:37.000Z',
        #         'ETag': '"a26173becab0d55ee5f051e1f4f30828"',
        #         'Size': '1766001',
        #         'Owner': {
        #             'ID': '1316803438',
        #             'DisplayName': '1316803438'
        #         },
        #         'StorageClass': 'STANDARD_IA'
        #     }, {
        #         'Key': 'tmp/IMG_7308.jpg?v=123.jpg',
        #         'LastModified': '2023-02-21T07:07:02.000Z',
        #         'ETag': '"a26173becab0d55ee5f051e1f4f30828"',
        #         'Size': '1766001',
        #         'Owner': {
        #             'ID': '1316803438',
        #             'DisplayName': '1316803438'
        #         },
        #         'StorageClass': 'STANDARD_IA'
        #     }, {
        #         'Key': 'tmp/IMG_7308.jpg@v=123.jpg',
        #         'LastModified': '2023-02-21T07:17:47.000Z',
        #         'ETag': '"a26173becab0d55ee5f051e1f4f30828"',
        #         'Size': '1766001',
        #         'Owner': {
        #             'ID': '1316803438',
        #             'DisplayName': '1316803438'
        #         },
        #         'StorageClass': 'STANDARD_IA'
        #     }, {
        #         'Key': 'tmp/P1ZnOzEgoH-0001-317250-0-Bev_H-12m.jpg',
        #         'LastModified': '2023-02-17T07:30:14.000Z',
        #         'ETag': '"9f7253471baba4d7ec7b39edbddbd4a9"',
        #         'Size': '658069',
        #         'Owner': {
        #             'ID': '1316803438',
        #             'DisplayName': '1316803438'
        #         },
        #         'StorageClass': 'STANDARD_IA'
        #     }, {
        #         'Key': 'tmp/P1ZnOzEgoH-0001-317250-0-Front.jpg',
        #         'LastModified': '2023-02-17T07:30:13.000Z',
        #         'ETag': '"a2c09cb4ddb01976b84a7262d674ea2d"',
        #         'Size': '251645',
        #         'Owner': {
        #             'ID': '1316803438',
        #             'DisplayName': '1316803438'
        #         },
        #         'StorageClass': 'STANDARD_IA'
        #     }, {
        #         'Key': 'tmp/P1ZnOzEgoH-0001-317250-0-Left.jpg',
        #         'LastModified': '2023-02-17T07:30:13.000Z',
        #         'ETag': '"e14f79f58c1e3c31e9903a64978ee77b"',
        #         'Size': '258395',
        #         'Owner': {
        #             'ID': '1316803438',
        #             'DisplayName': '1316803438'
        #         },
        #         'StorageClass': 'STANDARD_IA'
        #     }, {
        #         'Key': 'tmp/P1ZnOzEgoH-0001-317250-0-Rear.jpg',
        #         'LastModified': '2023-02-17T07:30:14.000Z',
        #         'ETag': '"a510f7fdadc9a90ea7ea8241cbb7297e"',
        #         'Size': '271800',
        #         'Owner': {
        #             'ID': '1316803438',
        #             'DisplayName': '1316803438'
        #         },
        #         'StorageClass': 'STANDARD_IA'
        #     }, {
        #         'Key': 'tmp/P1ZnOzEgoH-0001-317250-0-Right.jpg',
        #         'LastModified': '2023-02-17T07:30:13.000Z',
        #         'ETag': '"2fb9d0deb0db69f7d3c29a14ad7f93ea"',
        #         'Size': '269675',
        #         'Owner': {
        #             'ID': '1316803438',
        #             'DisplayName': '1316803438'
        #         },
        #         'StorageClass': 'STANDARD_IA'
        #     }, {
        #         'Key': 'tmp/local2.jpg',
        #         'LastModified': '2023-02-17T06:41:29.000Z',
        #         'ETag': '"9f7253471baba4d7ec7b39edbddbd4a9"',
        #         'Size': '658069',
        #         'Owner': {
        #             'ID': '1316803438',
        #             'DisplayName': '1316803438'
        #         },
        #         'StorageClass': 'STANDARD_IA'
        #     }, {
        #         'Key': 'tmp/screenshot-20230324-151321.png',
        #         'LastModified': '2023-04-17T07:05:42.000Z',
        #         'ETag': '"72398e271395dc82ff9ab7586b28ae6b"',
        #         'Size': '188856',
        #         'Owner': {
        #             'ID': '1316803438',
        #             'DisplayName': '1316803438'
        #         },
        #         'StorageClass': 'STANDARD'
        #     }, {
        #         'Key': 'tmp/screenshot-20230413-114619.png',
        #         'LastModified': '2023-04-14T07:16:12.000Z',
        #         'ETag': '"8a16a6bdeb1cf72cadebd6e914ac54c7"',
        #         'Size': '202725',
        #         'Owner': {
        #             'ID': '1316803438',
        #             'DisplayName': '1316803438'
        #         },
        #         'StorageClass': 'STANDARD'
        #     }, {
        #         'Key': 'tmp/smc_es6_2306.bin',
        #         'LastModified': '2023-02-17T06:39:57.000Z',
        #         'ETag': '"98f55cbf2abc87ef9f5d02f96383e4e8"',
        #         'Size': '41984',
        #         'Owner': {
        #             'ID': '1316803438',
        #             'DisplayName': '1316803438'
        #         },
        #         'StorageClass': 'STANDARD'
        #     }, {
        #         'Key': 'tmp/smc_es6_23062.bin',
        #         'LastModified': '2023-02-17T06:41:28.000Z',
        #         'ETag': '"98f55cbf2abc87ef9f5d02f96383e4e8"',
        #         'Size': '41984',
        #         'Owner': {
        #             'ID': '1316803438',
        #             'DisplayName': '1316803438'
        #         },
        #         'StorageClass': 'STANDARD'
        #     }, {
        #         'Key': 'tmp/smc_tianji_pc_20230414.bin',
        #         'LastModified': '2023-04-14T06:43:10.000Z',
        #         'ETag': '"a620609e330da7e4233883ca004ff9a9"',
        #         'Size': '41984',
        #         'Owner': {
        #             'ID': '1316803438',
        #             'DisplayName': '1316803438'
        #         },
        #         'StorageClass': 'STANDARD'
        #     }]
        # }
    
        # # 打印文件列表
        # if 'Contents' in response:
        #     for content in response['Contents']:
        #         print(content['Key'])
        # # 打印子目录
        # if 'CommonPrefixes' in response:
        #     for folder in response['CommonPrefixes']:
        #         print(folder['Prefix'])

    def get_object_file(self, target_file_path, output_file_path):
        '''
        # 文件下载 获取文件到本地
        '''
        try:
            response = self.client.get_object(
                Bucket=self.bucket_name,
                Key=target_file_path,
            )
            response['Body'].get_stream_to_file(output_file_path)
            return None
        except CosServiceError as e:
            # print(e.get_origin_msg())
            # print(e.get_digest_msg())
            # print(e.get_status_code())
            # print(e.get_error_code())
            # print(e.get_error_msg())
            # print(e.get_resource_location())
            # print(e.get_trace_id())
            # print(e.get_request_id())
            return e

    def get_object_stream(self, target_file_path):
        '''
        # 文件下载 获取文件流
        '''
        response = self.client.get_object(
            Bucket=self.bucket_name,
            Key=target_file_path,
        )
        fp = response['Body'].get_raw_stream()
        # print(fp.read(2))
        return fp

    def gen_file_download_url(self, target_file_path):
        # 生成下载 URL，同时指定响应的 content-disposition 头部，让文件在浏览器另存为，而不是显示
        if self.if_ever:
            url = self.client.get_presigned_url(
                Method='GET',
                Bucket=self.bucket_name,
                Key=target_file_path,
                SignHost=True,  # 决定请求域名算入签名，不允许使用者修改请求域名
                Params={
                    # 'response-content-disposition': f'attachment; filename={target_file_path.split("/")[-1]}'  # 下载时保存为指定的文件
                    'response-content-disposition': f'inline; filename={target_file_path.split("/")[-1]}',  # 直接在浏览器中打开该文件
                    # 除了 response-content-disposition，还支持 response-cache-control、response-content-encoding、response-content-language、
                    # response-content-type、response-expires 等请求参数，详见下载对象 API，https://cloud.tencent.com/document/product/436/7753
                },
                Expired=120  # 120秒后过期，过期时间请根据自身场景定义
            )
        else:
            logging.debug(f"--not if_ever{self.if_ever}")
            url = self.client.get_presigned_url(
                Method='GET',
                Bucket=self.bucket_name,
                Key=target_file_path,
                SignHost=False,  # 决定请求域名算入签名，不允许使用者修改请求域名
                Params={
                    # 'response-content-disposition': f'attachment; filename={target_file_path.split("/")[-1]}'  # 下载时保存为指定的文件
                    'response-content-disposition': f'inline; filename={target_file_path.split("/")[-1]}',  # 直接在浏览器中打开该文件
                    # 除了 response-content-disposition，还支持 response-cache-control、response-content-encoding、response-content-language、
                    # response-content-type、response-expires 等请求参数，详见下载对象 API，https://cloud.tencent.com/document/product/436/7753
                    'x-cos-security-token': self.token
                },
                # Headers={'x-cos-traffic-limit': '819200'},  # 预签名 URL 本身是不包含请求头部的，但请求头部会算入签名，那么使用 URL 时就必须携带请求头部，并且请求头部的值必须是这里指定的值
                Expired=120  # 120秒后过期，过期时间请根据自身场景定义
            )
        return url

    # 列出当前目录子节点，返回所有子节点信息
    def listCurrentDir(self, prefix):
        file_infos = []
        sub_dirs = []
        marker = ""
        count = 1
        delimiter = ""
        while True:
            response = self.client.list_objects(self.bucket_name, prefix, delimiter, marker)
            # 调试输出
            # json_object = json.dumps(response, indent=4)
            # print(count, " =======================================")
            # print(json_object)
            count += 1

            if "CommonPrefixes" in response:
                common_prefixes = response.get("CommonPrefixes")
                sub_dirs.extend(common_prefixes)

            if "Contents" in response:
                contents = response.get("Contents")
                file_infos.extend(contents)

            if "NextMarker" in response.keys():
                marker = response["NextMarker"]
            else:
                break

        # print("=======================================================")

        # 如果 delimiter 设置为 "/"，则需要进行递归处理子目录，
        # sorted(sub_dirs, key=lambda sub_dir: sub_dir["Prefix"])
        # for sub_dir in sub_dirs:
        #     print(sub_dir)
        #     sub_dir_files = listCurrentDir(sub_dir["Prefix"])
        #     file_infos.extend(sub_dir_files)

        # print("=======================================================")

        sorted(file_infos, key=lambda file_info: file_info["Key"])
        # for file in file_infos:
        #     print(file)
        return file_infos

    # 下载文件到本地目录，如果本地目录已经有同名文件则会被覆盖；
    # 如果目录结构不存在，则会创建和对象存储一样的目录结构
    def downLoadFiles(self, file_infos, localDir="./download/"):
        pool = SimpleThreadPool()
        for file in file_infos:
            # 文件下载 获取文件到本地
            file_cos_key = file["Key"]
            localName = os.path.join(localDir, file_cos_key)

            # 如果本地目录结构不存在，递归创建
            if not os.path.exists(os.path.dirname(localName)):
                os.makedirs(os.path.dirname(localName))

            # skip dir, no need to download it
            if str(localName).endswith("/"):
                continue

            # 实际下载文件
            # 使用线程池方式
            pool.add_task(self.client.download_file, self.bucket_name, file_cos_key, localName)

            # 简单下载方式
            # response = client.get_object(
            #     Bucket=test_bucket,
            #     Key=file_cos_key,
            # )
            # response['Body'].get_stream_to_file(localName)

        pool.wait_completion()
        return None

    # 功能封装，下载对象存储上面的一个目录到本地磁盘
    def downLoadDirFromCos(self, prefix, localDir="./download/"):
        global file_infos

        try:
            file_infos = self.listCurrentDir(prefix)
        except CosServiceError as e:
            print(e.get_origin_msg())
            print(e.get_digest_msg())
            print(e.get_status_code())
            print(e.get_error_code())
            print(e.get_error_msg())
            print(e.get_resource_location())
            print(e.get_trace_id())
            print(e.get_request_id())

        self.downLoadFiles(file_infos, localDir)
        return None
    # client.downLoadDirFromCos(start_prefix, localDir)

    # 下载文件到本地目录，如果本地目录已经有同名文件则会被覆盖；
    # 如果目录结构不存在，则会创建和对象存储一样的目录结构
    def download_image_keys(self, image_keys, tmpdirname):
        pool = SimpleThreadPool()
        _handle_dict = {}
        for image_key_path in image_keys:
            tmp_img_path = os.path.join(tmpdirname, image_key_path)
            # 如果本地目录结构不存在，递归创建
            if not os.path.exists(os.path.dirname(tmp_img_path)):
                os.makedirs(os.path.dirname(tmp_img_path))
            pool.add_task(self.client.download_file, self.bucket_name, image_key_path, tmp_img_path)
            _handle_dict[image_key_path] = tmp_img_path
        pool.wait_completion()
        return _handle_dict

    def download_image_keys_nodir(self, image_keys, tmpdirname):
        pool = SimpleThreadPool()
        _handle_dict = {}
        for image_key_path in image_keys:
            tmp_img_path = os.path.join(tmpdirname, image_key_path.split("/")[-1])
            if not os.path.isfile(tmp_img_path):
                # 如果本地目录结构不存在，递归创建
                if not os.path.exists(os.path.dirname(tmp_img_path)):
                    os.makedirs(os.path.dirname(tmp_img_path))
                pool.add_task(self.client.download_file, self.bucket_name, image_key_path, tmp_img_path)
            _handle_dict[image_key_path] = tmp_img_path
        pool.wait_completion()
        return _handle_dict

    def loacl_get_pred_images(self, file_dir, model_code):
        predict_file_keys = []
        for root, dirs, files in os.walk(file_dir, topdown=False):
            for name in files:
                if name.endswith(".jpg"):
                    file_name = name.split("/")[-1]
                    predict_file_name = file_name.replace(".jpg", f".{model_code}.json")
                    predict_file_key = f"pred/{model_code}/{predict_file_name}"
                    predict_file_keys.append(predict_file_key)
        self.download_image_keys_nodir(predict_file_keys, file_dir)



"""
pip install spacetool, requests
import sys,os,json
pp2 = os.path.abspath(".")
sys.path.append(pp2)

# 测试
from spacetool import main_tool
d = main_tool.DataTool(name="", code="", host="http://127.0.0.1:8000/")

d.update_code("new_code")

# 测试上传停车场信息
d.upload_car_parking_info("虹桥时代广场", "上海", "青浦区", "高光路与高泾支路交叉口")
d.upload_car_parking_info("进博会P17停车场", "上海", "青浦区", "诸光路与卫家角交叉口")
d.upload_car_parking_info("久事西郊名墅")

d.get_car_parking_info("虹桥时代广场")
d.get_car_parking_info("进博会P17停车场")
d.get_car_parking_info("久事西郊名墅")
d.get_car_parking_info("空")

d.upload_carparking_collection_record_info("P1xpdGelKq", "20220828-11-55-44", {"update": True, "record_type": "bevs"})
d.upload_carparking_collection_record_info("P1xpdGelKq", "20220821-16-25-14")
d.upload_carparking_collection_record_info("P1xpdGelKq", "20220820-16-25-14")
d.upload_carparking_collection_record_info("P1xpdGelKq", "20220819-16-25-14", {"record_type": "bevs"})

d.get_carparking_collection_record_info("P10eQQrhfa", "20220828-11-55-44")
d.get_carparking_collection_record_info("P10eQQrhfa", "20220821-16-25-14")
d.get_carparking_collection_record_info("P10eQQrhfa", "20220820-16-25-14")
d.get_carparking_collection_record_info("P10eQQrhfa", "20220819-16-25-14")
# 测试

pip install spacetool, requests
import sys,os,json
pp2 = os.path.abspath(".")
sys.path.append(pp2)

from spacetool import main_tool
d = main_tool.DataTool(name="", code="", host="http://127.0.0.1:8000/")
to_handle_dir = "/Users/leo/Documents/data/test数据格式样本/紫横家园东区"
to_handle_dir = "/Users/leo/Documents/data/文洋大厦地下"
to_handle_dir = "/Users/leo/Documents/data/wly/文洋大厦地下"
car_p_ser_path = d.walk_dir(to_handle_dir)
res = d.handle_local()

from spacetool import main_tool
d = main_tool.DataTool(name="", code="", host="")
f = "/Users/leo/Downloads/追势数据4号盘.txt"
res = d.walk_log_file(f3)
res2 = d.walk_log_and_upload_info(f3)

f1 = "/Users/leo/Downloads/用所选项目新建的文件夹2/离线硬盘path地址/追势数据1号盘.txt"
f2 = "/Users/leo/Downloads/用所选项目新建的文件夹2/离线硬盘path地址/追势数据2号盘.txt"
f3 = "/Users/leo/Downloads/用所选项目新建的文件夹2/离线硬盘path地址/追势数据3号盘.txt"

f1 = "/var/www/data/追势数据1号盘.txt"
f2 = "/var/www/data/追势数据2号盘.txt"
f3 = "/var/www/data/追势数据3号盘.txt"

"""

"""

# 长期开发密钥
secret_id = ""
secret_key = ""
region = ""
bucket_name = ""
if_ever = True
token = None
from spacetool import main_tool
qcloud_handle_instance = main_tool.QCloudHandle(secret_id, secret_key, region, bucket_name, if_ever, token)
from ods_data.models import carparking_collection_record
carparking_collection_record_instances = carparking_collection_record.objects.filter(id__gte=6732, if_all_frame=True)
to_download_list = []
for carparking_collection_record_instance in carparking_collection_record_instances:
    to_download_list.append(f"data/{carparking_collection_record_instance.carparking.serial}-{carparking_collection_record_instance.serial}/")
for to_download_dir in to_download_list:
    qcloud_handle_instance.downLoadDirFromCos(to_download_dir, "/Users/leo/Documents/data/od-车辆/data0608/")
qcloud_handle_instance.downLoadDirFromCos("data/", "/Users/leo/Documents/data/od-车辆/data0517/")

"""

"""
qcloud 测试
if __name__ == "__main__":
    # 进入异步任务队列
    # 申请临时密钥, 默认1800秒, 一个case一个密钥
    # 初始化qcloud_tool
    # do some action

    # 长期开发密钥
    secret_id = ""
    secret_key = ""
    region = ""
    bucket_name = ""
    if_ever = True
    token = None
    qcloud_handle_instance = QCloudHandle(secret_id, secret_key, region, bucket_name, if_ever, token)
    qcloud_handle_instance.upload_file("/Users/leo/Downloads/SMC_天际PC.bin", "tmp/smc_tianji_pc_20230414.bin")  # /Users/leo/Downloads/SEED-Ubuntu20.04.zip
    # qcloud_handle_instance.upload_file("/Users/leo/Downloads/screenshot-20230413-114619.png", "tmp/screenshot-20230413-114619.png")  # /Users/leo/Downloads/SEED-Ubuntu20.04.zip
    # signed_download_url = qcloud_handle_instance.gen_file_download_url("tmp/screenshot-20230413-114619.png")
    # print(f"#### signed_download_url: {signed_download_url}")

    # # 临时密钥
    # response = get_credential_demo(secret_id, secret_key, region, bucket_name)
    tmp_secret_id = response['credentials']['tmpSecretId']
    tmp_secret_key = response['credentials']['tmpSecretKey']
    tmp_secret_token = response['credentials']['sessionToken']
    # if_ever = False
    qcloud_handle_instance = QCloudHandle(tmp_secret_id, tmp_secret_key, region, bucket_name, if_ever, tmp_secret_token)
    qcloud_handle_instance.upload_file("/Users/leo/Downloads/screenshot-20230324-151321.png", "tmp/screenshot-20230324-151321.png")  # /Users/leo/Downloads/SEED-Ubuntu20.04.zip
    # signed_download_url = qcloud_handle_instance.gen_file_download_url("tmp/screenshot-20230324-151321.png")
    # print(f"#### signed_download_url: {signed_download_url}")
    # response = requests.get(signed_download_url)
    # print(response)
    res = qcloud_handle_instance.list_objects("tmp/")
    # print(f"---res: {res}")
"""

"""


"""