# 部署手把手 —— 把技术文档站放到云服务器上

照着从上往下做就行。每一步都写了**你要敲的命令**和**你应该看到什么**，
看到的不一样就跳到最后的「出问题怎么查」。

整个过程大约 15 分钟。不需要你会 Linux。

---

## 开始之前：先准备这四样东西

| 需要什么 | 从哪来 | 长什么样 |
| --- | --- | --- |
| **服务器 IP** | 云服务器控制台首页能看到 | `47.98.123.45` |
| **登录用户名** | 一般是 `root` | `root` |
| **密码** | 买服务器时设置的那个 | 一串字符 |
| **云平台的控制台** | 阿里云 / 腾讯云 / 华为云的网站 | 网页 |

> **忘记密码了？** 在云平台控制台里找到这台服务器，有「重置密码」按钮，
> 重置后需要重启服务器生效。

---

## 第 1 步：连上服务器，顺便看清它是什么系统

### 1.1 打开 PowerShell

按 `Win + R`，输入 `powershell`，回车。会出现一个蓝色窗口。

### 1.2 连上去

把下面这行的 `47.98.123.45` 换成你的服务器 IP，粘贴进去，回车：

```powershell
ssh root@47.98.123.45
```

会出现两种情况：

**情况一**，第一次连接，问你信不信这台机器：

```
The authenticity of host '47.98.123.45' can't be established.
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```

输入 `yes` 回车。（这是在问你「确认连的是这台服务器吗」，第一次都要确认一次。）

**情况二**，直接让你输密码：

```
root@47.98.123.45's password:
```

> ⚠️ **输密码时屏幕上什么都不会显示** —— 不打星号、不动光标，这是正常的安全设计，
> 不是卡住了。正常输入然后直接按回车就行。

### 1.3 确认连上了

成功的话，前面的提示符会从 `PS C:\Users\...>` 变成类似这样：

```
root@iZbp1a2b3c4d5e:~#
```

看到这个就说明**你已经在那台服务器里面了**。接下来敲的命令都是在服务器上执行，
不是在你自己的电脑上。

### 1.4 查一下系统是什么

敲这条，回车：

```bash
cat /etc/os-release
```

会输出一串东西，**只需要看 `ID=` 那一行**：

| 你看到 | 走哪条路线 |
| --- | --- |
| `ID=ubuntu` 或 `ID=debian` | **A 路线** |
| `ID=centos`、`ID=kylin`、`ID=uos`、`ID=rhel`、`ID=almalinux`、`ID=rocky` | **B 路线** |
| 都没有 / 报错说找不到文件 | 把这行输出截图发我 |

> 阿里云/腾讯云最常见的两个选项：选「Ubuntu」买的就是 A 路线，
> 选「CentOS」买的就是 B 路线。

---

## 第 2 步：装 Nginx，并确认它自己能跑起来

Nginx 就是那个「把网站文件发给访问者」的服务器软件。这一步先把 Nginx 装好、
确认它本身没问题，**下一步再放我们的文件**。分两步走是为了出错时好定位 ——
是 Nginx 没装好，还是我们的文件没放对。

### A 路线（Ubuntu / Debian）

逐条敲，每条回车等它跑完再敲下一条：

```bash
apt update
```
```bash
apt install -y nginx
```

### B 路线（CentOS / 麒麟 / 统信）

```bash
yum install -y nginx
```

> 如果报错说 `No package nginx available`，先执行这条再重试：
> ```bash
> yum install -y epel-release
> ```

### 2.1 确认装好了

```bash
nginx -v
```

**你应该看到**：类似 `nginx version: nginx/1.18.0` 的一行。

### 2.2 启动它，并设置成开机自动启动

```bash
systemctl enable --now nginx
```
```bash
systemctl status nginx
```

**你应该看到**：一大段输出里有一行绿色的 `Active: active (running)`。

> 这个界面是「分页查看」模式，**按 `q` 键退出**，不然会卡在那里动不了。

### 2.3 现在就用浏览器验证一下

在你自己电脑上打开浏览器，地址栏输入：

```
http://你的服务器IP
```

比如 `http://47.98.123.45`

**你应该看到**：Nginx 的欢迎页面（写着 "Welcome to nginx!"）。

