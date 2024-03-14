# 接口+UI自动化集成框架

​    简介：本框架集成了接口自动化及UI自动化功能，采用pytest+requests+selenium+yaml+allure搭建。接口自动化测试支持ddt和场景关联测试，UI自动化采用pageFactory模式。

## 接口自动化使用介绍

​    执行入口run_case.py,执行时会去pytest.ini中查找配置testpaths指定测试用例文件目录。

​     testcase文件夹存放用例文件,单接口采用数据驱动，.yml存放待测试接口，格式：

```yaml
-
  feature: api post测试
  story: 单接口数据驱动
  title: jsonplaceholder post接口
  parametrize:
    name-title-userId-assertion: \data_storage\ddt.yml
  request:
    origin: https://jsonplaceholder.typicode.com
    url: /posts
    header:
      Content-type: application/json; charset=UTF-8
    method: post
    param:
      title: $ddt{title}
      userId: $ddt{userId}
      id: 1
  validator:
    equal: $ddt{assertion}
  extract:
```

   feature story title parametrize request validator extract为固定字段，parametrize格式为 存放的数据的字段和数据存放路径。参数化的数据用$文件名{字段名}格式。

​    数据存放格式如下：

```yaml
#  \data_storage\ddt.yml
- [name, title, userId, assertion]
- [单接口正常响应, my title, 1, 200]
- [单接口失败验证, title2, 2, 400]
```

  优点： 对测试人员代码能力要求低，数据管理方便。

关联接口测试,关联接口需要写在相同的yml文件中，接口格式如下:

```yaml
-
  feature: api get测试
  story: jsonplaceholder请求返回
  request:
    origin: https://jsonplaceholder.typicode.com
    url: /posts/1
    header:
      Content-type: application/json; charset=UTF-8
#      secret-key: ede1b49708821e0b7bacaa3077db0dbd
    method: get
    param:
  validator:
    equal:
      id: 1
  extract:
    - userId

-
  feature: api post测试
  story: 变量获取测试
  request:
    origin: https://jsonplaceholder.typicode.com
    url: /posts
    header:
      Content-type: application/json; charset=UTF-8
#      secret-key: ede1b49708821e0b7bacaa3077db0dbd
    method: post
    param:
      title: july
      userId: ${userId}
      id: 1
  validator:
    title: july
  extract:
```



extract中填入需要提取的字段名,在要使用的接口中使用${xxx}调用

测试执行完成自动生成allure报告，最终执行效果：











# ReadMe

​       本项目采用python+requests+yaml+pytest+allure实现接口自动化测试框架，同时集成了UI自动化测试框架（未完善）。二次封装requests来发送和处理Http协议的请求接口，Yaml管理测试用例，pytest作为测试执行器，allure生成测试报告。

 ## 项目说明

   本项目整体分为几个部分，MyRequests对http请求进行二次封装，实现日志记录，解析请求参数，提取中间变量，接口响应断言等功能。yamlutil用于关联接口用例处理测试数据的读取，字段规范性校验，变量存储。ddt针对单接口用例数据驱动，对数据和用例进行规范化读取和处理。yaml测试用例及测试数据使用yaml格式管理，存放在testcase文件夹下。

* 对于单接口测试用例需包含一下字段

```yaml
-  
  feature: api post测试
  story: 单接口数据驱动
  title: jsonplaceholder post接口
  parametrize: 
    name-title-userId-assertion: \data_storage\ddt.yml     # \data_storage\ddt.yml为数据存储位置。文件需存放在testcase目录下。name-title-userId-assertion 代表测试数据中参数化的字段，需一一对应
  request:
    origin: https://jsonplaceholder.typicode.com      
    url: /posts
    header:
      Content-type: application/json; charset=UTF-8   
    method: post
    param: 
      title: $ddt{title}     # 参数化的数据提取需使用$filename{key}的方式
      userId: $ddt{userId}
      id: 1
  validator:
    equal: $ddt{assertion}     # 断言。支持的断言关键字有 equal，unequal, contain，exclude
  extract:              # 中间变量提取字段，若需提取响应中的值，需按照key: value的方式编写
```

测试数据存放如下

```yam
- [name, title, userId, assertion]
- [单接口正常响应, my title, 1, 200]
- [单接口失败验证, title2, 2, 400]
```

​      对于测试用例编写人员来说，只需要编写一次接口yaml文件，规定数据存放位置和参数化的内容，接口测试数据可独立交由其他人员填写。

​     测试执行文件只需如此编写, 一个类为一个测试套件，对于套件内的不同接口，需要编写对应的请求方法，用例传入@pytest.mark.parametrize中。

```python
import pytest
from myutils.myRequests import MyRequests
import allure
from myutils import ddt

class Test_Single:
    @allure.feature("单接口数据驱动")
    @pytest.mark.parametrize("url, header, method, param, expect, extract, feature, story",ddt.read_testcase("json_get_test.yml"))
    def test_single_api_demo(self, url, header, method, param, expect,extract, feature, story ,cleanup):

        MyRequests().send_requests(method, url,
                                   header=header,
                                   param = param,
                                   expect = expect,
                                   extract = extract,
                                   feature = feature,
                                   story = story)
```



* 对于关联接口，暂不支持数据驱动。关联接口需写在同一个yaml文件中，extract中以key:value方式写入要提取的中间变量，value提取来自此接口的响应数据，解析方式以jsonpath方式访问。要在其他接口使用该变量，采用${key}方式

  ```yaml
  -
    feature: 微博接口正常响应
    story: 微博热搜
    title: 2
    request:
      origin: https://www.coderutil.com
      url: /api/resou/v1/weibo
      header:
        access-key: 69c7a49f5a60ac2447cc2087347c4abe
        secret-key: ede1b49708821e0b7bacaa3077db0dbd
      method: get
      param: None
    validator:
      exclude:
        code: 200
    extract:
      keyword: $.data[0].keyword
  -
    feature: api post测试
    story: 变量获取测试
    request:
      origin: https://jsonplaceholder.typicode.com
      url: /posts
      header:
        Content-type: application/json; charset=UTF-8
      method: post
      param:
        title: july
        userId: ${keyword}
        id: 1
    validator:
      title: july
    extract:
  ```

  

测试的执行可运行run_case.py, 测试用例执行会按照pytest.ini中testpaths指定的目录下寻找测试用例执行。执行完成后生成allure报告。

## 项目部署

本项目需在python3环境下运行。下载项目源码后，在根目录下找到requirements.txt文件，通过pip安装依赖。执行命令

```pyt
pip install -r requirements.txt
```

## 项目结构

* log                       ----------->存放日志文件
* myutils                ----------->工具类，包含二次封装的请求类，验证类，yaml处理等
* testcase              ------------>用例文件，包含驱动数据，测试用例
* temp                   ------------>存放中间变量
* reports                ------------> 测试报告
* temps                 ------------>allure生成的临时文件
* pytest.ini             ------------>pytest配置文件
* run_case.py       ------------>测试执行入口

## 测试报告效果展示



![](E:\WorkPlace\pytest-course\report.png)
