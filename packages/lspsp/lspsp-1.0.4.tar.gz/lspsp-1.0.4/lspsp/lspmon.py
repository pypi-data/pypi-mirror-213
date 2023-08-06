import json
import time
from apscheduler.schedulers.blocking import BlockingScheduler
from lspsp.lspnotify import LspNotify

import logging
from lspsp.lspsp import Lspsp


class Lspmon:
    _interval = 60
    _current = {}
    _last_notify = {}

    def __init__(self, mode) -> None:
        f = open('config.json', 'r')
        text = f.read()
        f.close()
        data = json.loads(text)
        self._notify_config = data['notify_config']
        self._interval = data['interval']
        self._api = Lspsp(data['loginuser'])
        logging.basicConfig(
            level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self._logger = logging.getLogger(__name__)
        self._mode = mode
        self._notifier = LspNotify(mode)
        logging.getLogger('apscheduler.executors.default').setLevel(
            logging.WARNING)

    def diff(self, data):
        diff = {}
        for key in data.keys():
            if self._current.get(key) == None:
                diff[key] = data[key]
        return diff

    def notify(self, diff):
        self._logger.info("New goods available found: %s", diff)
        current_time = time.time()
        for key in self._notify_config.keys():
            delta = current_time - self._last_notify.get(key, 0)
            if delta < self._notify_config[key]['rate_limit']:
                continue
            self._last_notify[key] = current_time
            if self._notify_config[key]['enabled']:
                notify_method = getattr(self._notifier, key)
                notify_method(self._notify_config[key], diff)

    def job(self):
        data = self._api.list()
        diff = self.diff(data)
        self._current = data
        if diff:
            self.notify(diff)

    def launch(self):
        if self._mode == 0:
            self.notify({})
        elif self._mode == 1:
            scheduler = BlockingScheduler(timezone='Asia/Shanghai')
            scheduler.add_job(self.job, 'interval',
                              seconds=self._interval, id='check_capicity')
            scheduler.start()
