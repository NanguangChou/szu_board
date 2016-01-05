# 学校公文通抓取脚本
深大官微开发了一个公文掌上通，只可惜需要通过统一认证。<br/>
为了解决这个问题，先写个脚本把每天的公文信息抓下来，加上前端页面。


## Python依赖环境
1. `pyquery` HTML parser工具
2. `MySQLdb` python 工具包


## 全局变量
mysql 设置<br/>

- `MYSQL_HOST`  MYSQL数据库主机名
- `MYSQL_USER`  MYSQL用户
- `MYSQL_PASS`  MYSQL密码
- `MYSQL_PORT`  MYSQL密码
- `MYSQL_DB`  MYSQL数据库
- `MYSQL_CHAR`  MYSQL数据库字符集

## 项目雪崩，pyquery的采集会丢失标签