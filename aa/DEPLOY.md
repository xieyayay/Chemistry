# 部署方案 — 技术文档站上服务器

目标：把 `mkdocs` 生成的静态站点放到自有服务器上，团队成员开浏览器就能看。

---

## 一、总体思路

这个站点是**纯静态文件**（HTML / CSS / JS / 图片，没有后端、没有数据库、不需要
运行时）。所以部署的本质就是三步：

```
本地构建  →  上传 site/  →  Nginx 托管
```

三个关键取舍：

| 决定 | 选择 | 理由 |
| --- | --- | --- |
| 在哪构建 | **本地构建，只传产物** | 服务器不用装 Python/MkDocs；本仓库有 5GB 的 UE5 资源，服务器上根本不该拉整个仓库 |
| 传什么 | **只传 `site/` 目录**（约 6MB） | 传一次几秒钟 |
| 怎么发布 | **版本目录 + 软链接切换** | 上传过程中用户不会看到半截页面；出问题一条命令回滚 |

---

## 二、服务器端配置（一次性）

### 1. 装 Nginx

```bash
# Ubuntu / Debian
sudo apt update && sudo apt install -y nginx

# CentOS / RHEL / 麒麟
sudo yum install -y nginx
```

### 2. 建目录结构

```bash
sudo mkdir -p /var/www/aa-docs/releases
sudo chown -R "$USER":www-data /var/www/aa-docs   # CentOS 用 nginx 替换 www-data
```

结构长这样：

```
/var/www/aa-docs/
├── releases/
│   ├── 20260916-093000/     ← 每次发布的完整站点
│   └── 20260916-101500/     ← 上一次的还留着，随时能回滚
└── current -> releases/20260916-101500   ← Nginx 实际指向这里
```

### 3. Nginx 配置

新建 `/etc/nginx/conf.d/aa-docs.conf`（CentOS）或
`/etc/nginx/sites-available/aa-docs.conf`（Ubuntu）：

```nginx
server {
    listen 80;
    server_name _;                    # 有域名就填域名，没有就用 _

    root /var/www/aa-docs/current;
    index index.html;

    # 中文路径（站点里有些文件名是中文）——显式声明 UTF-8
    charset utf-8;

    # 静态资源压缩。HTML/CSS/JS 能压到原来的 1/4
    gzip on;
    gzip_comp_level 5;
    gzip_min_length 256;
    gzip_types text/plain text/css application/javascript application/json
               image/svg+xml application/xml;

    # 带哈希的构建产物可以长期缓存；HTML 不缓存，保证改完立刻可见
    location ~* \.(css|js|png|jpg|jpeg|gif|svg|woff2?)$ {
        expires 7d;
        add_header Cache-Control "public";
    }

    location / {
        try_files $uri $uri/ =404;
        add_header Cache-Control "no-cache";
    }

    # MkDocs 生成的 404 页面
    error_page 404 /404.html;
}
```

> **Ubuntu 用户注意**：默认站点 `/etc/nginx/sites-enabled/default` 会抢 80 端口，
> 先 `sudo rm /etc/nginx/sites-enabled/default`，再把自己的配置软链过去：
> `sudo ln -s /etc/nginx/sites-available/aa-docs.conf /etc/nginx/sites-enabled/`

### 4. 检查并启动

```bash
sudo nginx -t          # 语法检查，必须显示 successful
sudo systemctl enable --now nginx
sudo systemctl reload nginx
```

### 5. 放行端口

```bash
# Ubuntu
sudo ufw allow 80/tcp

# CentOS / RHEL
sudo firewall-cmd --permanent --add-service=http && sudo firewall-cmd --reload
```

### 6. 云服务器还要加安全组

阿里云/腾讯云/华为云的控制台里，给这台机器的**安全组**放行 80 端口
（这是最容易漏的一步：服务器本机防火墙开了，但云平台的安全组没开，外面照样连不上）。

---

## 三、发布流程（每次更新文档时）

### 方式 A：手工发布（推荐先用这个）

在项目根目录 `D:\UE5\Chemistry\aa\` 下：

```bash
# 1. 构建
mkdocs build --clean

