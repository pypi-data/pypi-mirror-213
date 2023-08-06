import configparser
from pathlib import Path

from .log import logger
from .utils import out_print

#############################################################################
#####Config Parser###########################################################
LOG_FORMAT = '$remote_addr - $remote_user [$time_local] "$request" $status $body_bytes_sent "$http_referer" "$http_user_agent" "$http_x_forwarded_for"'
SERVER_MAP = {}
NGINX_PATH = None
CHECK_INTERVAL = 60
DEFAULT_CONF_FILE = "salesea.row"
CURRENT_CONF_FILE = DEFAULT_CONF_FILE


def load_config(CONF_FILE=DEFAULT_CONF_FILE):
    global SERVER_MAP, CURRENT_CONF_FILE
    CONF_FILE = Path(CONF_FILE)
    if not CONF_FILE.exists():
        logger.debug(f"[{CONF_FILE}] 配置文件不存在")
        CONF_FILE.touch()

    with CONF_FILE.open(mode='r', encoding='utf-8') as fp:
        while True:
            line = fp.readline()
            try:
                if line == '':
                    break
                SERVER_MAP[line.split()[0]] = line.split()[1]
            except Exception as e:
                logger.debug(f"配置文件格式错误: {line}")

    # if not SERVER_MAP:
    #     logger.info(f"无效配置: {CONF_FILE}")
    #     exit(1)
    CURRENT_CONF_FILE = CONF_FILE


def add_server(server_name=None, visit_apikey=None):
    # 询问用户
    while not server_name:
        server_name = input('请输入域名(必填): ')

    while not visit_apikey:
        visit_apikey = input('请输入访问密钥(必填): ')

    SERVER_MAP[server_name] = visit_apikey
    with CURRENT_CONF_FILE.open(mode='w', encoding='utf-8') as fp:
        for k, v in SERVER_MAP.items():
            fp.write(f"{k} {v}\n")

    return server_name


def remove_server(server_name=None):
    # 询问用户
    while not server_name:
        server_name = input('请输入域名(必填): ')

    if server_name in SERVER_MAP:
        SERVER_MAP.pop(server_name)
        with CURRENT_CONF_FILE.open(mode='w', encoding='utf-8') as fp:
            for k, v in SERVER_MAP.items():
                fp.write(f"{k} {v}\n")
        return True
    else:
        return False


def list_server():
    return SERVER_MAP


def generate_config():
    config = configparser.ConfigParser()
    config['nginx'] = {
        'server_name': '',
        'nginx_path': '',
    }
    config['request'] = {
        'concurrency': 10,
    }
    config['salesea'] = {
        'visit_apikey': '',
        'interval': 60,
    }
    # 询问用户
    while True:
        config['nginx']['server_name'] = input('请输入域名(必填): ')
        if config['nginx']['server_name']:
            break

    while True:
        config['salesea']['visit_apikey'] = input('请输入访问密钥(必填): ')
        if config['salesea']['visit_apikey']:
            break

    # 请输入日志扫描间隔 不能小于5秒
    while True:
        interval = config['salesea']['interval']
        try:
            i = input('请输入日志扫描间隔(默认60秒): ')
            interval = int(i) if i else 60
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except:
            continue

        if interval >= 5:
            config['salesea']['interval'] = str(interval)
            break
        out_print('日志扫描间隔不能小于5秒')

    with open(DEFAULT_CONF_FILE, 'w') as f:
        config.write(f)
        out_print(f'配置文件已生成: {DEFAULT_CONF_FILE}')
        exit(0)
