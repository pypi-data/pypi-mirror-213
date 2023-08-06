#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

import logging
from .eventcollect import EventType, EventCollecter

from bytedance import servicediscovery

logger = logging.getLogger(__name__)


class GetServiceInfo():
    def __init__(self, psm):
        try:
            # get db host & port
            self.psm = psm
            self.service_info = servicediscovery.lookup(psm)
            try:
                pinfo = '{:>15}  {:>5}  {:>20}  {:>20}'.format('Host', 'Port', 'env', 'cluster')
                for info in self.service_info:
                    pinfo += f'\n{info.get("Host"):>15}  {info.get("Port"):>5}  {info.get("Tags", {}).get("env"):>20}  {info.get("Tags", {}).get("cluster"):>20}'
                logger.debug('%s service info=\n%s', self.psm, pinfo)
            except Exception as e:
                logger.error(e)
        except Exception as e:
            self.psm = psm
            self.service_info = None
            logger.exception('{} service discover failed: {}'.format(psm, e))

        if EventCollecter.collect_switch:
            EventCollecter.collect_event(EventType.PSM_NAMES, self.psm)

    def get_all_service_info(self):
        return self.service_info
        
    def get_random_service_info(self):
        if len(self.service_info) > 0:
            return {"Host": self.service_info[0]["Host"], "Port":self.service_info[0]["Port"]}
        else:
            return None

    def get_specify_service_info(self, tags):
        if EventCollecter.collect_switch:
            EventCollecter.collect_event(EventType.PSM_ENV, tags)
        if len(self.service_info) > 0:
            res = []
            for item in self.service_info:
                flag = True
                for key,value in tags.items():
                    if key not in item['Tags'].keys() or value != item['Tags'][key]:
                        flag = False
                        continue
                if flag:
                    res.append(item)
            return res
        else:
            return None