!!! warning "如果这一步就打不开，先别往下做"

    说明问题出在 Nginx 之前的环节（多半是端口没放行），
    跳到最后的 [**出问题怎么查 → 情况 1**](#情况-1-浏览器打不开这个网址)。
    先让这一步通了，再继续。

---

## 第 3 步：把你电脑上的 `site/` 文件夹传上去

⚠️ **先新开一个 PowerShell 窗口**（按 `Win + R` → `powershell`）。
连服务器那个窗口**不要关**，一会儿还要用。新窗口里**不要**再执行 `ssh`，
直接敲下面的命令 —— 这次是在你自己电脑上操作。

### 3.1 在服务器上建好放文件的目录

回到**连服务器的那个窗口**，敲：

```bash
mkdir -p /var/www
```

（`-p` 的意思是「已经有了就别报错」。这条不会有任何输出，没报错就是成功了。）

### 3.2 传文件

回到**新开的那个窗口**，敲下面这行（IP 换成你的）：

```powershell
scp -r "D:\UE5\Chemistry\aa\site" root@47.98.123.45:/var/www/aa-docs
```

这条命令的意思：把 `site` 这个文件夹，整个复制到服务器的 `/var/www/` 下面，
并命名为 `aa-docs`。

**你应该看到**：一行行文件名滚过去，大概几秒钟传完。最后回到提示符。

> 如果卡住不动：第一次连接会问 `yes/no`，输入 `yes` 回车；然后要输密码
> （同样不显示字符）。

### 3.3 确认传上去了

回到**连服务器的那个窗口**，敲：

```bash
ls /var/www/aa-docs
```

**你应该看到**：`index.html`、`404.html`、`assets`、`images`、`stylesheets` 等
一串名字。

如果报错说 `No such file or directory`，说明第 3.2 步没成功，重做一次。

---

## 第 4 步：告诉 Nginx「这个文件夹就是网站」

### 4.1 写配置文件

在**连服务器的窗口**里，把下面**一整块**复制粘贴进去，然后回车：

```bash
cat > /etc/nginx/conf.d/aa-docs.conf << 'EOF'
server {
    listen 80;
    server_name _;
    root /var/www/aa-docs;
    index index.html;
    charset utf-8;
    error_page 404 /404.html;
    location / {
        try_files $uri $uri/ =404;
    }
}
EOF
```

这条命令是「把 `EOF` 之间的内容写进一个配置文件」。不会有任何输出，
没报错就是成功了。

**关键的两行**：`root` 说明网站文件在哪，`index index.html` 说明「访问的是
目录时，返回里面的 index.html」——之前双击打不开、服务器却能打开，差别就在这行。

### 4.2 A 路线额外做一步：关掉 Nginx 自带的默认站点

Ubuntu 装完 Nginx 会自带一个占着 80 端口的示例站点，会和我们的打架。
**B 路线跳过这一步**。

```bash
rm -f /etc/nginx/sites-enabled/default
```

### 4.3 检查配置有没有写错

```bash
nginx -t
```

**你应该看到**：

```
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

看到 `test is successful` 才能往下做。如果报错，把报错内容发我。

### 4.4 让配置生效

```bash
systemctl reload nginx
```

没有任何输出就是成功了。

---

## 第 5 步：放行 80 端口（**最容易漏的一步**）

云服务器有两道门，都要打开：

### 5.1 云平台的安全组（必做）

打开你的云平台控制台网页：

- **阿里云**：找到这台服务器 → 「安全组」→「配置规则」→「入方向」→ 添加规则
  → 协议 `TCP`，端口 `80`，授权对象 `0.0.0.0/0`
- **腾讯云**：找到这台服务器 → 「安全组」→「入站规则」→ 添加规则
  → 类型 `HTTP (80)`，来源 `0.0.0.0/0`
- **华为云**：类似，找「安全组」→「入方向规则」

### 5.2 服务器自己的防火墙

**A 路线（Ubuntu）**：

```bash
ufw allow 80/tcp
```

（如果提示 `ufw: command not found`，说明没装 ufw，跳过即可。）

**B 路线（CentOS / 麒麟）**：

```bash
firewall-cmd --permanent --add-service=http
```
```bash
firewall-cmd --reload
```

---

## 第 6 步：验证

浏览器打开：

```
http://你的服务器IP
```

**你应该看到**：完整的文档站 —— 玻璃质感的顶栏、左侧导航、搜索框、
首页的「虚拟仿真化学实验教学软件」大标题。

试试点左侧导航、切换暗色模式、搜索一个词。**和你在本地双击
`本地预览.cmd` 看到的效果应该完全一样。**

把这个网址发给团队里的人，他们直接打开就能看。

---

## 以后怎么更新文档

改了 `docs/` 里的内容之后：

1. 在你电脑上双击 **`本地预览.cmd`**，先确认效果没问题
2. 删掉服务器上的旧版本 —— 在**连服务器的窗口**敲：
   ```bash
   rm -rf /var/www/aa-docs
   ```
3. 重新传一遍 —— 在**新开的 PowerShell 窗口**敲：
   ```powershell
   scp -r "D:\UE5\Chemistry\aa\site" root@你的服务器IP:/var/www/aa-docs
   ```

不用重启 Nginx，文件换了就直接生效。

> 第 2 步的 `rm -rf` 是**删掉旧文件**。不删也行，但那样已经删掉的页面会
> 残留在服务器上。每次重传前先删干净最省心。

---

## 出问题怎么查

### 情况 1：浏览器打不开这个网址

按顺序排查：

**① 服务器上的 Nginx 还活着吗？**

在连服务器的窗口敲：

```bash
systemctl status nginx
```

没有绿色 `active (running)` 就重新启动：

```bash
systemctl restart nginx
```

**② 服务器自己能不能打开？**

```bash
curl -I http://127.0.0.1
```

- 显示 `HTTP/1.1 200 OK` → Nginx 没问题，**是端口没放行 → 做第 5 步**
- 显示 `Connection refused` → Nginx 没跑起来 → 回到 ①
- 显示 `403 Forbidden` → 见情况 3

**③ 端口放行了吗？**

第 5 步的两道门（云平台安全组 + 服务器防火墙）**都要做**。
90% 的「打不开」都是漏了云平台的安全组 —— 因为它不在服务器上，
`systemctl` 查不到，很容易被忽略。

### 情况 2：打开是一堆文件名，不是网页

说明 Nginx 把目录列出来了，通常是因为**文件名不对**。

在连服务器的窗口敲：

```bash
ls /var/www/aa-docs
```

必须能看到 `index.html`。如果看到的是 **`site` 这个文件夹**，说明第 3.2 步
传多了一层，目录变成 `/var/www/aa-docs/site/` 了。两个办法：

- 把配置里的 `root /var/www/aa-docs;` 改成 `root /var/www/aa-docs/site;`，
  然后 `nginx -t && systemctl reload nginx`
- 或者干脆重传一次，注意命令最后的 `/var/www/aa-docs` 后面**不要**加斜杠

### 情况 3：显示 403 Forbidden

Nginx 没有权限读那个目录。在连服务器的窗口敲：

```bash
chmod -R 755 /var/www/aa-docs
```

### 情况 4：中文变成乱码

配置里已经有 `charset utf-8;` 了。确认一下第 4.1 步是整块复制进去的，
没有漏掉那一行。然后：

```bash
nginx -t && systemctl reload nginx
```

### 情况 5：`nginx -t` 报错

多半是第 4.1 步粘贴时内容不完整（比如漏了最后的 `EOF`）。
重新执行一次 4.1 那一整块即可，它会覆盖掉旧文件。

### 情况 6：样式全没了，只有光秃秃的文字

浏览器按 `F12` 打开开发者工具，看「网络 / Network」标签页里有没有红色的
404 错误。多半是文件没传全 —— 重新做第 3 步。

---

## 附：这套配置为什么这么写

| 配置行 | 作用 |
| --- | --- |
| `listen 80;` | 监听 80 端口，即 `http://` 默认端口 |
| `root /var/www/aa-docs;` | 网站文件所在目录 |
| `index index.html;` | 访问目录时返回里面的 index.html（目录式网址靠这行） |
| `charset utf-8;` | 声明编码，避免中文乱码 |
| `error_page 404 /404.html;` | 找不到页面时显示我们自己的 404 页 |
| `try_files $uri $uri/ =404;` | 先找同名文件，再找同名目录，都没有就返回 404 |

---

## 附：后面可以考虑的进阶项

- **绑域名 + HTTPS**：需要先有域名并解析到这台服务器。国内服务器还要先完成
  ICP 备案，否则 80/443 端口会被拦截。配好后 `certbot` 一条命令就能上 HTTPS。
- **只传改动而不是整个重传**：用 `rsync` 代替 `scp`，增量同步会快很多。
- **每次手动传太麻烦**：可以配 GitHub Actions，改成文档后自动部署，
  见 CLAUDE.md 里关于自动化部署的说明。
