import os
import logging
import requests
import subprocess
import time
import fnmatch
import json

from enum import Enum, unique
from datetime import datetime
from .utils import Singleton
from bytedance import servicediscovery
from random import randint
from requests.packages.urllib3.exceptions import InsecureRequestWarning

logger = logging.getLogger(__name__)
logging.getLogger("requests").setLevel(logging.CRITICAL)
logging.getLogger("urllib3").setLevel(logging.CRITICAL)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


# retry logic for post events
def retry_post(max_retries=3, max_wait_interval=10, period=1, rand=False):
    def _retry(func):
        def __retry(*args, **kwargs):
            MAX_RETRIES = max_retries
            MAX_WAIT_INTERVAL = max_wait_interval
            PERIOD = period
            RAND = rand

            retries = 0
            error = None
            while retries < MAX_RETRIES:
                try:
                    result = func(*args, **kwargs)
                    if "res" in result and result["res"]:
                        return result
                    elif "res" in result and not result["res"] and result["reason"] == "NOT_AVAILABLE":
                        return result
                    else:
                        pass
                except Exception as ex:
                    error = ex
                finally:
                    sleep_time = min(2 ** retries * PERIOD if not RAND else randint(0, 2 ** retries) * PERIOD,
                                     MAX_WAIT_INTERVAL)
                    time.sleep(sleep_time)
                    retries += 1
            if retries == MAX_RETRIES:
                pass
                # logger.error("retryed and still failed to post events to fratest. If it's local environemnt, it can be normal")

        return __retry

    return _retry


@unique
class EventType(Enum):
    # 整体运行信息 0-20
    PROJ_START = 1  # 整个项目运行 启动时间
    PROJ_END = 2  # 整个项目运行 结束时间
    TOTAL_NUM = 3  # 运行的Case总数
    SUCCESS_NUM = 4  # 运行成功的case数
    FAILED_NUM = 5  # 失败的case数
    XFAILED_NUM = 6  # 预见出错的Case
    SKIP_NUM = 7  # 跳过的case数
    SUCCESS_RATE = 8  # 成功率
    TEST_TYPE = 9  # 测试类型。 API or RPC
    PROJ_NAME = 10  # 项目名称
    REPO_NAME = 11  # repo名称
    TESLA_ID = 12  # tesla的仓库ID
    TESLA_PLAN_NAME = 13  # tesla计划名字
    TESLA_PLANID = 14  # tesla 计划id
    TESLA_TRIGGER_USER = 15  # tesla触发人
    FIRST_BUSINESS_LINE = 16  # 一级业务线
    SECOND_BUSINESS_LINE = 17  # 二级业务线
    THIRD_BUSINESS_LINE = 18  # 三级业务线
    PROJ_OWNER = 19  # owner人
    PROJ_DESCRIPTION = 20  # 描述

    # PSM 相关信息 21-40
    PSM_NAMES = 21  # PSM名字
    PSM_DESCRIPTION = 22  # PSM描述
    PSM_GDPR = 23  # 是否开启GDPR
    PSM_ENV = 24  # 执行环境
    PSM_IPPORT = 25  # ipport
    PSM_API_NUM = 26  # RPC拉取的接口数

    # 业务相关的信息 41-60
    CASE_NAME = 41  # Case的名字
    CASE_DESCRIPTION = 42  # CASE描述
    CASE_START = 43  # CASE执行时间
    CASE_END = 44  # CASE返回时间
    CASE_STATE = 45  # CASE执行成功、失败、SKIP
    CASE_FAILED_REASON = 46  # 失败原因
    CASE_PARAMS = 47  # 入参
    CASE_RESPONSE = 48  # 返回
    CASE_LOGID = 49  # 日志id
    CASE_DURATION = 50  # 耗时
    CASE_ENV = 51  # 执行环境
    CASE_LOGS = 52  # 执行日志

@unique
class StatisticType(Enum):
    BLACK_BOX_COVERAGE = 1
    INTERFACE_COVERAGE = 2

