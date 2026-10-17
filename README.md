# Yuexin Light — Company Website

这是**岳鑫光电有限公司（Yuexin Optoelectronics Co., Ltd.）**的官网源码，基于 [BootstrapMade Alstar](https://bootstrapmade.com/alstar-free-parallax-bootstrap-template/) 模板定制。

主营：摇头灯、LED染色灯、LED效果灯、激光灯、舞台特效、控制台 —— 一站式舞台灯光采购。

## 本地预览

用 VS Code 打开本文件夹，安装 **Live Server** 插件，右键 `index.html` → "Open with Live Server" 即可实时预览。

或者直接用 Python 启动：

```bash
cd alstar-main
python -m http.server 8000
```

然后浏览器打开 http://localhost:8000

---

## 部署到 GitHub Pages（免费托管）

### 第 1 步：新建 GitHub 仓库

1. 注册/登录 https://github.com
2. 点右上角 **+** → **New repository**
3. Repository name 填：`yuexin-light.github.io`
   - ⚠️ 注意：这个名字必须是 `<你的用户名>.github.io`，比如你 GitHub 用户名是 `leo`，就填 `leo.github.io`
   - 这样仓库会自动发布到 `https://<用户名>.github.io`
4. 选 **Public**（公开，免费版必须公开）
5. 不要勾选 "Add a README"（我们已经有文件了）
6. 点 **Create repository**

### 第 2 步：把代码 push 到仓库

在本文件夹（alstar-main）里打开终端，运行：

```bash
git init
git add .
git commit -m "Yuexin Light website"
git branch -M main
git remote add origin https://github.com/<你的用户名>/<你的用户名>.github.io.git
git push -u origin main
```

> 如果还没装 Git：去 https://git-scm.com/download/win 下载安装，一路下一步即可。
> 第一次 push 会弹出浏览器让你登录 GitHub，按提示授权。

### 第 3 步：开启 GitHub Pages

1. 进入刚建的仓库页面
2. 点 **Settings** → 左侧 **Pages**
3. Source 选 **Deploy from a branch**
4. Branch 选 **main**，文件夹选 **/ (root)**
5. 点 **Save**
6. 等 1-2 分钟，页面上方会出现绿色提示：
   "Your site is live at https://<你的用户名>.github.io/"

### 第 4 步：绑定你的域名 www.yuexin-light.com

**A. 在 GitHub 这边：**
- 进入仓库 **Settings** → **Pages**
- 在 **Custom domain** 框里填：`www.yuexin-light.com`
- 点 **Save**
- ✅ 本仓库根目录下已经有一个 `CNAME` 文件，内容就是 `www.yuexin-light.com`，push 上去后 GitHub 会自动识别

**B. 在 GoDaddy（或你的域名商）这边加 DNS 记录：**

登录 GoDaddy → My Products → 你的域名 → DNS → Manage：

| 类型  | 主机(Name) | 值(Value) | 说明 |
|-------|-----------|-----------|------|
| CNAME | www       | `<你的用户名>.github.io` | 把 www 指向 GitHub |
| A     | @         | 185.199.108.153 | 根域名指向 GitHub Pages |
| A     | @         | 185.199.109.153 | GitHub Pages IP |
| A     | @         | 185.199.110.153 | GitHub Pages IP |
| A     | @         | 185.199.111.153 | GitHub Pages IP |

> 如果 GoDaddy 里已有其他 A 记录或 CNAME 记录指向旧主机，先删掉，避免冲突。

### 第 5 步：等待生效 + 开 HTTPS

1. DNS 生效一般需要几分钟到几小时
2. 回到 GitHub 仓库 **Settings → Pages**
3. 等 Custom domain 下方出现绿色对勾后，勾选 **Enforce HTTPS**
4. 浏览器访问 https://www.yuexin-light.com 即可看到你的网站

---

## 需要你替换的真实信息

打开 `index.html`，搜索以下关键词并替换：

| 搜索关键词 | 替换为 |
|-----------|--------|
| `[YOUR COMPANY ADDRESS]` | 你的工厂/办公室真实地址 |
| `[YOUR PHONE NUMBER]` | 你的电话/WhatsApp 号码 |
| `+86 [YOUR NUMBER]` | 同上 |
| `info@yuexin-light.com` | 你的真实邮箱（建议用企业邮箱） |
| 社交链接 `href="#"` | 你的 Facebook / LinkedIn / WhatsApp 主页链接 |

## 替换产品图片

把你的产品照片放到 `assets/img/portfolio/` 目录，替换掉 `portfolio-1.jpg` ~ `portfolio-9.jpg`（保持同名即可）。
轮播大图在 `assets/img/slide/`，替换 `slide-1.jpg` ~ `slide-3.jpg` —— 建议用舞台演出/夜店/演唱会现场大图，更有视觉冲击力。
关于我们配图 `assets/img/about-img.jpg` 建议换成工厂车间或展厅照片。

## 联系表单

当前表单提交地址是 `forms/contact.php`，但 GitHub Pages 是纯静态托管，不支持 PHP。
要让表单真的能收到询盘邮件，推荐用以下任一免费服务：
- **Formspree**（https://formspree.io）：注册后把 form 的 action 改成 `https://formspree.io/f/你的ID`
- **Netlify Forms**：如果以后迁到 Netlify 可以直接用

---

## 文件结构

```
alstar-main/
├── index.html          # 首页（主要改这个文件）
├── CNAME               # GitHub Pages 自定义域名配置
├── assets/
│   ├── css/style.css   # 样式
│   ├── img/            # 图片（轮播、产品、关于我们）
│   ├── js/main.js      # 交互脚本
│   └── vendor/         # Bootstrap 等第三方库（不用动）
└── forms/contact.php   # 联系表单后端（GitHub Pages 不生效，见上方说明）
```
