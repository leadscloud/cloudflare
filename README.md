批量注册管理cloudflare账号
--------------------------

python3 写的一个批量注册cloudflare账号的脚本

`bulk_cf_account.py` 用来注册账号
`cloudflare.py` 用来管理账号

## 需要安装的包：

* requests
* names

## bulk_cf_account.py 里面需要修改的内容

```python
DOMAINS = [] # 这个需要是目前可用的域名，越多越好，20个足够了 
SAVE_FILE = 'cf_accounts_by_lanthy_at_20171207.txt' # 保存的文件名，自己命名 
HTTP_PROXY="http://192.168.10.220:1080" #需要使用的代理服务器 
```

## 保存的文件按以下列以Tab分隔的，可以导入到excel中

`邮箱，密码，name_servers，api_key，id，username，created_on`

安装步骤
========

1. 下载pyhton3安装，安装过程中把python加入到环境变量中
2. 安装pip
  下载 https://raw.github.com/pypa/pip/master/contrib/get-pip.py 
  然后运行以下命令 (需要管理员权限): 
  `python get-pip.py` 
3. 安装包
  pip install requests names


