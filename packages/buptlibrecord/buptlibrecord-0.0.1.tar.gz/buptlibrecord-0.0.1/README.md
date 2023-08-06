# BUPT Library Record Backup

用于导出个人北邮图书馆图书借阅记录。跨平台，但仅支持 Python 3。

需要输入使用学工号和密码登录北邮统一身份认证后的 Cookie中的 `JSESSIONID`，然后程序会自动导出全部的图书借阅记录并保存到文件，将会生成 3 个文件，包含原始数据的 json 格式文件，借阅过的图书列表，借阅日志（包含借阅，续借和还书三种操作）

## 如何获取 JSESSIONID

1. 登录北邮统一身份认证
   如网址 my.bupt.edu.cn
   
2. 按 F12 打开开发者工具

3. 在 FireFox 浏览器点击存储（Store）选项卡，Chrome 或 Edge 浏览器点击应用选项卡，再点击展开 Cookie


4. 查看Cookie中 JSESSIONID 的值

Firefox：
![image.png](https://i.loli.net/2021/06/24/YpyZfhG5sIutiUo.png)

Edge / Chrome：

![image.png](https://i.loli.net/2021/06/24/AuWrHKERSeyCtX6.png)

## 安装

直接使用 pip 安装

`pip install buptlibrecord`

## 使用

登录 `buptlibrecord JSESSIONID` 


### 在 python 中调用

```python
import buptlibrecord

book_info_list, totalPage, total_count = buptlibrecord.get_all_record_list(JSESSIONID) 

```
