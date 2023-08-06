# coding: utf-8
#

import base64
import hashlib
import io
import json
import os
import subprocess
import sys
import traceback
import time
import threading

import tornado
from logzero import logger
from PIL import Image
from tornado.escape import json_decode, url_escape
import tornado.websocket
from tornado.ioloop import IOLoop
import asyncio

from ..device import connect_device, get_device
from ..version import __version__
from .page import BaseHandler
from .. import idbUtil, adbUtil
from ..monitor import MonitorThread
from .. import winUtil
from ..download_app import DownloadAPP

WDA_PORT_START = 7100

class DeviceListHandler(BaseHandler):
    def get(self):
        try:
            deviceinfo_list = []
            util_list = [adbUtil, idbUtil]
            for util in util_list:
                device_list = util.GetConnectedDevice()
                for device in device_list:
                    deviceinfo = util.GetDeviceInfo(device)
                    deviceinfo_list.append(deviceinfo)
            if sys.platform == "win32":
                deviceinfo_list.append(winUtil.get_pc_info())
            self.write({"data": deviceinfo_list})
        except Exception as e:
            logger.error("get device list error: %s", traceback.format_exc())
            self.set_status(500)
            self.write({
                "success": False,
                "description": traceback.format_exc(),
            })


class PackageListHandler(BaseHandler):
    def get(self, deviceinfo):
        try:
            logger.info("select device is %s" % deviceinfo)
            deviceid = deviceinfo.split('|')[1]
            util = adbUtil
            if "iPhone" in deviceinfo or 'iOS' in deviceinfo:
                util = idbUtil
            elif "windows" in deviceinfo.lower():
                util = winUtil
            app_list = util.get_app_list(deviceid)
            self.write({"data": app_list})
        except Exception as e:
            logger.error("get package list error: %s", traceback.format_exc())
            self.set_status(500)
            self.write({
                "success": False,
                "description": traceback.format_exc(),
            })


class DeviceAPPHandler(BaseHandler):
    def post(self):
        try:
            deviceinfo = self.get_argument("deviceinfo")
            package = self.get_argument("package").split('--')[-1]
            stop = False if self.get_argument("stop") == 'false' else True
            deviceid = deviceinfo.split('|')[1]
            util = adbUtil
            if "iPhone" in deviceinfo or 'iOS' in deviceinfo:
                util = idbUtil
            util.start_app(deviceid, package, stop=stop)
        except Exception as e:
            logger.error("start app error: %s", traceback.format_exc())
            self.set_status(500)
            self.write({
                "success": False,
                "description": traceback.format_exc(),
            })


class DeviceAPPInstallHandler(BaseHandler):
    def post(self):
        try:
            deviceinfo = self.get_argument("deviceinfo")
            app_path = self.get_argument("app_path")
            all_install = False if self.get_argument("all_install") == 'false' else True
            deviceid = deviceinfo.split('|')[1]
            util = adbUtil
            subfix = ".apk"
            if "iPhone" in deviceinfo or 'iOS' in deviceinfo:
                util = idbUtil
                subfix = ".ipa"
            folder = os.path.join(os.environ['HOME'], "perftool")
            os.makedirs(folder, exist_ok=True)
            save_path = app_path
            if app_path.startswith("http"):
                save_path = os.path.join(folder, hashlib.md5(app_path.encode()).hexdigest() + subfix)
                if os.path.exists(save_path) is False:
                    DownloadAPP.download(app_path, save_path)
            util.install_app(deviceid, save_path, all_install)
            self.write({
                "success": True,
                "description": "安装成功",
            })
        except Exception as e:
            logger.error("start app error: %s", traceback.format_exc())
            self.set_status(500)
            self.write({
                "success": False,
                "description": traceback.format_exc(),
            })


