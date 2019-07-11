本仓库目的：

- email下载器，将邮件以eml文件格式备份到本地。
- python3多进程和多线程编程实践

使用方法：

编辑.pymotw文件，可以添加多个邮件地址，比如：
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

**注意account编号**

运行程序：

- python3 emaildownloader.py #多进程版本

说明：

- 只在python3，ubunut14环境下测试过
- 仅测试sina免费邮箱账户
