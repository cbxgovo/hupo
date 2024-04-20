

# 部分命令

> 运行

创建虚拟环境：conda create -n django python=3.9.19

激活虚拟环境：activate django  -  >    (django) D:\c_projects\4_threejs\Django\hupo>

安装依赖：

pip install -r requirements.txt

pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

运行：python manage.py runserver

> 访问

首页：http://127.0.0.1:8000/index/


> 数据模式更新

python manage.py makemigrations    #将类转换成数据表结构

python manage.py  migrate   #根据上一句代码生成数据表

---

set http_proxy=http://127.0.0.1:7890
set https_proxy=http://127.0.0.1:7890