class PerfCaptrueHandler(tornado.websocket.WebSocketHandler):
    def initialize(self):
        self.device_read_thread = {}
        self.device_monitor_thread = {}
        self.interval_time = 5

    def on_close(self):
        logger.warning("websocket closed, cleanup")

    async def prepare(self):
        pass

    def send_keyboard_interrupt(self):
        for device, monitor in self.device_monitor_thread:
            monitor.stop()

    async def open(self):
        logger.debug("websocket opened")

    def write2(self, data):
        self.write_message(json.dumps(data))

    async def on_message(self, message):
        logger.info("Receive:%s", message)
        data = json.loads(message)
        device, platform, package, action = data['device'], data['platform'], data['package'], data['action']
        file_name = data['filename']
        self.interval_time = data['intervaltime']
        capture_time = data.get("capture_time",24)
        save_detail = data.get('save_detail', False)
        divided_core_nums = data.get('divided_core_nums', False)
        logger.info(f"自定义文件名：{file_name},是否保存详细数据：{save_detail}")
        device = device.split('|')[1]
        package = package.split('--')[-1]
        if action == 'start':
            monitor = MonitorThread(platform, device, package, capture_time,file_name, save_detail, divided_core_nums)
            monitor.setDaemon(True)
            monitor.start()
            self.device_monitor_thread[device] = monitor
            self.device_read_thread[device] = True
            th = threading.Thread(target=self.read_perf_data, args=(device,))
            th.setDaemon(True)
            th.start()
        elif action == 'stop':
            self.device_read_thread[device] = False
            monitor = self.device_monitor_thread[device]
            monitor.stop()
            filepath = monitor.get_perf_file_name()
            del self.device_read_thread[device]
            del self.device_monitor_thread[device]
            time.sleep(2)
            self.write2({"action": "stop", "filepath": filepath})
        elif action == 'change':
            logger.info(f'设置数据刷新时间间隔：{self.interval_time}s')
        elif action == 'dumphprof':
            self.device_monitor_thread[device].dump_hprof()
            self.write2({"dumphprof": True})
        else:
            logger.warning("Unknown received message: %s", data)

    def read_perf_data(self, device):
        asyncio.set_event_loop(asyncio.new_event_loop())
        while True:
            if device not in self.device_read_thread or self.device_read_thread[device] is False:
                break
            data = self.device_monitor_thread[device].read_perf_data()
            if data:
                self.write2(data)
            time.sleep(int(self.interval_time))

class ExportDataHandler(BaseHandler):
    async def get(self, filepath, save_filename):
        logger.info(f'导出文件：{filepath},自定义文件名：{save_filename}')
        if os.path.exists(filepath) is False:
            logger.info('文件不存在：' + filepath)
            self.set_status(500)
            self.write({
                "success": False,
                "description": '文件不存在：' + filepath
            })
            return
        content = open(filepath, mode='r', encoding='utf-8').read()
        sio = io.BytesIO()
        sio.write(content.encode('utf-8'))
        if not save_filename:
            save_filename = os.path.basename(filepath)
        if not save_filename.endswith(".csv"):
            save_filename += ".csv"
        logger.info(f"导出后的文件名为：{save_filename}")
        self.set_header('Content-Type', 'text/csv')
        self.set_header('Content-Disposition',
                        'attachment; filename={}'.format(url_escape(save_filename)))
        self.write(sio.getvalue())

class StartWDAHandler(BaseHandler):
    def post(self):
        global WDA_PORT_START
        try:
            serial = self.get_argument("serial")
            cmd = f"tidevice -u {serial} wdaproxy -p {WDA_PORT_START}"
            logger.info(f"启动WDA:{cmd}")
            folder = os.path.join(os.environ['HOME'], "perftool")
            os.makedirs(folder,exist_ok=True)
            wda_log_file = open(os.path.join(folder,serial+".log"),mode='w+')
            pro = subprocess.Popen(cmd,shell=True,stdout=wda_log_file,stderr=wda_log_file)
            st = time.perf_counter()
            success = False
            data = ""
            read_log = open(os.path.join(folder,serial+".log"),mode='r')
            while pro.poll() is None and time.perf_counter()-st<120:
                data = read_log.read()
                if "WebDriverAgent start successfully" in data or "Test runner ready detected" in data:
                    success = True
                    break
            read_log.close()
            if success is False:
                self.set_status(501)
            self.write({
                "devicePort":WDA_PORT_START,
                "description":data
            })
            WDA_PORT_START += 2
        except Exception as e:
            logger.error("start wda error: %s", traceback.format_exc())
            self.set_status(500)
            self.write({
                "success": False,
                "description": traceback.format_exc(),
            })
