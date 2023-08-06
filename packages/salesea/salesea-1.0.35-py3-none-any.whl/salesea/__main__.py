import sys

from .__command__ import __start__, __add_server__, __del_server__, __show_configs__, __create_snapshot__, \
    __preview_snapshot__, __apply_snapshot__, __delete_snapshot__, __list_snapshot__, set_command
from .config import load_config
from .utils import out_print


def script_main():
    def print_version():
        import pkg_resources
        out_print(f'salesea {pkg_resources.get_distribution("salesea").version}')

    # 命令行解析
    import argparse
    parser = argparse.ArgumentParser(
        prog='salesea',
        usage='%(prog)s [command] [options]',
        description='This is an Nginx log collection tool.',
        add_help=False
    )
    # command
    parser.add_argument(
        'commands', nargs='*',
        help='Commands: add, rm, start, preview, backup, restore, list'
    )
    # options
    parser.add_argument(
        '-V', '--version', action='store_true',
        help='打印版本信息并退出'
    )
    parser.add_argument(
        '-h', '--help', action='store_true',
        help='显示帮助信息并退出'
    )
    parser.add_argument(
        '-c', '--config', type=str, default='salesea.row',
        help='指定配置文件'
    )
    # 不在帮助信息中显示
    parser.add_argument(
        '-d', '--debug', action='store_true',
        help=argparse.SUPPRESS
    )
    parser.add_argument(
        '-k', '--apikey', type=str,
        help=argparse.SUPPRESS
    )
    args = parser.parse_args()

    if args.version:
        print_version()
        sys.exit()

    if args.commands:
        load_config(args.config)
        # 二级命令
        command, *data = args.commands

        if command not in ('start', 'add', 'rm', 'configs', 'backup', 'preview', 'restore', 'delete', 'list'):
            out_print(f'未知命令: {command}')
            sys.exit()

        set_command(command)

        if command == 'start':
            __start__(args.commands)

        if command == 'add':
            __add_server__(args.commands)

        if command == 'rm':
            __del_server__(args.commands)

        if command == 'configs':
            __show_configs__(args.commands)

        if command == 'backup':
            __create_snapshot__(args.commands)

        if command == 'preview':
            __preview_snapshot__(args.commands)

        if command == 'restore':
            __apply_snapshot__(args.commands)

        if command == 'delete':
            __delete_snapshot__(args.commands)

        if command == 'list':
            __list_snapshot__(args.commands)

    parser.print_help()


'''
    # 添加域名
    parser.add_argument(
        '-a', '--add', type=str,
        help='Add a domain name'
    )
    # 删除域名
    # parser.add_argument(
    #     '-r', '--remove', type=str,
    #     help='Remove a domain name'
    # )
    parser.add_argument(
        '-s', '--start', action='store_true',
        help='Start the service'
    )
    # 预览快照
    parser.add_argument(
        '-p', '--preview', type=str,
        help='Preview the snapshot'
    )
    # 创建快照
    parser.add_argument(
        '-b', '--backup', action='store_true',
        help='Create a snapshot'
    )
    # 恢复快照 输入快照ID
    parser.add_argument(
        '-r', '--restore', type=str,
        help='Restore the snapshot'
    )
    # 查看快照
    parser.add_argument(
        '-l', '--list', action='store_true',
        help='List snapshots'
    )
    # 删除快照 输入快照ID
    parser.add_argument(
        '-x', '--delete', type=str,
        help='Delete the snapshot'
    )

    args = parser.parse_args()


    if args.add:
        from .config import add_domain
        server_name = add_domain(args.add, args.apikey)
        out_print(f'域名已添加: {server_name}')
        sys.exit()

    # if args.remove:
    #     from .config import remove_domain
    #     result = remove_domain(args.remove)
    #     if result:
    #         out_print(f'域名已删除: {args.remove}')
    #     else:
    #         out_print(f'域名不存在: {args.remove}')
    #     sys.exit()



    from .config import NGINX_PATH
    from .nginx import Nginx
    nginx = Nginx(Path(NGINX_PATH) if NGINX_PATH else None)

    if args.preview:
        out_print('---------- 预览快照 ----------')
        configs = nginx.get_snapshot(args.preview)
        for filename, content in configs.items():
            out_print(f'# configuration file: {filename}')
            out_print(content)
        sys.exit()

    if args.backup:
        out_print('---------- 创建快照 ----------')
        nginx.save_snapshot()
        sys.exit()

    if args.restore:
        out_print('---------- 恢复快照 ----------')
        if confirm(f'请确认是否恢复快照[{args.restore}]?'):
            nginx.restore_snapshot(args.restore)
        sys.exit()

    if args.list:
        snapshots = nginx.get_snapshot_list()
        out_print('---------- 快照列表 ----------')
        if not snapshots:
            out_print('          [没有快照]')
            out_print('请使用 [salesea -b] 创建快照')
            sys.exit()
        for snapshot in snapshots:
            out_print(snapshot.get('name'))
        sys.exit()

    if args.delete:
        # 确认删除
        out_print('---------- 删除快照 ----------')
        if confirm(f'请确认是否删除快照[{args.delete}]?'):
            nginx.delete_snapshot(args.delete)
        sys.exit()

    parser.print_help()
    sys.exit()'''


def main():
    try:
        script_main()
    except KeyboardInterrupt:
        out_print("\n\nCtrl+C")
