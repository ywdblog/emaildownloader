### 本仓库目的

- email下载器，将邮件以eml文件格式备份到本地
- python3多进程和多线程编程实践（会陆续更新公众号文章）

### 使用方法

编辑.pymotw文件，可以添加多个邮件地址（account编号递增），比如：

```
[account1]
hostname=imap.sina.com.cn
port=993
username=
password=

[account2]
hostname=imap.sina.com.cn
port=993
username=
password=
```

### 运行程序

- python3 e_multiprocessing.py #多进程版本
- python3 e_threading.py #多线程版本

### 说明

- 只在python3，linux环境下测试过
- 仅测试过sina免费邮箱账户

### 相关文章

- [一个email下载器：多进程思路](https://mp.weixin.qq.com/s/i5qJ7REqdelR2y2NFF8mlg)
- [一个email下载器：多进程编程中遇到的问题](https://mp.weixin.qq.com/s/oqDL76g1su9ZP-BaTbNU_A)
