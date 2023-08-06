import datetime
import hashlib
import logging
import time
import urllib.parse
from typing import cast

import requests as requests

from saic_ismart_client.common_model import MessageV2, MessageBodyV2, Header, AbstractMessageBody, AbstractMessage
from saic_ismart_client.ota_v1_1.Message import MessageCoderV11
from saic_ismart_client.ota_v1_1.data_model import VinInfo, MpUserLoggingInReq, MpUserLoggingInRsp, AlarmSwitchReq, \
    MpAlarmSettingType, AlarmSwitch, MessageBodyV11, MessageV11, MessageListReq, StartEndNumber, MessageListResp, \
    Timestamp, Message, AbortSendMessageReq
from saic_ismart_client.ota_v2_1.Message import MessageCoderV21
from saic_ismart_client.ota_v2_1.data_model import OtaRvmVehicleStatusReq, OtaRvmVehicleStatusResp25857, OtaRvcReq,\
    RvcReqParam, OtaRvcStatus25857
from saic_ismart_client.ota_v3_0.Message import MessageCoderV30, MessageV30, MessageBodyV30
from saic_ismart_client.ota_v3_0.data_model import OtaChrgMangDataResp

UID_INIT = '0000000000000000000000000000000000000000000000000#'
AVG_SMS_DELIVERY_TIME = 15
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)


class SaicMessage:
    def __init__(self, message_id: int, message_type: str, title: str, message_time: datetime, sender: str,
                 content: str, read_status: int, vin: str):
        self.message_id = message_id
        self.message_type = message_type
        self.title = title
        self.message_time = message_time
        self.sender = sender
        self.content = content
        self.read_status = read_status
        self.vin = vin

    def get_read_status_str(self) -> str:
        if self.read_status is None:
            return 'unknown'
        elif self.read_status == 0:
            return 'unread'
        else:
            return 'read'

    def get_details(self) -> str:
        return f'ID: {self.message_id}, Time: {self.message_time}, Type: {self.message_type}, Title: {self.title}, '\
            + f'Content: {self.content}, Status: {self.get_read_status_str()}, Sender: {self.sender}, VIN: {self.vin}'


def convert(message: Message) -> SaicMessage:
    if message.content is not None:
        content = message.content.decode()
    else:
        content = None
    return SaicMessage(message.message_id, message.message_type, message.title.decode(),
                       message.message_time.get_timestamp(), message.sender.decode(), content, message.read_status,
                       message.vin)


class SaicApiException(Exception):
    def __init__(self, msg: str, return_code: int = None):
        if return_code is not None:
            self.message = f'return code: {return_code}, message: {msg}'
        else:
            self.message = msg

    def __str__(self):
        return self.message


