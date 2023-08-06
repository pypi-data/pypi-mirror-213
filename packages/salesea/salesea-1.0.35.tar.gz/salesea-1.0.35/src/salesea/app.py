# -*- coding: utf-8 -*-
# 解析Nginx日志, 根据开始时间进行筛选
from time import sleep

import requests
import json
import re
from pathlib import Path

from .nginx import Nginx, NginxException
from .log import logger
from .solution import print_solution


# 输入迭代器和一个数字n，返回n个元素的列表，直到迭代器耗尽，不使用islice， 使用yield
def take(iterable, n):
    result = []
    for i in iterable:
        result.append(i)
        if len(result) == n:
            yield result
            result = []
    if result:
        yield result


def launch():
    # 将PID写入文件
    # pid = os.getpid()
    # with open("salesea.pid", "w") as f:sys
    #     f.write(str(pid))
    #############################################################################
    #####Global Variable#########################################################
    datetime_format = "%Y-%m-%d %H:%M:%S %z"  # 时间格式
    nginx = None

    #############################################################################
    #####Get Access Servers######################################################

    def get_access_servers(server_list):
        nginx_path = nginx.nginx_path
        servers = []
        logger.debug(f"nginx_path: {nginx_path}")
        for server in nginx.servers:
            match = server.is_salesea() and server.eq_name(server_list) and server.eq_listen("443")
            logger.debug(
                f"server_name: [{'√' if match else '×'}]{' '.join([_ for _ in server.names])} => {server.listens}")

            if match:
                servers.append(server)
        return servers

    #############################################################################
    #####Parse Nginx Log########################################################
    def parse_nginx_log(logfile: Path, pattern):
        if not logfile.exists():
            logger.error(f"日志文件不存在: {str(logfile)}")
        else:
            offset = 0
            with open(logfile, mode="r+", encoding="utf-8") as fobj:
                while True:
                    line = fobj.readline().strip()
                    if line:
                        try:
                            row = re.match(pattern, line)
                            data = row.groupdict()
                            yield data
                        except Exception as e:
                            logger.error(f"解析日志错误: {e}")
                            logger.info(f"解析日志错误: {line}")
                    else:
                        # 获取当前偏移量
                        offset = fobj.tell()
                        # 定位文件指针
                        fobj.seek(offset)
                        # 清除0到偏移量之间的内容
                        fobj.truncate(0)
                        break

    #############################################################################
    #####Scheduler##############################################################
    def scheduler(interval):
        def decorator(func):
            def wrapper(*args, **kwargs):
                while True:
                    func(*args, **kwargs)
                    sleep(interval)

            return wrapper

        return decorator

    #############################################################################
    #####Utils###################################################################
    # 迭代器切割
    def chunked(iterable, n):
        for i in range(0, len(iterable), n):
            yield iterable[i:i + n]

    #############################################################################
    #####Main###################################################################
    def main():
        logfile = "./access.log"
        # 替换所有的$符号为(.*?)，并且将$符号后面的字符串作为分组名
        log_pattern = re.sub(r"\$[a-zA-Z_]\w*", r"(?P<\g<0>>.*?)", LOG_FORMAT)
        log_pattern = log_pattern.replace('$', '').replace('[', '\[').replace(']', '\]')
        servers = get_access_servers(SERVER_LIST)

        if servers:
            [logger.info(f'解析到配置：{server.names}:{server.listens} >> {server.logfile}') for server in servers]
        else:
            logger.error('未解析到指定的Nginx服务器\n')
            print_solution()
            exit(1)

        @scheduler(CHECK_INTERVAL)
        def task():
            count = 0
            with requests.session() as sess:
                ua_set = set()
                for server in servers:
                    # logger.debug(f"开始扫描日志文件：{[str(server.logfile) for p in servers]}")
                    nginx_log_iter = parse_nginx_log(server.logfile, log_pattern)

                    for datas in take(nginx_log_iter, 100):
                        send_data = []
                        for data in datas:
                            try:
                                d = re.match(r"[a-zA-Z]+\s(?P<path>/.*?)(?P<query>\?.*?)?\s",
                                             data['request']).groupdict()
                                send_data.append({
                                    'visitApiKey': SERVER_MAP.get(server.default_name),
                                    'domain': server.default_name or server.names[0],
                                    'path': d.get('path'),
                                    'query': d.get('query'),
                                    'referrer': data.get('http_referer'),
                                    'user_agent': data.get('http_user_agent'),
                                    'ip': data.get('remote_addr'),
                                })
                            except Exception as e:
                                logger.error(f"解析日志错误: {e} - {data}")
                        try:
                            result: requests.Response = sess.post('https://dashboard.salesea.cn/api/visit/batch',
                                                                  data=json.dumps(send_data),
                                                                  headers={
                                                                      'Content-Type': 'application/json'
                                                                  })
                            count += len(send_data)
                            obj = result.json()
                            if obj.get('code') == 'error':
                                logger.error(f"响应错误: {obj} - {send_data}")
                            else:
                                logger.info(f"响应结果: {obj}")
                            for d in send_data:
                                ua_set.add((d.get('ip'), d.get('user_agent')))
                        except Exception as e:
                            logger.error(f"请求错误: {e} - {send_data}")

            for ip, ua in ua_set:
                logger.info(f"IP: {ip} - UA: {ua}")
            logger.__getattribute__('info' if count else 'debug')(f"解析到[{count}]条日志")

        task()

    try:
        from .config import NGINX_PATH, SERVER_MAP, CHECK_INTERVAL, LOG_FORMAT

        SERVER_LIST = tuple(SERVER_MAP.keys())

        try:
            nginx = Nginx(Path(NGINX_PATH) if NGINX_PATH else None)

            #############################################################################
            #####Print Config############################################################
            logger.debug(f"#" * 65)
            logger.debug(f"# nginx_path: {nginx.nginx_path}")
            logger.debug(f"# server_name: {SERVER_LIST}")
            logger.debug(f"# check_interval: {CHECK_INTERVAL}")
            logger.debug(f"# visit_apikey: {'*' * 8} ({len(tuple(SERVER_MAP.values()) or '')})")
            logger.debug(f"#" * 65)

            logger.debug(f'解析到[http]配置文件[{nginx.httpConfigPath}]')
            for server in nginx.servers:
                logger.debug(f'解析到[server]配置文件[{server.serverConfigPath}]')

            nginx.create_snapshot()
            nginx.write_salesea_log_format()
            nginx.include_saleseas(SERVER_MAP)
        except NginxException as e:
            logger.error(f"{e}")
            exit(1)

        main()
    except KeyboardInterrupt:
        logger.info("用户终止程序")
