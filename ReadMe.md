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

![](.\微信截图_20240307125632.png)