class SaicApi:
    def __init__(self, saic_uri: str, saic_user: str, saic_password: str, relogin_delay: int = None):
        self.saic_uri = saic_uri
        self.saic_user = saic_user
        self.saic_password = saic_password
        if relogin_delay is None:
            self.relogin_delay = 0
        else:
            self.relogin_delay = relogin_delay
        self.message_v1_1_coder = MessageCoderV11()
        self.message_V2_1_coder = MessageCoderV21()
        self.message_V3_0_coder = MessageCoderV30()
        self.cookies = None
        self.uid = ''
        self.token = ''
        self.token_expiration = None
        self.on_publish_raw_value = None
        self.on_publish_json_value = None

    def login(self) -> MessageV11:
        application_data = MpUserLoggingInReq()
        application_data.password = self.saic_password
        header = Header()
        header.protocol_version = 17
        login_request_message = MessageV11(header, MessageBodyV11(), application_data)
        application_id = '501'
        application_data_protocol_version = 513
        self.message_v1_1_coder.initialize_message(
            UID_INIT[len(self.saic_user):] + self.saic_user,
            cast(str, None),
            application_id,
            application_data_protocol_version,
            1,
            login_request_message)
        self.publish_json_request(application_id, application_data_protocol_version, login_request_message.get_data())
        login_request_hex = self.message_v1_1_coder.encode_request(login_request_message)
        self.publish_raw_request(application_id, application_data_protocol_version, login_request_hex)
        login_response_hex = self.send_request(login_request_hex,
                                               urllib.parse.urljoin(self.saic_uri, '/TAP.Web/ota.mp'))
        self.publish_raw_response(application_id, application_data_protocol_version, login_response_hex)
        logging_in_rsp = MpUserLoggingInRsp()
        login_response_message = MessageV11(header, MessageBodyV11(), logging_in_rsp)
        self.message_v1_1_coder.decode_response(login_response_hex, login_response_message)
        self.publish_json_response(application_id, application_data_protocol_version, login_response_message.get_data())
        if login_response_message.body.error_message is not None:
            raise SaicApiException(login_response_message.body.error_message.decode(),
                                   login_response_message.body.result)
        else:
            self.uid = login_response_message.body.uid
            self.token = logging_in_rsp.token
            if logging_in_rsp.token_expiration is not None:
                self.token_expiration = logging_in_rsp.token_expiration
        return login_response_message

    def set_alarm_switches(self, alarm_switches: list) -> None:
        alarm_switch_req = AlarmSwitchReq()
        alarm_switch_req.alarm_switch_list = alarm_switches
        alarm_switch_req.pin = hash_md5('123456')

        header = Header()
        header.protocol_version = 17
        alarm_switch_req_message = MessageV11(header, MessageBodyV11(), alarm_switch_req)
        application_id = '521'
        application_data_protocol_version = 513
        self.message_v1_1_coder.initialize_message(
            self.uid,
            self.get_token(),
            application_id,
            application_data_protocol_version,
            1,
            alarm_switch_req_message)
        self.publish_json_request(application_id, application_data_protocol_version,
                                  alarm_switch_req_message.get_data())
        alarm_switch_request_hex = self.message_v1_1_coder.encode_request(alarm_switch_req_message)
        self.publish_raw_request(application_id, application_data_protocol_version, alarm_switch_request_hex)
        alarm_switch_response_hex = self.send_request(alarm_switch_request_hex,
                                                      urllib.parse.urljoin(self.saic_uri, '/TAP.Web/ota.mp'))
        self.publish_raw_response(application_id, application_data_protocol_version, alarm_switch_response_hex)
        alarm_switch_response_message = MessageV11(header, MessageBodyV11())
        self.message_v1_1_coder.decode_response(alarm_switch_response_hex, alarm_switch_response_message)
        self.publish_json_response(application_id, application_data_protocol_version,
                                   alarm_switch_response_message.get_data())

        if alarm_switch_response_message.body.error_message is not None:
            raise SaicApiException(alarm_switch_response_message.body.error_message.decode(),
                                   alarm_switch_response_message.body.result)

    def get_vehicle_status(self, vin_info: VinInfo, event_id: str = None) -> MessageV2:
        vehicle_status_req = OtaRvmVehicleStatusReq()
        vehicle_status_req.veh_status_req_type = 2
        vehicle_status_req_msg = MessageV2(MessageBodyV2(), vehicle_status_req)
        application_id = '511'
        application_data_protocol_version = 25857
        self.message_V2_1_coder.initialize_message(self.uid, self.get_token(), vin_info.vin, application_id,
                                                   application_data_protocol_version, 1, vehicle_status_req_msg)
        if event_id is not None:
            vehicle_status_req_msg.body.event_id = event_id
        self.publish_json_request(application_id, application_data_protocol_version, vehicle_status_req_msg.get_data())
        vehicle_status_req_hex = self.message_V2_1_coder.encode_request(vehicle_status_req_msg)
        self.publish_raw_request(application_id, application_data_protocol_version, vehicle_status_req_hex)
        vehicle_status_rsp_hex = self.send_request(vehicle_status_req_hex,
                                                   urllib.parse.urljoin(self.saic_uri, '/TAP.Web/ota.mpv21'))
        self.publish_raw_response(application_id, application_data_protocol_version, vehicle_status_rsp_hex)
        vehicle_status_rsp_msg = MessageV2(MessageBodyV2(), OtaRvmVehicleStatusResp25857())
        self.message_V2_1_coder.decode_response(vehicle_status_rsp_hex, vehicle_status_rsp_msg)
        self.publish_json_response(application_id, application_data_protocol_version, vehicle_status_rsp_msg.get_data())
        return vehicle_status_rsp_msg

    def get_vehicle_status_with_retry(self, vin_info: VinInfo) -> MessageV2:
        return self.handle_retry(self.get_vehicle_status, vin_info)

    def lock_vehicle(self, vin_info: VinInfo) -> MessageV2:
        rvc_params = []
        return self.send_vehicle_ctrl_cmd_with_retry(vin_info, b'\x01', rvc_params, False)

    def unlock_vehicle(self, vin_info: VinInfo) -> MessageV2:
        rvc_params = []
        param1 = RvcReqParam()
        param1.param_id = 4
        param1.param_value = b'\x00'
        rvc_params.append(param1)

        param2 = RvcReqParam()
        param2.param_id = 5
        param2.param_value = b'\x00'
        rvc_params.append(param2)

        param3 = RvcReqParam()
        param3.param_id = 6
        param3.param_value = b'\x00'
        rvc_params.append(param3)

        param4 = RvcReqParam()
        param4.param_id = 7
        param4.param_value = b'\x03'
        rvc_params.append(param4)

        param5 = RvcReqParam()
        param5.param_id = 255
        param5.param_value = b'\x00'
        rvc_params.append(param5)

        return self.send_vehicle_ctrl_cmd_with_retry(vin_info, b'\x02', rvc_params, False)

    def start_rear_window_heat(self, vin_info: VinInfo) -> MessageV2:
        rvc_params = []
        param1 = RvcReqParam()
        param1.param_id = 23
        param1.param_value = b'\x01'
        rvc_params.append(param1)

        param2 = RvcReqParam()
        param2.param_id = 255
        param2.param_value = b'\x00'
        rvc_params.append(param2)

        return self.send_vehicle_ctrl_cmd_with_retry(vin_info, b'\x20', rvc_params, False)

    def stop_rear_window_heat(self, vin_info: VinInfo) -> MessageV2:
        rvc_params = []
        param1 = RvcReqParam()
        param1.param_id = 23
        param1.param_value = b'\x00'
        rvc_params.append(param1)

        param2 = RvcReqParam()
        param2.param_id = 255
        param2.param_value = b'\x00'
        rvc_params.append(param2)

        return self.send_vehicle_ctrl_cmd_with_retry(vin_info, b'\x20', rvc_params, False)

    def start_ac(self, vin_info: VinInfo) -> MessageV2:
        rcv_params = []
        param1 = RvcReqParam()
        param1.param_id = 19
        param1.param_value = b'\x02'
        rcv_params.append(param1)

        param2 = RvcReqParam()
        param2.param_id = 20
        param2.param_value = b'\x08'
        rcv_params.append(param2)

        param3 = RvcReqParam()
        param3.param_id = 255
        param3.param_value = b'\x00'
        rcv_params.append(param3)

        return self.send_vehicle_ctrl_cmd_with_retry(vin_info, b'\x06', rcv_params, True)

    def stop_ac(self, vin_info: VinInfo) -> MessageV2:
        rcv_params = []
        param1 = RvcReqParam()
        param1.param_id = 19
        param1.param_value = b'\x00'
        rcv_params.append(param1)

        param2 = RvcReqParam()
        param2.param_id = 20
        param2.param_value = b'\x00'
        rcv_params.append(param2)

        param3 = RvcReqParam()
        param3.param_id = 255
        param3.param_value = b'\x00'
        rcv_params.append(param3)

        return self.send_vehicle_ctrl_cmd_with_retry(vin_info, b'\x06', rcv_params, True)

    def start_ac_blowing(self, vin_info: VinInfo) -> MessageV2:
        rcv_params = []
        param1 = RvcReqParam()
        param1.param_id = 19
        param1.param_value = b'\x01'
        rcv_params.append(param1)

        param2 = RvcReqParam()
        param2.param_id = 20
        param2.param_value = b'\x00'
        rcv_params.append(param2)

        param3 = RvcReqParam()
        param3.param_id = 22
        param3.param_value = b'\x01'
        rcv_params.append(param3)

        param4 = RvcReqParam()
        param4.param_id = 255
        param4.param_value = b'\x00'
        rcv_params.append(param4)

        return self.send_vehicle_ctrl_cmd_with_retry(vin_info, b'\x06', rcv_params, True)

    def stop_ac_blowing(self, vin_info: VinInfo) -> MessageV2:
        rcv_params = []
        param1 = RvcReqParam()
        param1.param_id = 19
        param1.param_value = b'\x00'
        rcv_params.append(param1)

        param2 = RvcReqParam()
        param2.param_id = 20
        param2.param_value = b'\x00'
        rcv_params.append(param2)

        param3 = RvcReqParam()
        param3.param_id = 22
        param3.param_value = b'\x00'
        rcv_params.append(param3)

        param4 = RvcReqParam()
        param4.param_id = 255
        param4.param_value = b'\x00'
        rcv_params.append(param4)

        return self.send_vehicle_ctrl_cmd_with_retry(vin_info, b'\x06', rcv_params, True)

    def start_front_defrost(self, vin_info: VinInfo) -> MessageV2:
        rcv_params = []
        param1 = RvcReqParam()
        param1.param_id = 19
        param1.param_value = b'\x05'
        rcv_params.append(param1)

        param2 = RvcReqParam()
        param2.param_id = 20
        param2.param_value = b'\x08'
        rcv_params.append(param2)

        param3 = RvcReqParam()
        param3.param_id = 22
        param3.param_value = b'\x01'
        rcv_params.append(param3)

        param4 = RvcReqParam()
        param4.param_id = 255
        param4.param_value = b'\x00'
        rcv_params.append(param4)

        return self.send_vehicle_ctrl_cmd_with_retry(vin_info, b'\x06', rcv_params, True)

    def stop_front_defrost(self, vin_info: VinInfo) -> MessageV2:
        rcv_params = []
        param1 = RvcReqParam()
        param1.param_id = 19
        param1.param_value = b'\x00'
        rcv_params.append(param1)

        param2 = RvcReqParam()
        param2.param_id = 20
        param2.param_value = b'\x08'
        rcv_params.append(param2)

        param3 = RvcReqParam()
        param3.param_id = 22
        param3.param_value = b'\x00'
        rcv_params.append(param3)

        param4 = RvcReqParam()
        param4.param_id = 255
        param4.param_value = b'\x00'
        rcv_params.append(param4)

        return self.send_vehicle_ctrl_cmd_with_retry(vin_info, b'\x06', rcv_params, True)

    def send_vehicle_ctrl_cmd_with_retry(self, vin_info: VinInfo, rvc_req_type: bytes, rvc_params: list,
                                         has_app_data: bool) -> MessageV2:
        vehicle_control_cmd_rsp_msg = self.send_vehicle_control_command(vin_info, rvc_req_type, rvc_params)

        if has_app_data:
            while vehicle_control_cmd_rsp_msg.application_data is None:
                if vehicle_control_cmd_rsp_msg.body.error_message is not None:
                    self.handle_error(vehicle_control_cmd_rsp_msg.body)
                else:
                    logging.debug('API request returned no application data and no error message.')
                    time.sleep(float(AVG_SMS_DELIVERY_TIME))

                event_id = vehicle_control_cmd_rsp_msg.body.event_id
                vehicle_control_cmd_rsp_msg = self.send_vehicle_control_command(vin_info, rvc_req_type, rvc_params,
                                                                                event_id)
        else:
            retry = 1
            while(
                vehicle_control_cmd_rsp_msg.body.error_message is not None
                and retry <= 3
            ):
                self.handle_error(vehicle_control_cmd_rsp_msg.body)
                event_id = vehicle_control_cmd_rsp_msg.body.event_id
                vehicle_control_cmd_rsp_msg = self.send_vehicle_control_command(vin_info, rvc_req_type, rvc_params,
                                                                                event_id)
                retry += 1
            if vehicle_control_cmd_rsp_msg.body.error_message is not None:
                raise SaicApiException(vehicle_control_cmd_rsp_msg.body.error_message.decode(),
                                       vehicle_control_cmd_rsp_msg.body.result)
        return vehicle_control_cmd_rsp_msg

    def get_message_list_with_retry(self) -> list:
        message_list_rsp_msg = self.handle_retry(self.get_message_list)

        result = []
        if message_list_rsp_msg.application_data is not None:
            message_list_rsp = cast(MessageListResp, message_list_rsp_msg.application_data)
            for message in message_list_rsp.messages:
                result.append(convert(message))
        return result

    def handle_retry(self, func, vin_info: VinInfo = None):
        if vin_info:
            rsp = func(vin_info)
        else:
            rsp = func()
        rsp_msg = cast(AbstractMessage, rsp)
        while rsp_msg.application_data is None:
            if rsp_msg.body.error_message is not None:
                self.handle_error(rsp_msg.body)
            else:
                logging.debug('API request returned no application data and no error message.')
                time.sleep(float(AVG_SMS_DELIVERY_TIME))

            if vin_info:
                rsp_msg = func(vin_info, rsp_msg.body.event_id)
            else:
                rsp_msg = func(rsp_msg.body.event_id)
        return rsp_msg

    def send_vehicle_control_command(self, vin_info: VinInfo, rvc_req_type: bytes, rvc_params: list,
                                     event_id: str = None) -> MessageV2:
        vehicle_control_req = OtaRvcReq()
        vehicle_control_req.rvc_req_type = rvc_req_type
        for p in rvc_params:
            param = cast(RvcReqParam, p)
            vehicle_control_req.rvc_params.append(param)

        vehicle_control_cmd_req_msg = MessageV2(MessageBodyV2(), vehicle_control_req)
        application_id = '510'
        application_data_protocol_version = 25857
        self.message_V2_1_coder.initialize_message(self.uid, self.get_token(), vin_info.vin, application_id,
                                                   application_data_protocol_version, 1, vehicle_control_cmd_req_msg)
        vehicle_control_cmd_req_msg.body.ack_required = False
        if event_id is not None:
            vehicle_control_cmd_req_msg.body.event_id = event_id
        self.publish_json_request(application_id, application_data_protocol_version,
                                  vehicle_control_cmd_req_msg.get_data())
        vehicle_control_cmd_req_msg_hex = self.message_V2_1_coder.encode_request(vehicle_control_cmd_req_msg)
        self.publish_raw_request(application_id, application_data_protocol_version, vehicle_control_cmd_req_msg_hex)
        vehicle_control_cmd_rsp_msg_hex = self.send_request(vehicle_control_cmd_req_msg_hex,
                                                            urllib.parse.urljoin(self.saic_uri, '/TAP.Web/ota.mpv21'))
        self.publish_raw_response(application_id, application_data_protocol_version, vehicle_control_cmd_rsp_msg_hex)
        vehicle_control_cmd_rsp_msg = MessageV2(MessageBodyV2(), OtaRvcStatus25857())
        self.message_V2_1_coder.decode_response(vehicle_control_cmd_rsp_msg_hex, vehicle_control_cmd_rsp_msg)
        self.publish_json_response(application_id, application_data_protocol_version,
                                   vehicle_control_cmd_rsp_msg.get_data())
        return vehicle_control_cmd_rsp_msg

    def get_charging_status(self, vin_info: VinInfo, event_id: str = None) -> MessageV30:
        chrg_mgmt_data_req_msg = MessageV30(MessageBodyV30())
        application_id = '516'
        application_data_protocol_version = 768
        self.message_V3_0_coder.initialize_message(self.uid, self.get_token(), vin_info.vin, application_id,
                                                   application_data_protocol_version, 5, chrg_mgmt_data_req_msg)
        if event_id is not None:
            chrg_mgmt_data_req_msg.body.event_id = event_id
        self.publish_json_request(application_id, application_data_protocol_version, chrg_mgmt_data_req_msg.get_data())
        chrg_mgmt_data_req_hex = self.message_V3_0_coder.encode_request(chrg_mgmt_data_req_msg)
        self.publish_raw_request(application_id, application_data_protocol_version, chrg_mgmt_data_req_hex)
        chrg_mgmt_data_rsp_hex = self.send_request(chrg_mgmt_data_req_hex,
                                                   urllib.parse.urljoin(self.saic_uri, '/TAP.Web/ota.mpv30'))
        self.publish_raw_response(application_id, application_data_protocol_version, chrg_mgmt_data_rsp_hex)
        chrg_mgmt_data_rsp_msg = MessageV30(MessageBodyV30(), OtaChrgMangDataResp())
        self.message_V3_0_coder.decode_response(chrg_mgmt_data_rsp_hex, chrg_mgmt_data_rsp_msg)
        self.publish_json_response(application_id, application_data_protocol_version, chrg_mgmt_data_rsp_msg.get_data())
        return chrg_mgmt_data_rsp_msg

    def get_charging_status_with_retry(self, vin_info: VinInfo) -> MessageV30:
        return self.handle_retry(self.get_charging_status, vin_info)

    def get_message_list(self, event_id: str = None) -> MessageV11:
        message_list_request = MessageListReq()
        message_list_request.start_end_number = StartEndNumber()
        message_list_request.start_end_number.start_number = 1
        message_list_request.start_end_number.end_number = 5
        message_list_request.message_group = 'ALARM'

        header = Header()
        header.protocol_version = 18
        message_body = MessageBodyV11()
        message_list_req_msg = MessageV11(header, message_body, message_list_request)
        application_id = '531'
        application_data_protocol_version = 513
        self.message_v1_1_coder.initialize_message(self.uid, self.get_token(), application_id,
                                                   application_data_protocol_version, 1, message_list_req_msg)
        if event_id is not None:
            message_body.event_id = event_id
        self.publish_json_request(application_id, application_data_protocol_version, message_list_req_msg.get_data())
        message_list_req_hex = self.message_v1_1_coder.encode_request(message_list_req_msg)
        self.publish_raw_request(application_id, application_data_protocol_version, message_list_req_hex)
        message_list_rsp_hex = self.send_request(message_list_req_hex,
                                                 urllib.parse.urljoin(self.saic_uri, '/TAP.Web/ota.mp'))
        self.publish_raw_response(application_id, application_data_protocol_version, message_list_rsp_hex)
        message_list_rsp_msg = MessageV11(header, MessageBodyV11(), MessageListResp())
        self.message_v1_1_coder.decode_response(message_list_rsp_hex, message_list_rsp_msg)
        self.publish_json_response(application_id, application_data_protocol_version, message_list_rsp_msg.get_data())
        return message_list_rsp_msg

    def delete_message(self, message_id: int, event_id: str = None) -> None:
        abort_send_msg_req = AbortSendMessageReq()
        abort_send_msg_req.action_type = 'DELETE'
        abort_send_msg_req.message_id = message_id

        header = Header()
        header.protocol_version = 17
        message_body = MessageBodyV11()
        message_delete_req_msg = MessageV11(header, message_body, abort_send_msg_req)
        application_id = '615'
        application_protocol_version = 513
        self.message_v1_1_coder.initialize_message(self.uid, self.get_token(), application_id,
                                                   application_protocol_version, 1, message_delete_req_msg)
        if event_id is not None:
            message_body.event_id = event_id
        self.publish_json_request(application_id, application_protocol_version, abort_send_msg_req.get_data())
        message_delete_req_hex = self.message_v1_1_coder.encode_request(message_delete_req_msg)
        self.publish_raw_request(application_id, application_protocol_version, message_delete_req_hex)
        message_delete_rsp_hex = self.send_request(message_delete_req_hex,
                                                   urllib.parse.urljoin(self.saic_uri, '/TAP.Web/ota.mp'))
        self.publish_raw_response(application_id, application_protocol_version, message_delete_rsp_hex)
        message_delete_rsp_msg = MessageV11(header, MessageBodyV11())
        self.message_v1_1_coder.decode_response(message_delete_rsp_hex, message_delete_rsp_msg)
        self.publish_json_response(application_id, application_protocol_version, message_delete_rsp_msg.get_data())
        if message_delete_rsp_msg.body.error_message is not None:
            raise SaicApiException(message_delete_rsp_msg.body.error_message.decode(),
                                   message_delete_rsp_msg.body.result)

    def publish_raw_value(self, key: str, raw: str):
        if self.on_publish_raw_value is not None:
            self.on_publish_raw_value(key, raw)
        else:
            logging.debug(f'{key}: {raw}')

    def publish_raw_request(self, application_id: str, application_data_protocol_version: int, raw: str):
        key = f'{application_id}_{application_data_protocol_version}/raw/request'
        self.publish_raw_value(key, raw)

    def publish_raw_response(self, application_id: str, application_data_protocol_version: int, raw: str):
        key = f'{application_id}_{application_data_protocol_version}/raw/response'
        self.publish_raw_value(key, raw)

    def publish_json_request(self, application_id: str, application_data_protocol_version: int, data: dict):
        key = f'{application_id}_{application_data_protocol_version}/json/request'
        self.publish_json(key, data)

    def publish_json_response(self, application_id: str, application_data_protocol_version: int, data: dict):
        key = f'{application_id}_{application_data_protocol_version}/json/response'
        self.publish_json(key, data)

    def publish_json(self, key: str, data: dict):
        if self.on_publish_json_value is not None:
            self.on_publish_json_value(key, data)
        else:
            logging.debug(f'{key}: {data}')

    def send_request(self, hex_message: str, endpoint) -> str:
        headers = {
            'Accept': '*/*',
            'Content-Type': 'text/html',
            'Accept-Encoding': 'gzip, deflate, br',
            'User-Agent': 'MG iSMART/1.1.1 (iPhone; iOS 16.3; Scale/3.00)',
            'Accept-Language': 'de-DE;q=1, en-DE;q=0.9, lu-DE;q=0.8, fr-DE;q=0.7',
            'Content-Length': str(len(hex_message))
        }
        try:
            response = requests.post(url=endpoint, data=hex_message, headers=headers, cookies=self.cookies)
            self.cookies = response.cookies
            return response.content.decode()
        except requests.exceptions.ConnectionError as ece:
            raise SaicApiException(f'Connection error: {ece}')
        except requests.exceptions.Timeout as et:
            raise SaicApiException(f'Timeout error: {et}')
        except requests.exceptions.HTTPError as ehttp:
            status_code = ehttp.response.status_code
            raise SaicApiException(f'HTTP error. HTTP status: {status_code}, {ehttp}')
        except requests.exceptions.RequestException as e:
            raise SaicApiException(f'{e}')

    def get_token(self):
        if self.token_expiration is not None:
            token_expiration = cast(Timestamp, self.token_expiration)
            if token_expiration.get_timestamp() < datetime.datetime.now():
                self.login()
        return self.token

    def handle_error(self, message_body: AbstractMessageBody):
        message = f'application ID: {message_body.application_id},'\
              + f' protocol version: {message_body.application_data_protocol_version},'\
              + f' message: {message_body.error_message.decode()}'\
              + f' result code: {message_body.result}'

        if message_body.result == 2:
            # re-login
            logging.debug(message)
            if self.relogin_delay > 0:
                logging.warning(f'The SAIC user has been logged out. '
                                + f'Waiting {self.relogin_delay} seconds before attempting another login')
                time.sleep(float(self.relogin_delay))
            self.login()
        elif message_body.result == 4:
            # please try again later
            logging.debug(message)
            time.sleep(float(AVG_SMS_DELIVERY_TIME))
        elif message_body.result == -1:
            logging.warning(message)
        else:
            logging.error(message)


def hash_md5(password: str) -> str:
    return hashlib.md5(password.encode('utf-8')).hexdigest()


def create_alarm_switch(alarm_setting_type: MpAlarmSettingType) -> AlarmSwitch:
    alarm_switch = AlarmSwitch()
    alarm_switch.alarm_setting_type = alarm_setting_type.value
    alarm_switch.alarm_switch = True
    alarm_switch.function_switch = True
    return alarm_switch
