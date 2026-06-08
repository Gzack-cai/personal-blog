# 个人博客 — 项目说明文档

> 赛博朋克科技风个人品牌展示网站 | 全栈项目  

---

## 目录

1. [项目简介](#1-项目简介)
2. [技术栈](#2-技术栈)
3. [项目结构](#3-项目结构)
4. [快速启动](#4-快速启动)
5. [后端（FastAPI）](#5-后端fastapi)
6. [前端（Vue3）](#6-前端vue3)
7. [音乐服务](#7-音乐服务)
8. [数据库设计](#8-数据库设计)
9. [API 接口文档](#9-api-接口文档)
10. [管理后台](#10-管理后台)
11. [常见问题](#11-常见问题)

---

## 1. 项目简介

一个**赛博朋克科技风**的个人品牌展示网站，包含以下功能模块：

- **个人介绍** — 展示个人信息、技能标签、联系方式
- **项目展示** — 作品集展示，带技术栈标签
- **文章归档** — 链接到外部博客（CSDN 等）的文章列表
- **精彩生活** — 3D 网状球体交互的生活动态记录
- **在线音乐** — 基于网易云 API 的在线音乐播放器（含歌词）
- **我的好友** — 友情链接展示
- **联系我** — 访客留言表单
- **管理后台** — 密码保护的内容管理系统（CRUD）

### 设计特点

- 🎨 赛博朋克霓虹风格，动态渐变 + 发光效果
- 🌓 支持深色/浅色主题切换
- ✨ 粒子动画背景 + 扫描线效果
- 📱 响应式布局
- 🎵 全局浮动歌词面板（除音乐页面外）

---

## 2. 技术栈

### 前端

| 技术 | 用途 |
|------|------|
| **Vue 3** (Composition API + `<script setup>`) | 前端框架 |
| **Vue Router** | 前端路由 |
| **Vue I18n** | 国际化（中/英） |
| **Axios** | HTTP 请求（API 封装） |
| **Vite** | 构建工具 |
| **CSS Variables** | 主题系统（深色/浅色） |

### 后端

| 技术 | 用途 |
|------|------|
| **FastAPI** | Python Web 框架 |
| **SQLAlchemy** | ORM 数据库操作 |
| **PyMySQL** | MySQL 数据库驱动 |
| **Pydantic** | 数据验证与序列化 |
| **Uvicorn** | ASGI 服务器 |

### 数据库

- **MySQL 8.0**（字符集 `utf8mb4`）

### 第三方服务

- **NeteaseCloudMusicApi** — 网易云音乐 API（搜索、播放、歌词）

---

## 3. 项目结构

```
D:\A_Project\Blog\
├── backend/                     # FastAPI 后端
│   ├── main.py                  # 应用入口，路由注册
│   ├── config.py                # 数据库配置
│   ├── database.py              # SQLAlchemy 引擎 & 会话
│   ├── models.py                # ORM 模型定义
│   ├── schemas.py               # Pydantic 请求/响应模型
│   ├── requirements.txt         # Python 依赖
│   └── routers/                 # API 路由
│       ├── __init__.py
│       ├── profile.py           # 个人介绍
│       ├── projects.py          # 项目展示
│       ├── articles.py          # 文章归档
│       ├── life.py              # 精彩生活
│       ├── friends.py           # 友链
│       └── contact.py           # 联系留言
│
├── frontend/                    # Vue3 前端
│   ├── index.html               # HTML 入口
│   ├── package.json             # 前端依赖
│   ├── vite.config.js           # Vite 配置（含代理）
│   └── src/
│       ├── main.js              # Vue 入口 & 路由注册
│       ├── App.vue              # 根组件（导航 + 粒子 + 主题）
│       ├── player.js            # 全局音乐播放器状态
│       ├── api/
│       │   └── index.js         # Axios API 封装
│       ├── router/
│       │   └── index.js         # 路由配置
│       ├── i18n/
│       │   └── index.js         # 国际化配置
│       ├── locales/
│       │   ├── zh.json          # 中文语言包
│       │   └── en.json          # 英文语言包
│       ├── styles/
│       │   ├── variables.css    # CSS 变量（已迁移至 App.vue）
│       │   └── global.css       # 全局样式（已迁移至 App.vue）
│       ├── views/               # 页面视图
│       │   ├── Profile.vue      # 个人介绍
│       │   ├── Projects.vue     # 项目展示
│       │   ├── Articles.vue     # 文章归档
│       │   ├── Life.vue         # 精彩生活（3D 球体交互）
│       │   ├── Music.vue        # 音乐播放器
│       │   ├── Friends.vue      # 友链
│       │   ├── Contact.vue      # 联系表单
│       │   └── Admin.vue        # 管理后台
│       └── components/          # 复用组件
│           ├── LyricsPanel.vue  # 全局浮动歌词面板
│           ├── MusicPlayer.vue  # (未使用)
│           └── NavBar.vue       # (未使用)
│
├── music-server/                # 音乐代理服务
│   ├── package.json
│   └── server.js                # NeteaseCloudMusicApi 启动脚本
│
├── sql/
│   └── init.sql                 # 数据库建表 & 示例数据
│
├── search.json                  # 搜索数据缓存
└── docs/
    └── project-overview.md      # 本文档
```

---

## 4. 快速启动

### 4.1 环境要求

- Node.js 18+
- Python 3.10+
- MySQL 8.0+

### 4.2 启动步骤

**第一步：初始化数据库**

```bash
mysql -u root -p --default-character-set=utf8mb4 < sql/init.sql
```

**第二步：启动后端**

```bash
cd backend
pip install -r requirements.txt
python main.py
# 服务运行在 http://localhost:8000
```

**第三步：启动音乐服务**

```bash
cd music-server
npm install
PORT=3001 node server.js
# 服务运行在 http://localhost:3001
```

**第四步：启动前端**

```bash
cd frontend
npm install
npm run dev
# 服务运行在 http://localhost:5173
```

### 4.3 访问页面

| 页面 | URL |
|------|-----|
| 首页（个人介绍） | `http://localhost:5173/profile` |
| 项目展示 | `http://localhost:5173/projects` |
| 文章归档 | `http://localhost:5173/articles` |
| 精彩生活 | `http://localhost:5173/life` |
| 音乐播放器 | `http://localhost:5173/music` |
| 好友链接 | `http://localhost:5173/friends` |
| 联系我 | `http://localhost:5173/contact` |
| 管理后台 | `http://localhost:5173/admin` |

---

## 5. 后端（FastAPI）

### 5.1 配置 (`config.py`)

```python
DATABASE_URL = "mysql+pymysql://root:1234@localhost:3306/personal_blog"
HOST = "0.0.0.0"
PORT = 8000
```

### 5.2 ORM 模型 (`models.py`)

共 6 个模型类：

| 模型 | 表名 | 说明 |
|------|------|------|
| `Profile` | `profile` | 个人介绍（单行） |
| `Project` | `projects` | 项目作品 |
| `Article` | `articles` | 文章归档 |
| `LifeMoment` | `life_moments` | 生活动态 |
| `Friend` | `friends` | 友链 |
| `ContactMessage` | `contact_messages` | 联系留言 |

启动时 `main.py` 自动调用 `Base.metadata.create_all()` 建表。

### 5.3 依赖

```
fastapi==0.104.0
uvicorn==0.24.0
sqlalchemy==2.0.23
pymysql==1.1.0
python-dotenv==1.0.0
pydantic==2.5.2
```

### 5.4 中间件

- CORS 全开放（`allow_origins=["*"]`）

---

## 6. 前端（Vue3）

### 6.1 页面路由

| 路径 | 页面 | 说明 |
|------|------|------|
| `/` | 重定向 | → `/profile` |
| `/profile` | Profile | 个人介绍 |
| `/projects` | Projects | 项目展示 |
| `/articles` | Articles | 文章归档 |
| `/life` | Life | 3D 网状球体交互 |
| `/music` | Music | 在线音乐播放器 |
| `/friends` | Friends | 友情链接 |
| `/contact` | Contact | 联系表单 |
| `/admin` | Admin | 管理后台 |

### 6.2 全局组件

**App.vue** — 根组件功能：
- 粒子动画背景（Canvas）
- 赛博朋克扫描线效果
- 导航栏（含迷你播放器）
- 深色/浅色主题切换
- 全局歌词面板 LyricsPanel
- 页面过渡动画

**LyricsPanel.vue** — 全局浮动歌词：
- 固定在页面右侧（260px 宽）
- 歌词滚动高亮
- 仅非 `/music` 页面显示

### 6.3 全局播放器 (`player.js`)

基于 `Audio` API 实现的全局音乐播放器：

| 功能 | 说明 |
|------|------|
| 播放/暂停 | `togglePlayPause()` |
| 歌曲切换 | `playSong(song)` |
| 歌词解析 | 解析 LRC 格式歌词 |
| 进度控制 | `seek(time)` |
| 音量控制 | `setVolume(val)` |
| 默认歌曲 | 筷子兄弟《老男孩》 |
| 数据源 | 网易云音乐 API |

播放器状态通过 `reactive` 全局共享：
```javascript
player = {
  currentSong, currentSongId, isPlaying,
  currentTime, duration, volume,
  lyrics[], currentLyricIdx
}
```

### 6.4 主题系统

通过 CSS 变量实现深色/浅色切换：

```css
:root { /* 深色主题 */ }
html.light-mode, .light-mode { /* 浅色主题 */ }
```

切换逻辑：`localStorage.getItem('theme')` 持久化用户偏好。

### 6.5 国际化

支持中英文切换，语言包位于 `src/locales/`，通过 Vue I18n 管理。

### 6.6 Vite 开发代理

```javascript
// vite.config.js
proxy: {
  '/api':        { target: 'http://localhost:8000', changeOrigin: true },
  '/music-api':  { target: 'http://localhost:3001', rewrite: path => path.replace(/^\/music-api/, '') },
}
```

---

## 7. 音乐服务

基于 `NeteaseCloudMusicApi` 的网易云音乐 API 代理。

### 7.1 启动方式

```bash
cd music-server
npm install
PORT=3001 node server.js
```

### 7.2 前端调用接口

| 功能 | 前端调用路径 | 说明 |
|------|-------------|------|
| 搜索歌曲 | `/music-api/search?keywords=xxx&limit=30` | 搜索 |
| 获取播放 URL | `/music-api/song/url/v1?id=xxx&level=standard` | 播放 |
| 获取歌词 | `/music-api/lyric?id=xxx` | 显示歌词 |

---

## 8. 数据库设计

### 8.1 概览

| 项目 | 内容 |
|------|------|
| 数据库名 | `personal_blog` |
| 表数量 | 6 |
| 字符集 | `utf8mb4` |
| 排序规则 | `utf8mb4_unicode_ci` |

### 8.2 表结构

#### `profile` — 个人介绍（单行）

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | INT PK | 主键 |
| `name` | VARCHAR(100) | ⚠️ 必填 |
| `title` | VARCHAR(200) | ⚠️ 必填 |
| `avatar` | VARCHAR(500) | 头像 URL |
| `bio` | TEXT | 个人简介 |
| `skills` | TEXT | JSON 数组，如 `["Python","Vue"]` |
| `email` | VARCHAR(200) | 邮箱 |
| `phone` | VARCHAR(50) | 电话 |
| `github` | VARCHAR(500) | GitHub |
| `bilibili` | VARCHAR(500) | 哔哩哔哩 |
| `csdn` | VARCHAR(500) | CSDN |
| `wechat` | VARCHAR(200) | 微信 |
| `qq` | VARCHAR(50) | QQ |
| `created_at` | DATETIME | 默认当前时间 |
| `updated_at` | DATETIME | 自动更新 |

#### `projects` — 项目展示

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | INT PK | 主键 |
| `title` | VARCHAR(200) | ⚠️ 必填 |
| `description` | TEXT | 项目描述 |
| `image` | VARCHAR(500) | 截图 URL |
| `tech_stack` | TEXT | JSON 数组 |
| `demo_url` | VARCHAR(500) | 演示链接 |
| `github_url` | VARCHAR(500) | 源码链接 |
| `sort_order` | INT | 排序（默认 0） |
| `created_at` | DATETIME | 创建时间 |
| `updated_at` | DATETIME | 更新时间 |

#### `articles` — 文章归档

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | INT PK | 主键 |
| `title` | VARCHAR(200) | ⚠️ 必填 |
| `summary` | TEXT | 摘要 |
| `url` | VARCHAR(500) | ⚠️ 原文链接 |
| `date` | DATE | 发布日期 |
| `sort_order` | INT | 排序 |
| `created_at` | DATETIME | 创建时间 |

#### `life_moments` — 精彩生活

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | INT PK | 主键 |
| `title` | VARCHAR(200) | 标题 |
| `content` | TEXT | 内容 |
| `image` | VARCHAR(500) | 配图 |
| `date` | DATE | 日期 |
| `created_at` | DATETIME | 创建时间 |

#### `friends` — 友链

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | INT PK | 主键 |
| `name` | VARCHAR(100) | ⚠️ 必填 |
| `avatar` | VARCHAR(500) | 头像 |
| `description` | TEXT | 简介 |
| `blog_url` | VARCHAR(500) | ⚠️ 博客链接 |
| `sort_order` | INT | 排序 |
| `created_at` | DATETIME | 创建时间 |

#### `contact_messages` — 联系留言

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | INT PK | 主键 |
| `name` | VARCHAR(100) | ⚠️ 必填 |
| `email` | VARCHAR(200) | ⚠️ 必填 |
| `message` | TEXT | ⚠️ 必填 |
| `created_at` | DATETIME | 提交时间 |

### 8.3 表关系

各表之间**独立无外键**，解耦设计，方便模块替换。

### 8.4 初始化脚本

完整建表 + 示例数据见 `sql/init.sql`。

---

## 9. API 接口文档

### Profile

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/profile` | 获取个人介绍 |
| PUT | `/api/profile` | 更新个人介绍 |

### Projects

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/projects` | 获取项目列表 |
| POST | `/api/projects` | 新增项目 |
| PUT | `/api/projects/{id}` | 更新项目 |
| DELETE | `/api/projects/{id}` | 删除项目 |

### Articles

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/articles` | 获取文章列表 |
| POST | `/api/articles` | 新增文章 |
| PUT | `/api/articles/{id}` | 更新文章 |
| DELETE | `/api/articles/{id}` | 删除文章 |

### Life

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/life` | 获取生活动态列表 |
| POST | `/api/life` | 新增动态 |
| PUT | `/api/life/{id}` | 更新动态 |
| DELETE | `/api/life/{id}` | 删除动态 |

### Friends

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/friends` | 获取友链列表 |
| POST | `/api/friends` | 新增友链 |
| PUT | `/api/friends/{id}` | 更新友链 |
| DELETE | `/api/friends/{id}` | 删除友链 |

### Contact

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/contact` | 获取留言列表（管理员） |
| POST | `/api/contact` | 提交留言 |
| DELETE | `/api/contact/{id}` | 删除留言 |

### 通用响应格式

```json
{
  "code": 200,
  "message": "success",
  "data": [...]  // 或 null
}
```

---

## 10. 管理后台

### 10.1 访问

路径：`/admin`

### 10.2 登录

默认密码：**`admin123`**

（密码硬编码在 `Admin.vue` 中，可按需修改）

### 10.3 管理功能

| 标签 | 功能 |
|------|------|
| 个人介绍 | 编辑姓名、头衔、头像、技能标签、联系方式、简介 |
| 项目 | 新增/编辑/删除项目卡片 |
| 文章 | 新增/编辑/删除文章记录 |
| 精彩生活 | 新增/编辑/删除生活动态 |
| 好友 | 新增/编辑/删除友情链接 |
| 留言 | 查看/删除访客留言 |

认证状态保存在 `sessionStorage`，关闭标签页后失效。

---

## 11. 常见问题

### Q: 数据库连接失败？

- 检查 MySQL 是否已启动
- 检查 `config.py` 中的连接信息
- 确认已执行 `sql/init.sql`

### Q: 音乐无法播放？

- 确认 `music-server` 已启动（端口 3001）
- 网易云 API 部分歌曲有版权限制，可能无法播放
- Vite 代理配置是否正确（`/music-api` → `localhost:3001`）

### Q: 管理后台无法加载数据？

- 确认后端已启动
- 检查 Vite 代理是否生效（`/api` → `localhost:8000`）

### Q: 如何修改管理后台密码？

编辑 `frontend/src/views/Admin.vue`，修改 `ADMIN_PASSWORD` 的值。

### Q: 如何更换默认歌曲？

编辑 `frontend/src/player.js`，修改 `defaultSong` 对象中的歌曲 ID 和信息。

---

## 附录：关键配置与入口文件

| 文件 | 作用 |
|------|------|
| `backend/main.py` | 后端启动入口，自动建表 |
| `backend/config.py` | 数据库连接 URL |
| `backend/models.py` | 6 个 ORM 模型 |
| `frontend/src/main.js` | 前端入口，路由定义 |
| `frontend/src/App.vue` | 根组件（导航、主题、粒子） |
| `frontend/src/player.js` | 全局音乐播放器 |
| `frontend/vite.config.js` | 开发代理配置 |
| `sql/init.sql` | 数据库建表 + 示例数据 |
| `music-server/server.js` | 网易云音乐 API 代理 |
