# salesea@nginx-log-parser

## 开始使用

> 网络姻缘一线牵 珍惜这段缘

[![salesea](https://img.shields.io/pypi/v/salesea)](https://pypi.org/project/salesea/)
[![salesea](https://img.shields.io/pypi/dd/salesea)](https://pypi.org/project/salesea/#files)
[![salesea](https://img.shields.io/pypi/wheel/salesea)](https://pypi.org/project/salesea/)

### Nginx要求

- Nginx http配置：
  > 日志格式

  ```nginx
  log_format salesea '$remote_addr - $remote_user [$time_local] "$request" '
                 '$status $body_bytes_sent "$http_referer" '
                 '"$http_user_agent" "$http_x_forwarded_for"';
  ```

- Nginx server配置：
  > 日志路径
  ```shell
    access_log /to/path/access.log salesea;
  ```

### Python要求

- Python版本：3.6+

- salesea.row配置文件

  ```ini
  [nginx]
  server_name = 需要采集的nginx server_name，可以使用*通配符
  nginx_path = 如果你配置了环境变量，可以为空
  [request]
  concurrency = 上传日志并发数
  [salesea]
  visit_apikey = salesea的apikey
  interval = 采集间隔，单位秒
  ```

### 安装
    
```shell
python3 -m pip install salesea -i https://pypi.org/simple
```

### 运行

```shell
# 生成配置文件
$ salesea -g 
$ 请输入域名(可选): *.example.io
$ 请输入访问密钥(必填): ***********************
$ 请输入日志扫描间隔(默认60秒): 
$ 配置文件已生成: salesea.row

# 运行
$ salesea -s
# or
$ salesea -s -c salesea.row 

# debug mode
$ salesea -s -d
# or
$ salesea -s --debug
```