# 2. 上传到服务器（把 user@server 换成实际地址）
STAMP=$(date +%Y%m%d-%H%M%S)
ssh user@server "mkdir -p /var/www/aa-docs/releases/$STAMP"
scp -r site/* user@server:/var/www/aa-docs/releases/$STAMP/

# 3. 切换软链接（原子操作，瞬间生效）
ssh user@server "ln -sfn /var/www/aa-docs/releases/$STAMP /var/www/aa-docs/current"

# 4. 保留最近 5 个版本，其余删掉
ssh user@server "ls -1dt /var/www/aa-docs/releases/* | tail -n +6 | xargs -r rm -rf"
```

回滚就是把软链接指回上一个版本：

```bash
ssh user@server "ln -sfn /var/www/aa-docs/releases/<上一个版本> /var/www/aa-docs/current"
```

### 方式 B：写成一个脚本

把上面 4 步存成 `deploy.sh` 放项目根目录，以后一条 `./deploy.sh` 搞定。
要不要我写这个脚本，你说了算。

---

## 四、可选增强

### 绑域名 + HTTPS

需要先有域名并解析到服务器 IP：

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d docs.example.com
```

certbot 会自动改 Nginx 配置、申请证书、配置 90 天自动续期。

> 如果服务器在**国内**，域名指向国内 IP 需要先完成 **ICP 备案**，否则 80/443 会被
> 拦截。只在公司内网/校园网用的话，直接用 `http://内网IP` 就行，不用备案。

### 内网访问

如果服务器没有公网 IP，只能内网访问，那 `server_name` 填内网 IP 或不管它，
团队成员用 `http://192.168.x.x` 访问即可。上面所有配置都不需要改。

---

## 五、需要你提供的信息

要我把上面的东西落地成可执行脚本、并实际跑一遍，需要知道：

1. **服务器操作系统** —— Ubuntu / CentOS / 麒麟 / Windows Server？
2. **网络** —— 有公网 IP 吗？还是只能内网访问？内网的话 IP 段是什么？
3. **登录方式** —— SSH 的用户名和地址（`user@ip`）。密码/密钥不用给我，你自己在
   终端里执行我给的命令即可。
4. **Nginx 装了吗** —— 还是从零开始？
5. **域名** —— 有没有打算绑域名？有的话解析做了吗？

---

## 六、上线前要决定：这几个页面要不要公开发布

`docs/` 下有 4 个文件不在 `mkdocs.yml` 的 `nav` 里，但 **MkDocs 仍然会把它们构建成
HTML，并收进站内搜索和 sitemap** —— 也就是说，部署之后任何人只要搜一下或猜一下
网址就能看到：

| 文件 | 内容 | 建议 |
| --- | --- | --- |
| `docs/文档维护说明.md` | 内部维护流程，含给 AI 用的提示词 | **不建议公开**，移到 `docs/` 外面 |
| `docs/_template.md` | 新页面的空白模板 | 不建议公开 |
| `docs/打开网页.md` | 本地怎么看文档 | 站点上线后这份说明就过时了，可删 |
| `docs/ui/task-system.md` | 和 `docs/systems/task-system.md` 内容重复 | 建议删掉其中一个 |

处理方式：把不想发布的那几个 `.md` 移出 `docs/`（比如放到项目根的 `notes/`），
它们就不会再被构建。MkDocs 本身没有「排除某个文件」的配置项，移出去是最干净的
做法。

> 这一条要不要做、怎么做，你定。定之前我不会动这些文件。

---

## 七、顺带一个建议：`site/` 不该进 Git

现在 `site/`（构建产物）是被 Git 跟踪的，有两个副作用：

- 每次改文档，Git 里会多出十几个 HTML 文件的 diff，真正的改动（`docs/*.md`）被淹没；
- `site/ui.zip` 这种手工放进去的文件，会被 `mkdocs build --clean` 清掉
  （这次执行构建时就发生了一次，已恢复）。

建议：

```bash
git rm -r --cached site          # 停止跟踪，但保留本地文件
echo "site/" >> .gitignore
git commit -m "构建产物移出版本控制"
```

这样 `site/` 就纯粹是本地构建输出，服务器上也不需要它进仓库。