@Singleton
class EventCollect(object):
    def __init__(self):
        self.events = {}
        self.proj_events = {}
        self.psm_events = {}
        self.case_events = {}
        self.current_running_case = None
        self.collect_switch = True
        self.i18n_host_main = "https://fratest.byteintl.net"
        self.cn_host_main = "https://fratest-boe.byted.org"
        self.ttp_host_main = "https://fratest.tiktok-usts.org"
        self.local_folder = "."
        self.local_info_file = "fratest.json"
        self.local_info = {}

        self.not_collect_events = []
        self.initial_events()

    def initial_events(self):

        self.proj_events[EventType.PROJ_START.name] = "0"
        self.proj_events[EventType.PROJ_END.name] = "0"
        self.proj_events[EventType.TOTAL_NUM.name] = 0
        self.proj_events[EventType.SUCCESS_NUM.name] = 0
        self.proj_events[EventType.FAILED_NUM.name] = 0
        self.proj_events[EventType.XFAILED_NUM.name] = 0
        self.proj_events[EventType.SUCCESS_RATE.name] = "0"
        self.proj_events[EventType.TEST_TYPE.name] = "API"

        repo_name = self.get_current_repo_name() if self.get_env_value("tesla_repo_name",
                                                                       "") == "" else self.get_env_value(
            "tesla_repo_name", "")
        # init proj_name and repo_name to repo_name( if tesla_repo_name exists))
        self.proj_events[EventType.PROJ_NAME.name] = repo_name
        self.proj_events[EventType.REPO_NAME.name] = repo_name
        self.proj_events[EventType.TESLA_ID.name] = self.get_env_value("tesla_repo_id", 0)
        self.proj_events[EventType.TESLA_PLANID.name] = self.get_env_value("tesla_planid", 0)
        self.proj_events[EventType.TESLA_PLAN_NAME.name] = self.get_env_value("tesla_plan_name", "")
        self.proj_events[EventType.TESLA_TRIGGER_USER.name] = self.get_env_value("tesla_trigger_user", "")

        self.proj_events[EventType.FIRST_BUSINESS_LINE.name] = ""
        self.proj_events[EventType.SECOND_BUSINESS_LINE.name] = ""
        self.proj_events[EventType.THIRD_BUSINESS_LINE.name] = ""
        self.proj_events[EventType.PROJ_OWNER.name] = []
        self.proj_events[EventType.PROJ_DESCRIPTION.name] = ""

        self.psm_events[EventType.PSM_ENV.name] = "prod"
        self.psm_events[EventType.PSM_DESCRIPTION.name] = ""
        self.psm_events[EventType.PSM_GDPR.name] = "FALSE"
        self.psm_events[EventType.PSM_IPPORT.name] = "0"
        self.psm_events[EventType.PSM_API_NUM.name] = 0
        self.psm_events[EventType.PSM_NAMES.name] = []

    def initial_fratest_info(self):
        self.get_proj_info_from_local()

        if "PROJ_NAME" in self.local_info:
            self.not_collect_events.append(EventType.PROJ_NAME)
            self.proj_events[EventType.PROJ_NAME.name] = self.local_info["PROJ_NAME"]

        BUSINESS_LINE_INFO = self.local_info.get("BUSINESS_LINE", {})

        self.proj_events[EventType.FIRST_BUSINESS_LINE.name] = BUSINESS_LINE_INFO.get("FIRST_BUSINESS_LINE", "")
        self.proj_events[EventType.SECOND_BUSINESS_LINE.name] = BUSINESS_LINE_INFO.get("SECOND_BUSINESS_LINE", "")
        self.proj_events[EventType.THIRD_BUSINESS_LINE.name] = BUSINESS_LINE_INFO.get("THIRD_BUSINESS_LINE", "")

        if "PSM_NAMES" in self.local_info:
            self.not_collect_events.append(EventType.PSM_NAMES)
            self.psm_events[EventType.PSM_NAMES.name] = self.local_info.get("PSM_NAMES", [])

        self.proj_events[EventType.PROJ_OWNER.name] = self.local_info.get("PROJ_OWNER", [])
        self.proj_events[EventType.PROJ_DESCRIPTION.name] = self.local_info.get("PROJ_DESCRIPTION", "")

    # collect project psm case infos
    def collect_event(self, event_type: EventType, event_value=None):
        if not self.collect_switch and event_type in self.not_collect_events:
            return
        # print("collect event : {0} value : {1}".format(event_type.name, event_value))
        if 1 <= event_type.value <= 20:
            # proj events

            self.proj_events[event_type.name] = event_value
            if event_type == EventType.PROJ_START or event_type == EventType.PROJ_END:
                self.proj_events[event_type.name] = self.get_current_time()

        elif 21 <= event_type.value <= 40:
            # psm events
            if event_type == EventType.PSM_NAMES:
                if event_value not in self.psm_events[event_type.name]:
                    self.psm_events[event_type.name].append(event_value)
            else:
                self.psm_events[event_type.name] = event_value

        # case events
        elif 41 <= event_type.value <= 60:
            # case events
            if self.current_running_case is None:
                return

            if self.current_running_case not in self.case_events:
                self.case_events[self.current_running_case] = {}

            if event_type.name not in self.case_events[self.current_running_case]:
                self.case_events[self.current_running_case][event_type.name] = event_value

            else:
                if event_value == "FAILED" and event_type == EventType.CASE_STATE:
                    self.case_events[self.current_running_case][event_type.name] = event_value

            if event_type == EventType.CASE_START or event_type == EventType.CASE_END:
                self.case_events[self.current_running_case][event_type.name] = self.get_current_time()

        else:
            self.events[event_type.name] = event_value

    def set_current_running_case(self, case_name):
        self.current_running_case = case_name
        self.collect_event(EventType.CASE_NAME, case_name)

    def set_collect_switch(self, flag: bool):
        self.collect_switch = flag

    def send_events(self):
        if not self.collect_switch:
            logger.info("not collect events")
            return

        event_data_dict = {
            "proj_info": self.proj_events,
            "psm_info": self.psm_events,
            "case_info": self.case_events
        }

        self.post_events(event_data_dict)

    def get_current_time(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return current_time

    def get_current_repo_name(self):
        repo = ""
        try:
            output = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'])
            repo = os.path.basename(output).decode("utf-8").strip().replace("\n", "")
        except:
            logger.error("running git command failed")

        return repo

    def get_env_value(self, env_key, default_value):
        env_value = default_value
        try:
            env_value = os.environ.get(env_key)
        except:
            pass

        if env_value is None:
            return default_value
        else:
            return env_value

    def set_local_folder(self, local_folder):
        self.local_folder = local_folder

    def search_file_path(self):

        def iterfindfiles(path, fnexp):
            for root, dirs, files in os.walk(path):
                for filename in fnmatch.filter(files, fnexp):
                    yield os.path.join(root, filename)

        cur_path = os.path.abspath(os.getcwd())
        local_folder_path = os.path.abspath(self.local_folder)
        local_info_file_path = ""
        count = 0
        if local_folder_path == cur_path:
            for filename in iterfindfiles(local_folder_path, self.local_info_file):
                local_info_file_path = filename
                return local_info_file_path
        else:
            while local_folder_path != cur_path and count <= 5:
                local_folder_path = os.path.abspath(os.path.dirname(local_folder_path))
                for filename in iterfindfiles(local_folder_path, self.local_info_file):
                    local_info_file_path = filename
                    return local_info_file_path

                count += 1

        return local_info_file_path

    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            pass

        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass

        return False

    def get_proj_info_from_local(self):
        local_info_file_path = self.search_file_path()

        if local_info_file_path != "" and os.path.exists(local_info_file_path):
            with open(local_info_file_path) as local_info_file_json:
                self.local_info = json.load(local_info_file_json)

    def read_functions_from_thrift(self, idl_path):
        functions = []
        if os.path.exists(idl_path):
            start = 0
            with open(idl_path, 'r') as f:
                all_lines = f.readlines()
                for i in range(len(all_lines)):
                    the_line = all_lines[i].strip()
                    if the_line.startswith("service"):
                        start = i
                    if start > 0 and start != i and the_line != "}" and the_line != "" and the_line != "{":
                        functions.append(the_line)

        return functions

    def get_fratest_ip_port(self):
        # service discover
        service_info = None
        psm = "ad.qa.fratest"
        try:
            service_info = servicediscovery.lookup(psm)
            try:
                pinfo = '{:>15}  {:>5}  {:>20}  {:>20}'.format('Host', 'Port', 'env', 'cluster')
                for info in self.service_info:
                    pinfo += '\n{Host:>15}  {Port:>5}  {Tags[env]:>20}  {Tags[cluster]:>20}'.format(**info)
                logger.debug('%s service info=\n%s', self.psm, pinfo)
            except Exception as e:
                logger.error(e)
        except Exception as e:
            service_info = None
            logger.error(
                "{0} service not found. so the statistic data will not be collect. but not affect the test!".format(
                    psm))
            # logger.exception('{} service discover failed: {}'.format(psm, e))

        if service_info is None:
            return None, None
        service_ip = service_info[0]["Host"]
        service_port = service_info[0]["Port"]

        return service_ip, service_port

    def get_host_domain(self):
        i18n_flag = True
        cn_flag = True
        try:
            response = requests.get(self.i18n_host_main, timeout=5, verify=False)
        except requests.exceptions.RequestException:
            i18n_flag = False

        if i18n_flag:
            return self.i18n_host_main

        try:
            response = requests.get(self.cn_host_main, timeout=5, verify=False)
        except requests.exceptions.RequestException:
            cn_flag = False

        if cn_flag:
            return self.cn_host_main
        else:
            return self.ttp_host_main

    @retry_post()
    def post_events(self, event_data_dict):
        post_url_path = "{0}/collect_events/".format(self.get_host_domain())

        headers = {'content-type': 'application/json'}

        response = requests.post(post_url_path, data=json.dumps(event_data_dict), headers=headers)

        try:
            response_json = json.loads(response.text)
        except Exception as ex:
            pass
        finally:
            return response_json

    def post_statistics_data(self, first_business_line="", second_business_line="", third_business_line="", psm_name="", owner="", statistic_type: StatisticType= StatisticType.BLACK_BOX_COVERAGE, statistic_value=None):
        if statistic_value is None:
            logger.error("{0}'s value is None.".format(statistic_type.name))
            return

        statistic_dict = {
            "FIRST_BUSINESS_LINE": first_business_line,
            "SECOND_BUSINESS_LINE": second_business_line,
            "THIRD_BUSINESS_LINE": third_business_line,
            "PSM_NAME": psm_name,
            "OWNER": owner,
        }

        if statistic_type == StatisticType.BLACK_BOX_COVERAGE:
            if not self.is_number(statistic_value):
                logger.error("{0} need to be a number".format(statistic_value))
                return

            statistic_dict["BLACK_BOX_COVERAGE"] = statistic_value

        if statistic_type == StatisticType.INTERFACE_COVERAGE:
            if not self.is_number(statistic_value):
                logger.error("{0} need to be a number".format(statistic_value))
                return

            statistic_dict["INTERFACE_COVERAGE"] = statistic_value

        post_url_path = "{0}/collect_statistic/".format(self.get_host_domain())
        headers = {'content-type': 'application/json'}
        response = requests.post(post_url_path, data=json.dumps(statistic_dict), headers=headers)

        try:
            response_json = json.loads(response.text)
        except Exception as ex:
            pass
        finally:
            return response_json


EventCollecter = EventCollect()
