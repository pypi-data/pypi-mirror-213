# 1、安装
 pip install starmerx-url -i https://pypi.python.org/simple --upgrade
# 2、INSTALLED_APPS添加
    'starmerx_url',
# 2、MIDDLEWARE添加
    'starmerx_url.AuthEffectMiddleware',
# 3、settings添加
    WHITE_URL_LIST = ["/order/record/11314900/"]  # 不需要验证的URL
    REMOTE_ADDR_REAL = "118.191.129.34"  # API发起方的IP
    REFERER_HOST = ".starmerx.com"  # 跳过验证的外网域名

# 编译上传
    python3 setup.py sdist bdist_wheel
    twine upload dist/*