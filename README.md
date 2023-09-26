# USTC CAS 密信

利用 USTC CAS 给同学展示密信（使用场景示例：你是助教，给学生自助查分）。

![image](https://github.com/yusanshi/ustc-cas-secret/assets/36265606/d47ffd4b-3a79-46db-95a1-0234fbe29a2f)


## 快速开始

在你的服务器上执行以下操作：

1. `git clone https://github.com/yusanshi/ustc-cas-secret && cd ustc-cas-secret`
1. 创建 `data.json`，仿照 `data.sample.json` 在其中写入你想要展示给每个人的数据（学号中的字母大写，数据支持 HTML）；
3. `pip install fastapi "uvicorn[standard]"`；
4. `python backend.py`；
4. 设置反向代理绑定到 `http://127.0.0.1:8088`（如 Nginx 服务器使用 proxy_pass）。

## 原理解析

### 常规 CAS 认证过程

> “常规”指你有一个 ustc.edu.cn 的二级域名：foobar.ustc.edu.cn。

1. 用户访问 https://passport.ustc.edu.cn/login?service=https://foobar.ustc.edu.cn/something （这里的 service 要求其中的 host 以 ustc.edu.cn 结尾）
2. 登录成功后，自动跳转到 `service` 并将在末尾 append 上 ticket：https://foobar.ustc.edu.cn/something?ticket=ST-XXXXXXX
3. 你作为 foobar.ustc.edu.cn 所有人，可以根据拿到的 ticket 从 https://passport.ustc.edu.cn/serviceValidate 获取用户信息（GID、学号等）

### Hack CAS 认证过程

> 显然，我们往往没有这样的二级域名，因此我们需要 hack。

#### 思路一

利用个人 FTP 空间 `home.ustc.edu.cn`，下面的“致谢”的项目即是这个思路。

#### 思路二

利用漏洞。具体来说，前文的 `这里的 service 要求其中的 host 以 ustc.edu.cn 结尾` 实际实现的逻辑是 `if ".ustc.edu.cn/" in service`，所以我们可以将 `service` 选为 `https://example.com/www.ustc.edu.cn/` 或 `https://example.com/?query=.ustc.edu.cn/`。本项目用的就是这个思路。

## 致谢

- [zzh1996/ustccas-revproxy](https://github.com/zzh1996/ustccas-revproxy)
- [volltin/USTC-CAS-Redirect](https://github.com/volltin/USTC-CAS-Redirect)

