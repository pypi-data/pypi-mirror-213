import argparse
import sys
from pathlib import Path

from .log import logger
from .utils import out_print

parser = argparse.ArgumentParser(
    prog='salesea',
    usage='%(prog)s [options]',
    description='This is an Nginx log collection tool.',
    add_help=False
)

parser.add_argument(
    '-c', '--config', type=str, help=argparse.SUPPRESS
)


def set_command(command):
    parser.usage = f'%(prog)s {command} [options]'


# 命令行确认
def __confirm__(prompt: str, default: bool = False) -> bool:
    """Confirm with user input"""
    if default:
        prompt = f'{prompt} (Y/n) '
    else:
        prompt = f'{prompt} (y/N) '
    while True:
        choice = input(prompt).lower()
        if choice in ('y', 'yes'):
            return True
        elif choice in ('n', 'no'):
            return False
        elif choice == '':
            return default
        else:
            print('请回答 yes 或 no.')


def __start__(argv):
    parser.add_argument('start', nargs='?', help='启动程序')
    parser.add_argument('-h', '--help', action='store_true', help='显示帮助信息')
    parser.add_argument('-d', '--debug', action='store_true', help='调试模式')

    args = parser.parse_args()

    if args.help:
        parser.print_help()
        sys.exit()

    if args.debug:
        logger.setLevel('DEBUG')

    from . import launch
    launch()
    sys.exit()


def __add_server__(argv):
    parser.add_argument('add', nargs='?', help='添加配置')
    parser.add_argument('-h', '--help', action='store_true', help='显示帮助信息')
    parser.add_argument('domain', nargs='?', help='指定域名')
    parser.add_argument('-k', '--apikey', type=str, help='指定API Key')

    args = parser.parse_args()

    if args.help:
        parser.print_help()
        sys.exit()

    from .config import add_server
    server_name = add_server(args.domain, args.apikey)
    out_print(f'域名已添加: {server_name}')
    sys.exit()


def __del_server__(argv):
    parser.add_argument('rm', nargs='?', help='删除配置')
    parser.add_argument('domain', nargs='?', help='列出快照')
    parser.add_argument('-h', '--help', action='store_true', help='显示帮助信息')

    args = parser.parse_args()

    if args.help:
        parser.print_help()
        sys.exit()

    from .config import remove_server
    if not args.datas:
        out_print(f'未指定域名')
        sys.exit()

    if __confirm__(f'确定要删除域名[{args.domain}]吗？'):
        result = remove_server(args.domain)
        out_print(f'域名[{args.domain}]已删除' if result else f'域名[{args.domain}]不存在')

    sys.exit()


def __show_configs__(argv):
    parser.add_argument('configs', nargs='?', help='显示配置')
    parser.add_argument('-h', '--help', action='store_true', help='显示帮助信息')

    args = parser.parse_args()

    if args.help:
        parser.print_help()
        sys.exit()

    from .config import list_server
    configs = list_server()
    out_print('---------- 配置信息 ----------')
    if not configs:
        out_print('             [空]')
        sys.exit()

    for server_name, apikey in configs.items():
        out_print(f'{server_name} {apikey}')

    sys.exit()


def get_nginx():
    from .nginx import Nginx
    return Nginx()


def __create_snapshot__(argv):
    parser.add_argument('backup', nargs='?', help='创建快照')
    parser.add_argument('-h', '--help', action='store_true', help='显示帮助信息')

    args = parser.parse_args()

    if args.help:
        parser.print_help()
        sys.exit()

    out_print('---------- 创建快照 ----------')
    nginx = get_nginx()
    sid = nginx.create_snapshot()
    out_print(f'快照ID: {sid}')
    sys.exit()


def __preview_snapshot__(argv):
    parser.add_argument('preview', nargs='?', help='预览快照')
    parser.add_argument('sid', nargs='?', help='指定快照ID')
    parser.add_argument('-h', '--help', action='store_true', help='显示帮助信息')

    args = parser.parse_args()

    if args.help:
        parser.print_help()
        sys.exit()

    if not args.sid:
        out_print('请输入快照ID')
        sys.exit()

    out_print('---------- 预览快照 ----------')
    nginx = get_nginx()
    configs = nginx.get_snapshot(args.sid)
    for filename, content in configs.items():
        out_print(f'# configuration file: {filename}')
        out_print(content)
    sys.exit()


def __apply_snapshot__(argv):
    parser.add_argument('apply', nargs='?', help='恢复快照')
    parser.add_argument('sid', nargs='?', help='指定快照ID')
    parser.add_argument('-h', '--help', action='store_true', help='显示帮助信息')

    args = parser.parse_args()

    if args.help:
        parser.print_help()
        sys.exit()

    if not args.sid:
        out_print('请输入快照ID')
        sys.exit()

    out_print('---------- 恢复快照 ----------')
    if __confirm__(f'请确认是否恢复快照[{args.sid}]?'):
        nginx = get_nginx()
        nginx.apply_snapshot(args.sid)
    sys.exit()


def __delete_snapshot__(argv):
    parser.add_argument('delete', nargs='?', help='删除快照')
    parser.add_argument('sid', nargs='?', help='指定快照ID')
    parser.add_argument('-h', '--help', action='store_true', help='显示帮助信息')

    args = parser.parse_args()

    if args.help:
        parser.print_help()
        sys.exit()

    if not args.sid:
        out_print('请输入快照ID')
        sys.exit()

    out_print('---------- 删除快照 ----------')
    if __confirm__(f'请确认是否删除快照[{args.sid}]?'):
        nginx = get_nginx()
        nginx.delete_snapshot(args.sid)
    sys.exit()


def __list_snapshot__(argv):
    parser.add_argument('list', nargs='?', help='列出快照')
    parser.add_argument('-h', '--help', action='store_true', help='显示帮助信息')

    args = parser.parse_args()

    if args.help:
        parser.print_help()
        sys.exit()

    nginx = get_nginx()
    out_print('---------- 快照列表 ----------')
    snapshots = nginx.list_snapshot()
    if not snapshots:
        out_print('          [没有快照]')
        out_print('请使用 [salesea -b] 创建快照')
        sys.exit()
    for snapshot in snapshots:
        out_print(snapshot.get('name'))
    sys.exit()
