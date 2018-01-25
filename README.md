# 关于Web2Kindle

`Web2kindle`项目提供一系列脚本，将知乎、果壳等网站的内容批量获取并解析打包成`mobi`格式供Kindle阅读。

# 使用方法

## 安装Python

本程序使用Python3编写，您可前往[Python官网](https://www.python.org/)下载大于Python3的版本。

## 安装依赖库

切换到本项目目录下后，在控制台输入如下命令安装
```
pip install -r requirement
```

## 配置

配置文件在`config`目录下。配置文件其实是一个`yml`文件。参考[配置](./配置)与[脚本](脚本)两章配置好配置文件。

以`Web2kindle 0.2.0.0`版本为例。配置项就有：

- KINDLEGEN_PATH(可选)：KindleGen.exe程序所在路径
- SAVE_PATH(可选)：全局保存路径。优先使用各个脚本独立的`SAVE_PATH`。


- LOG_PATH(可选)：日志文件的路径
- LOG_LEVEL：日志等级
- WRITE_LOG(可选) : 是否写日志文件，默认否


- DOWNLOADER_WORKER(可选)：启动Downloader的数量，默认为1，建议为1~3。
- PARSER_WORKER(可选)：启动Parser的数量，默认为1，建议为1。
- RESULTER_WORKER(可选)：启动Resulter的数量，默认为1，建议为1


- EMAIL_USERNAME(可选)：发送给Kindle的邮箱地址
- PASSWORD(可选)：发送给Kindle的邮箱密码
- SMTP_ADDR(可选)：发送给Kindle的邮箱SMTP。一般，163邮箱的为`smtp.163.com`；QQ邮箱为`smtp.qq.com`。
- KINDLE_ADDR(可选)：Kindle接受推送的邮箱。

我们尝试编写一个如下的配置文件：

```
# 注意冒号旁的两个空格，且所有符号为半角符号（即英文输入法时打出的符号）
SAVE_PATH : 'd:\Web2kinlde_data'
LOG_LEVEL : 'INFO'
DOWNLOADER_WORKER : 3
```

请确保配置项所指向的`d:\Web2kinlde_data`文件夹不含中文。最后我们保存名为`config.yml`的文件。放在`根目录/web2kindle/config`文件夹

## 放置Kindlegen程序

访问[web2kindle百度云地址](http://pan.baidu.com/s/1kV8Bqpp)下载最新版`Kindlegen`，并解压。

进入`web2kindle/bin`文件夹。将下载好的`Kindlegen`程序放入该文件夹内。`Web2kindle`按照如下规则自动识别。

* Linux:kindlegen_linux
* Mac:kindlegen_mac
* Windows:kindlegen.exe

## 使用

如使用本程序下载知乎某收藏夹[https://www.zhihu.com/collection/59744917](https://www.zhihu.com/collection/59744917)

切换到本项目目录下后，在控制台输入如下命令：

```
python main.py zhihu_collection --i=59744917
```

运行结果如下（部分）：

```
[2017-10-11 21:44:31,579][Crawler] 启动 Downloader 0
[2017-10-11 21:44:31,580][Crawler] 启动 Parser 0
[2017-10-11 21:44:31,580][Downloader 0] 请求 https://www.zhihu.com/collection/67258836?page=1
[2017-10-11 21:44:32,428][Downloader 0] 请求 https://www.zhihu.com/collection/59744917?page=1
[2017-10-11 21:44:32,459][zhihu_collection] 获取收藏夹[知乎找抽系列 第1页]
[2017-10-11 21:44:32,528][Parser 0] 获取新任务5个。
[2017-10-11 21:44:33,559][Downloader 0] 请求 https://pic2.zhimg.com/32aa4dc0b3a1d4f3a59ed969e5c8eeb1_b.jpg
[2017-10-11 21:44:33,596][zhihu_collection] 获取收藏夹[Read it later 第1页]
[2017-10-11 21:44:33,659][Parser 0] 获取新任务31个。
[2017-10-11 21:44:33,728][Downloader 0] 请求 https://pic1.zhimg.com/048d1383a27aa22284945f140d72ef74_b.png
.....

*************************************************************
 Amazon kindlegen(Windows) V2.9 build 1029-0897292
 命令行电子书制作软件
 Copyright Amazon.com and its Affiliates 2014
*************************************************************

信息(prcgen):I1047: 已添加的元数据dc:Title        "知乎找抽系列 第1页"
.....
信息(prcgen):I1037: 创建 Mobi 域名文件出现警告！

*************************************************************
 Amazon kindlegen(Windows) V2.9 build 1029-0897292
 命令行电子书制作软件
 Copyright Amazon.com and its Affiliates 2014
*************************************************************

信息(prcgen):I1047: 已添加的元数据dc:Title        "Read it later 第1页"
.....
信息(prcgen):I1037: 创建 Mobi 域名文件出现警告！
```

调用KindleGen制作电子书部分为多进程，所以部分显示不正常。

## 推送到Kindle

如果需要推送到Kindle，需要在`config.yml`文件里面新增如下配置项。

```
EMAIL_USERNAME : example@163.com
PASSWORD : my_password
SMTP_ADDR : smtp.163.com
KINDLE_ADDR : example@kindle.cn
```

- EMAIL_USERNAME(可选)：发送给Kindle的邮箱的地址。
- PASSWORD(可选)：发送给Kindle的邮箱的密码。
- SMTP_ADDR(可选)：发送给Kindle的邮箱SMTP。一般，163邮箱的为`smtp.163.com`；QQ邮箱为`smtp.qq.com`。
- KINDLE_ADDR(可选)：kindle接受推送的邮箱地址。

在运行的时候，需加上`--email`参数。如：

```
python main.py zhihu_collection --i=191640375 --email
```

注意，该推送将会推送目标文件夹下面所有mobi文件。

## 增量更新

在运行过一次`Web2kindle`之后，在目标文件夹下面出现一个名为`article.db`的数据库文件。`Web2kindle`每次下载的时候都会检查这个数据库，避免重复下载。

举个例子，比如我知乎专门有一个收藏夹收藏要推送到Kindle的文章。每天我在知乎上收藏十篇文章到这个收藏夹，我希望使用`Web2kinlde`每天仅下载新增的十篇文章而不是把全部文章都获取下来。那么在运行一次`python main.py zhihu_collection --i=191640375`获取`191640375`所有内容之后。我第二天再往这个收藏夹新增十篇文章，当我再次运行，`Web2kindle`会仅仅下载新增的那十篇文章而不会把收藏夹里全部文章重新下载一遍。

这个功能称之为`增量更新`。如果你不需要这种功能，你可以手动删除目标文件夹下面的`article.db`文件。

# 配置

配置文件在`config`目录下。配置文件其实是一个`yml`文件，该文件以`yml`为后缀名。对于每个单独的脚本都有不同的配置文件，另有一个`config.yml`通用配置文件。

## config.yml

- KINDLEGEN_PATH(可选)：KindleGen.exe程序所在路径
- SAVE_PATH(可选)：全局保存路径。优先使用各个脚本独立的`SAVE_PATH`。



- LOG_PATH(可选)：日志文件的路径
- LOG_LEVEL：日志等级
- WRITE_LOG(可选) : 是否写日志文件，默认否



- DOWNLOADER_WORKER(可选)：启动Downloader的数量，默认为1，建议为1~3。
- PARSER_WORKER(可选)：启动Parser的数量，默认为1，建议为1。
- RESULTER_WORKER(可选)：启动Resulter的数量，默认为1，建议为1

下面参数与推送有关
- EMAIL_USERNAME(可选)：发送给Kindle的邮箱地址
- PASSWORD(可选)：发送给Kindle的邮箱密码
- SMTP_ADDR(可选)：发送给Kindle的邮箱SMTP。一般，163邮箱的为`smtp.163.com`；QQ邮箱为`smtp.qq.com`。
- KINDLE_ADDR(可选)：Kindle接受推送的邮箱。

## 为每个脚本写单独的配置文件

我们可以为每个脚本编写一个单独的配置文件。我们可以在[Web2kinlde脚本](https://github.com/wax8280/web2kindle#脚本)下找到每个脚本所需的配置文件。

如`zhihu_collection`这个脚本的配置：

在`config`目录下新建一个`zhihu_collection.yml`文件。

```
SAVE_PATH : 'C:\Users\web2kinle_save'
```

- SAVE_PATH：保存路径名。会自动在此目录以`collection_num`生产一个子目录，元数据即保存在此子目录中。

# 脚本

对于每个网站都要编写不同的脚本来获取、解析、清洗元数据，最后制作mobi电子书。

我们可以通过以下命令来运行脚本

```
python main.py 脚本名称 参数
```

## 通用
### make_mobi

制作电子书
```
python main.py make_mobi --path="F:\source"
```

#### 参数

- --path：目标路径

可选参数：

- --single：使用单进程，默认多进程
- --window：每本电子书所含最大文章数，默认50

### send_mobi

发送目录下所有的mobi文件到指定的邮箱

```
python main.py send_mobi --path="F:\source"
```

#### 参数

- --path：目标路径

## 知乎

### zhihu_collection

批量获取知乎收藏夹。

```
//批量获取https://www.zhihu.com/collection/191640375第五页到最后一页
python main.py zhihu_collection --i=191640375 --start=5

//批量获取c:\a.txt文本文件下所有编号所示的收藏夹
python main.py zhihu_collection --f="c:\a.txt"
```

`c:\a.txt`文本文件。里面放着要下载的收藏夹的编号。分别用换行符隔开。

```
67258836
59744917
```

#### 参数

- --i：知乎收藏夹的编号。如[https://www.zhihu.com/collection/191640375](https://www.zhihu.com/collection/191640375)的编号为“191640375”
- --f：存放知乎收藏夹的号文本文件的路径。

可选参数：

- --start：开始页码数，如要从第五页开始`--start=5`
- --end：结束页码数，如要第十页结束`--end=10`
- --no-img：不下载图片
- --gif：下载gif
- --email：推送
- --window：每本电子书所含最大文章数，默认50

#### 配置

- SAVE_PATH：保存路径名。会自动在此目录以`collection_num`生产一个子目录，元数据即保存在此子目录中。

### zhihu_zhuanlan

批量获取知乎专栏。

```
//批量获取https://zhuanlan.zhihu.com/vinca520第三篇到最后一篇
python main.py zhihu_zhuanlan --i=vinca520 --start=3

//批量获取c:\a.txt文本文件下所有编号所示的专栏
python main.py zhihu_zhuanlan --f="c:\a.txt"
```

`c:\a.txt`文本文件。里面放着要下载的专栏的编号。分别用换行符隔开。

```
vinca520
alenxwn
```
#### 参数

- --i：知乎专栏的编号。如[https://zhuanlan.zhihu.com/vinca520](https://zhuanlan.zhihu.com/vinca520)的编号为“vinca520”
- --f：存放知乎专栏编号文本文件的路径。

可选参数：

- --start：开始篇数，如要从第五篇开始`--start=5`
- --end：结束篇数，如要第十篇结束`--end=10`
- --no-img：不下载图片
- --gif：下载gif
- --email：推送
- --window：每本电子书所含最大文章数，默认50

#### 配置

- SAVE_PATH：保存路径名。会自动在此目录以`collection_num`生产一个子目录，元数据即保存在此子目录中。

### zhihu_answers

批量获取知乎某人的全部回答。

```
//批量获取https://www.zhihu.com/people/zhong-wen-sen/answers第三篇到最后一篇
python main.py zhihu_answers --i=vinca520 --start=3

//批量获取c:\a.txt文本文件下所有答主的所有答案
python main.py zhihu_answers --f="c:\a.txt"
```

`c:\a.txt`文本文件。里面放着要下载的专栏的编号。分别用换行符隔开。

```
zhong-wen-sen
chen-zi-long-50-58
```

#### 参数

- --i：知乎答主的ID。如[https://www.zhihu.com/people/zhong-wen-sen/answers](https://www.zhihu.com/people/zhong-wen-sen/answers)的ID为“zhong-wen-sen”
- --f：存放知乎答主ID文本文件的路径。

可选参数：

- --start：开始篇数，如要从第五篇开始`--start=5`
- --end：结束篇数，如要第十篇结束`--end=10`
- --no-img：不下载图片
- --gif：下载gif
- --email：推送
- --window：每本电子书所含最大文章数，默认50

#### 配置

- SAVE_PATH：保存路径名。会自动在此目录以`collection_num`生产一个子目录，元数据即保存在此子目录中。

## 果壳
### guoke_scientific
批量获取果壳网科学人下的所有文章。

```
python main.py guoke_scientific
```
#### 参数

可选参数：

- --start：开始篇数，如要从第二十篇开始`--start=20`。
- --end：结束篇数，如要第四十篇结束`--end=40`
- --no-img：不下载图片
- --gif：下载gif
- --email：推送
- --window：每本电子书所含最大文章数，默认50

#### 配置

- SAVE_PATH：保存路径名。


## 好奇心日报

### qdaily

批量获取好奇心下的所有文章。

```
python main.py qdaily
```

#### 参数

可选参数：

- --start：开始日期，如`--start=2017-12-12`。默认今天。
- --end：结束篇数，如`--start=2017-12-12`。默认今天。因为是倒叙获取，`start`参数的日期必须大于或等于`end`参数的日期。
- --no-img：不下载图片。
- --gif：下载gif
- --i：制定类型，默认为`home`
  - home：首页
  - business：商业
  - intelligent：智能
  - design：设计
  - fashion：时尚
  - entertainment：娱乐
  - city：城市
  - game：游戏
  - long：长文章
- --email：推送
- --window：每本电子书所含最大文章数，默认50

#### 配置

- SAVE_PATH：保存路径名。

## 简书

### jianshu_wenji

批量获取某一简书文集下的所有文章。

```
python main.py jianshu_wenji --i=4431345
```

#### 参数

* --i：简书文集的ID。如`https://www.jianshu.com/nb/4431345`的ID为“4431345”

可选参数：

- --start：开始页，默认`1`。
- --end：结束页，默认无限。
- --no-img：不下载图片。
- --gif：下载gif
- --email：推送
- --window：每本电子书所含最大文章数，默认50
- --order_by：
  - seq：按目录排序（默认）
  - commented_at：按评论时间排序
  - added_at：按添加时间排序

#### 配置

- SAVE_PATH：保存路径名。

### jianshu_zhuanti

批量获取某一简书专题下的所有文章。

```
python main.py jianshu_zhuanti --i=1a54c5910458
```

#### 参数

* --i：简书专题的定位元素ID。如`https://www.jianshu.com/c/1a54c5910458`的定位元素ID为“1a54c5910458”

可选参数：

- --start：开始页，默认`1`。
- --end：结束页，默认无限。
- --no-img：不下载图片。
- --gif：下载gif
- --email：推送
- --window：每本电子书所含最大文章数，默认50
- --order_by：
  - top：按热门排序
  - commented_at：按评论时间排序
  - added_at：按添加时间排序（默认）

#### 配置

- SAVE_PATH：保存路径名。

### jianshu_user

批量获取某一简书专题下的所有文章。

```
python main.py jianshu_user --i=74307f7c1d61
```

#### 参数

* --i：简书用户的定位元素ID。如`https://www.jianshu.com/u/74307f7c1d61?utm_source=desktop&utm_medium=index-users`的定位元素ID为“74307f7c1d61”

可选参数：

- --start：开始页，默认`1`。
- --end：结束页，默认无限。
- --no-img：不下载图片。
- --gif：下载gif
- --email：推送
- --window：每本电子书所含最大文章数，默认50
- --order_by：
  - top：按热门排序
  - commented_at：按评论时间排序
  - added_at：按添加时间排序（默认）

#### 配置

- SAVE_PATH：保存路径名。

# TODO

- 天涯
- 修复GUI版添加配置项后需要重启的bug

# 更新日志

### 0.1.0.0

测试版第一版

### 0.1.0.1

- 修复了一直重试的Bug，默认重试次数为3。
- 文章里面可以显示作者、创建时间、赞数。
- 设置开始和结束的范围（page参数已荒废）。
- 修复了专栏倒叙的Bug。
- 配置文件更改为YAML格式。
- 可以修改`Download`和`Parser`的数量。

### 0.1.1.0

- Task注册功能（自动判断无任务）

### 0.1.1.1

- 无图模式
- 修复知乎公式无法显示的Bug
- 新增单独制作电子书命令行
- 修复重复文件名导致不能制作mobi的Bug

### 0.1.2.0

- 添加果壳网脚本
- 添加了Linux，Mac的支持

### 0.1.2.1

- 自动获取`KINDLEGEN_PATH`，配置文件里面不用写了
- 添加`WRITE_LOG`参数，可以自己选择写日志与否
- 添加`fix_mobi`脚本
- 修复了文件名太长而导致无法制作mobi的bug

### 0.1.2.2

- 添加"-dont_append_source"参数，大大减小mobi的体积

### 0.1.2.3

- 知乎前端更新

### 0.1.3.0

- 添加好奇心日报脚本
- 为减少体积。默认不下载gif。如需要下载加上`--gif`参数。

### 0.2.0.0

* 支持增量更新
* 修复很多bug
* 支持邮箱推送功能
* 新增了更人性化的目录
* 取消`fix_mobi`脚本
* 换行排版改进


### 1.0.0.0

* 添加了WebUI
* 修复Crawler里面线程不能被正确结束的bug
* 修正文章格式
* 修复防止文件名重复导致后缀名出错的bug

### 1.1.0.0

* 添加简书脚本
* WebUI可以设置脚本参数
* 修复了同一收藏夹不能获取多条相同问题答案的bug 
* 修复了"start""end"参数不能被正确处理的bug 
* 修复没有配置文件就退出的bug 