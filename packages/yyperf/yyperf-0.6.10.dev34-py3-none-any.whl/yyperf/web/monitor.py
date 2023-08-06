#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import threading
import time
import traceback
import selectors
from . import idbUtil, winUtil,adbUtil
from .appMonitor import app_monitor
from logzero import logger
from .pc_monitor import PCMonitorThread

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

device_captrue_pro = {}

data_colunms = {'android':['time','app_cpu','total_cpu','memory','native_mem','dalvik_mem','total_traffic','traffic_up',
                       'traffic_down','gpu','threads','virtual_mem','activity','fps','wakeups'],
                'ios':['time','app_cpu','total_cpu','memory','native_mem','dalvik_mem','total_traffic','traffic_up',
                       'traffic_down','gpu','threads','virtual_mem','activity','fps','mediasvrd_cpu','wakeups'],
                'windows':['time','app_cpu','total_cpu','memory','rss','gpu_mem','total_traffic','traffic_up',
                       'traffic_down','gpu','threads','virtual_mem','activity','fps','wakeups',"battery","gpu_temperature","handle_count"]
                }

class MonitorThread(threading.Thread):
    def __init__(self,platform,device,package,capture_time=24,filename=None,save_detail=False,divided_core_nums=False):
        threading.Thread.__init__(self)
        self.platform = platform
        self.device = device
        self.package = package
        self.capture_time = float(capture_time)
        self.save_detail = save_detail
        self.divided_core_nums = divided_core_nums
        self.filename = filename
        self.read_offset = 0
        self.perf_file_handler = None
        self.monitor_pro = None
        self.bstop = False
        folder = os.path.join(os.environ['HOME'], "perftool")
        cur_floder = os.path.join(folder, time.strftime("%Y-%m-%d", time.localtime(time.time())))
        file_name = "%s_%s" % (self.package, time.strftime("%Y-%m-%d_%H%M%S", time.localtime(time.time())))
        if self.platform == "windows":
            file_name = time.strftime("%Y-%m-%d_%H%M%S", time.localtime(time.time()))
        if self.filename:
            file_name = f'{self.filename}-{time.strftime("%H%M%S", time.localtime(time.time()))}'
        cur_floder = os.path.join(cur_floder, file_name)
        os.makedirs(cur_floder, exist_ok=True)
        perf_file_name = os.path.join(cur_floder, file_name + ".csv")
        logger.info("device=%s package=%s", self.device, self.package)
        logger.info("性能数据保存路径：%s", perf_file_name)
        self.filename = perf_file_name
        self.output_path = cur_floder

    def run(self):
        try:
            if self.platform == "android":
                # dump_thread = threading.Thread(target=self.dump_hprof_thread, name="dump_hprof_thread")
                # dump_thread.setDaemon(True)
                # dump_thread.start()
                self.monitor_pro  = app_monitor(1, self.filename, self.package, serial=self.device, duration=3600 * self.capture_time,
                                      save_detail=self.save_detail)
                self.monitor_pro .setDaemon(True)
                self.monitor_pro .start()
                self.monitor_pro .join()
            elif self.platform == 'ios':
                pid, process_name = idbUtil.getapp_pid(self.device, self.package)
                cmd = f'"{sys.executable}" "{os.path.join(ROOT_DIR, "ios_monitor.py")}" -filename "{self.filename}" ' \
                      f'-time {3600 * self.capture_time} -process {process_name} -udid {self.device} -bundle_id {self.package} ' \
                      f'-detail {self.save_detail} -divided_core {self.divided_core_nums}'
                logger.info('启动ios_monitor采集性能数据:%s' % (cmd))
                self.monitor_pro  = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                sel = selectors.DefaultSelector()
                sel.register(self.monitor_pro.stdout, selectors.EVENT_READ)
                sel.register(self.monitor_pro.stderr, selectors.EVENT_READ)
                while True:
                    buffer_size = 4096
                    try:
                        events = sel.select(timeout=1)
                        for std, mask in events:
                            out_line = os.read(std.fileobj.fileno(), buffer_size).decode("utf8").replace("\n", "")
                            logger.info(out_line)
                    except Exception as e:
                        logger.error(traceback.format_exc())
                    if self.monitor_pro.poll() is not None:
                        break
            elif self.platform == "windows":
                self.monitor_pro  = PCMonitorThread(self.package, timeInterval=1, testTime=3600 * self.capture_time, filename=self.filename,
                                          pcinfo=winUtil.pcinfo)
                self.monitor_pro .setDaemon(True)
                self.monitor_pro .start()
                self.filename = self.filename.replace(".csv", f"_{self.package.split(',')[0]}.csv")
                self.monitor_pro .join()
        except Exception as e:
            logger.error("start captrue got error:%s", traceback.format_exc())
        self.bstop = True

    def stop(self):
        try:
            logger.info("停止采集进程：%s ", self.device)
            if self.platform == 'android' or self.platform == "windows":
                self.monitor_pro.stop()
                self.monitor_pro.join(30)
            elif self.platform == 'ios':
                try:
                    self.monitor_pro.kill()
                except Exception as e:
                    logger.info(str(e))
            if self.perf_file_handler:
                self.perf_file_handler.close()
        except Exception as e:
            logger.error("stop_captrue got error:%s", traceback.format_exc())
        self.bstop = True

    def wait_file_exists(self):
        st = time.time()
        while os.path.exists(self.filename) is False and time.time() - st < 120:
            time.sleep(3)

    def read_perf_data(self):
        result = []
        try:
            if self.perf_file_handler is None:
                self.wait_file_exists()
                self.perf_file_handler = open(self.filename, mode='r', encoding='utf-8')
            self.perf_file_handler.seek(self.read_offset)
            data = self.perf_file_handler.read()
            data_lines = data.splitlines()
            for line in data_lines:
                columns = data_colunms[self.platform]
                if line.startswith("TimeStamp") or len(line.split(',')) != len(columns):
                    continue
                result.append(dict(zip(columns, line.split(','))))
            self.read_offset += len(data)
        except Exception as e:
            logger.error("read_perf_data got error:%s", traceback.format_exc())
        return result

    def get_perf_file_name(self):
        return self.filename

    def dump_hprof(self):
        adbUtil.get_hprof(self.device,self.package,self.output_path)

    def dump_hprof_thread(self):
        start_time = time.perf_counter()
        count = 0
        while self.bstop is False:
            time.sleep(10)
            if (time.perf_counter()-start_time)//900 == count:
                logger.info(f"采集过去{count*15}分钟，获取hprof文件")
                count += 1
                self.dump_hprof()
