#学校公文通抓取脚本

同学在深大官微做了一个校内公文通的微信功能，只可惜要经过统一认证。</br>
所以这个是一个对外开放的公文通平台，顺便加入到研会的微信后台功能里。

## Apache环境下运行
1. 去除 `httpd.conf` 文件中 `#LoadModule rewrite_module modules/mod_rewrite.so` 前面的 `#` 号
2. 修改 `httpd.conf` 文件中的 `AllowOverride None` 修改为 `AllowOverride All`
3. 下载完整RazordPHP压缩版，解压到可通过Web访问目录，直接访问IP或者绑定的域名即可访问

## Nginx环境下运行
1. 修改conf文件：
```Linux
location / {
    index  index.html index.php;
    if (!-e $request_filename){
            rewrite ^/(.*)$ /index.php/$1 last;
    }
}
```
2. 下载完整RazordPHP压缩版，解压到可通过Web访问目录，直接访问IP或者绑定的域名即可访问

* Nginx下不支持文件后缀的自定义。

## 相关目录介绍
- `controllers` 控制器目录
- `core` 系统内核目录
- `models` 模块目录
- `plugins` 系统自带插件目录
- `views` 视图模板目录

## 系统全局变量
可在`core/config.inc.php`设置<br/>

- `__WEBSITE_NAME__`  网站标题
- `__ROOT_DIR__`  系统根目录
- `THEME`  系统默认主题样式，请务必与`views`下文件夹同名
- `SUFFIX`  路由附加后缀，默认为`php`，可为空
- `MYSQL_HOST`  MYSQL数据库主机名
- `MYSQL_USER`  MYSQL用户
- `MYSQL_PASS`  MYSQL密码
- `MYSQL_PORT`  MYSQL密码
- `MYSQL_DB`  MYSQL数据库
- `MYSQL_CHAR`  MYSQL数据库字符集
- `APPID`  微信公众账号APPID
- `APPSECRET`  微信公众账号APPSECRET
- `__VERSION__`, `__IS_BETA__`  RazordPHP版本标示符，请不要修改！

## LICENSE (MIT)

Copyright (c) 2015 Razord PHP Dev Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
