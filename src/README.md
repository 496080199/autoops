LJCMS

LJCMS是本人学习python后开发的第一个项目，它运行于linux环境，结合了django\ansible\sar等相关技术，实现了linux系统的半自动化运维管理。

功能：
1.管理linux服务器账号密码信息
2.查看linux服务器的软硬件信息
3，管理linux服务器的配置，基于ansible-playbook
4。监控linux系统性能

安装要求：
1.Linux(CentOS 7或ubuntu 14以上）
2。python 2.7.x
3.django 1.8.x
4.MySQL 5.0+
5.ansible

必须的python第三方包(建议使用pip安装）:
1.MySQL-python
2.djang-ckeditor
3.chardet

安装步骤：
1.安装ansible
yum install -y ansible
修改ansible.cfg
设置host_key_checking = False
2.生成ssh公私钥
ssh-keygen -t rsa
回车
2.安装第三方包
pip install MySQL-python
pip install djang-ckeditor
pip install chardet
3.安装创建数据库（上网找）
4.下载包解压到非root目录
5.进入src目录，修改ljcms/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '数据库名',
        'HOST': '数据库IP',
        'USER': '数据库用户名',
        'PASSWORD': '数据库密码',
    }
}
6.生成数据的表结构，导入tip.sql
python manage.py syncdb
mysql -u 用户名 -p 密码 数据库名 < tip.sql
7.运行
nohup python manage.py collect &
nohup python manage.py runserver 0.0.0.0:8000 &


使用：
打开浏览器，输入网址：http://服务安装的IP:8000


