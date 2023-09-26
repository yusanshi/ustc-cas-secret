# USTC CAS 密信

利用 USTC CAS 给同学展示密信（使用场景示例：你是助教，给学生自助查分）。

![image](https://github.com/yusanshi/ustc-cas-secret/assets/36265606/b47e4969-adb2-41f0-9288-d2f145facd9c)

## 快速开始

首先，在个人 USTC FTP 空间放入 `cas-redirect.html` 并对应修改 `backend.py` 中的 `REDIRECT_URL`（若其中的 `REDIRECT_URL` 正常可访问，你也可以省略这一步，即直接用我的 FTP 空间）；

接着，在你的服务器上执行以下操作：

1. `git clone https://github.com/yusanshi/ustc-cas-secret && cd ustc-cas-secret`
1. 创建 `data.json`，仿照 `data.sample.json` 在其中写入你想要展示给每个人的数据（学号中的字母大写，数据支持 HTML）；
3. `pip install fastapi "uvicorn[standard]"`；
4. `python backend.py`；
4. 设置反向代理绑定到 `http://127.0.0.1:8088`（如 Nginx 服务器使用 proxy_pass）。


## 致谢

- [zzh1996/ustccas-revproxy](https://github.com/zzh1996/ustccas-revproxy)
- [USTC-CAS-Redirect](https://github.com/volltin/USTC-CAS-Redirect)

