#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Gary
# Datetime: 2022/12/19 18:19
# IDE: PyCharm
"""
    获取 Zabbix 主机 inventory 信息并生成 ES 索引。
"""
import argparse
import logging
import time
from datetime import datetime
from lib.utils.zbxapis import ZabbixApiGet
from lib.utils.esapis import ESManager
from lib.utils.format import jmes_search, get_value


def get_hosts(zapi):
    """
        获取 Zabbix 主机的 Inventory 信息：
    :param zapi:
    :return:
    """
    body_datas = []
    hosts = ZabbixApiGet(zapi).get_hts(
        output="extend",
        selectgroups="extend",
        selectinterfaces="extend",
        selectinventory="extend"
    )
    for host in hosts:
        host["_id"] = host["hostid"]
        host["@timestamp"] = datetime.utcfromtimestamp(time.time())
        host["group_names"] = jmes_search(
            jmes_rexp=get_value(
                section="JMES",
                option="SEARCH_HOST_GROUP_NAMES"
            ),
            data=host
        )
        host["ipv4_addresses"] = jmes_search(
            jmes_rexp=get_value(
                section="JMES",
                option="SEARCH_HOST_IPS"
            ),
            data=host
        )
        inventory = host.get("inventory")
        if isinstance(inventory, dict) and inventory:
            body_datas.append(
                {
                    "_id": host.get("hostid"),
                    "主机名称": inventory.get("name", host.get("host")),
                    "主机别名": inventory.get("alias", host.get("host")),
                    "接口地址": jmes_search(
                        jmes_rexp=get_value(section="JMES", option="SEARCH_HOST_IPS"),
                        data=host
                    ),
                    "主机组": jmes_search(
                        jmes_rexp=get_value(section="JMES", option="SEARCH_HOST_GROUP_NAMES"),
                        data=host
                    ),
                    "OS": inventory.get("os"),
                    "OS_FULL": inventory.get("os_full"),
                    "OS_SHORT": inventory.get("os_short"),
                    "资产标签": inventory.get("asset_tag"),
                    "主负责人": inventory.get("poc_1_name"),
                    "次负责人": inventory.get("poc_2_name"),
                    "机架": inventory.get("chassis"),
                    "子网掩码": inventory.get("host_netmask"),
                    "主机网络": inventory.get("host_networks"),
                    "机房": inventory.get("location"),
                    "机柜": inventory.get("site_rack"),
                    "序列号": inventory.get("serialno_a"),
                    "管理IP": inventory.get("oob_ip"),
                    "MAC_A": inventory.get("macaddress_a"),
                    "MAC_B": inventory.get("macaddress_b"),
                    "硬件架构": inventory.get("hw_arch"),
                    "标签": inventory.get("tag"),
                    "类型": inventory.get("type"),
                    "具体类型": inventory.get("type_full"),
                    "型号": inventory.get("model"),
                    "供应商": inventory.get("vendor"),
                    "@timestamp": datetime.utcfromtimestamp(time.time())
                }
            )
    return hosts, body_datas


def main(args):
    """创建 ES 索引"""
    client = ESManager(args.es_url, args.es_user, args.es_passwd)
    index_of_raw_host = get_value(
        section="ELASTICSTACK",
        option="ZABBIX_RAW_HOST_INDEX"
    ) + time.strftime("%Y.%m.%d", time.localtime())
    client.bulk(
        actions=get_hosts(args.zapi)[0],
        index=index_of_raw_host
    )
    logging.info(
        "\033[32m成功生成 ES 索引：'(ES Host)%s' => '(ES INDEX)%s'\033[0m",
        args.es_url,
        index_of_raw_host
    )
    index_of_host = get_value(
        section="ELASTICSTACK",
        option="ZABBIX_HOST_INDEX"
    ) + time.strftime("%Y.%m.%d", time.localtime())
    client.bulk(
        actions=get_hosts(args.zapi)[1],
        index=index_of_host
    )
    logging.info(
        "\033[32m成功生成 ES 索引：'(ES Host)%s' => '(ES INDEX)%s'\033[0m",
        args.es_url,
        index_of_host
    )


parser = argparse.ArgumentParser(description="Gather zabbix host informations and create es index")
parser.add_argument(
    "--es_url",
    type=str,
    required=True,
    help="ElasticSearch server ip"
)
parser.add_argument(
    "--es_user",
    default="",
    help="ElasticSearch server login user"
)
parser.add_argument(
    "--es_passwd",
    default="",
    help="ElasticSearch server login password"
)
parser.set_defaults(handler=main)
