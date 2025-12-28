# Django 博客系统

一个功能完整、界面现代化的 Django 博客系统，具有用户认证、文章管理、评论点赞等功能。

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

## 核心功能

### 文章管理
- **文章发布**：用户可创建、编辑、删除自己的博客文章
- **文章展示**：按时间倒序展示所有公开文章
- **权限控制**：只有文章作者可以编辑和删除自己的文章
- **浏览量统计**：自动记录并显示每篇文章的浏览次数

### 用户系统
- **用户认证**：注册、登录、登出功能
- **个人资料**：查看用户发布的文章和统计数据
- **权限管理**：区分匿名用户、注册用户和文章作者权限

### 互动功能
- **评论系统**：登录用户可对文章发表评论
- **点赞功能**：用户可以为喜欢的文章点赞/取消点赞
- **评论排序**：评论按时间倒序排列，最新评论显示在最前面

### 界面特色
- **现代化UI设计**：采用卡片式布局和渐变色彩
- **响应式设计**：适配桌面、平板和手机等不同设备
- **自定义背景**：支持上传和显示文章封面图片

## 技术栈

### 后端技术
- **Django 6.0** - Python Web框架

### 前端技术
- **HTML5 & CSS3** - 页面结构和样式
- **Bootstrap 5** - 响应式框架
- **JavaScript (ES6)** - 交互功能
- **AJAX** - 异步请求（用于点赞功能）
- **Font Awesome** - 图标库

## 项目结构

```
blog_prj/
├── blog/                  # 博客应用
│   ├── migrations/        # 数据库迁移文件
│   ├── templates/         # 模板文件
│   │   ├── blog/          # 博客模板
│   │   └── registration/  # 注册登录模板
│   ├── models.py          # 数据模型
│   ├── views.py           # 视图函数
│   ├── urls.py            # URL配置
│   └── forms.py           # 表单定义
├── blog_prj/              # 项目配置
│   ├── settings.py        # 项目设置
│   ├── urls.py            # 主URL配置
│   └── wsgi.py            # WSGI配置
│   static/                # 静态文件
│   ├── css/               # 样式文件
│   └── images/            # 图片资源
├── db.sqlite3             # SQLite数据库
└── manage.py              # Django管理脚本
```

## 快速开始

### 环境要求
- Python 3.8+
- Django 6.0+

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd blog_prj
```

2. **创建虚拟环境**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **数据库迁移**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **创建超级用户**
```bash
python manage.py createsuperuser
```

6. **运行开发服务器**
```bash
python manage.py runserver
```

7. **访问应用**
打开浏览器访问：http://127.0.0.1:8000/

## 数据模型

### BlogPost (博客文章)
```python
- title: 文章标题
- text: 文章内容
- date_added: 创建时间
- owner: 文章作者 (ForeignKey to User)
- views: 浏览量
- cover_image: 封面图片 (可选)
- likes: 点赞用户 (ManyToManyField)
- tags: 标签 (ManyToManyField)
```

### Comment (评论)
```python
- post: 关联文章 (ForeignKey to BlogPost)
- author: 评论作者 (ForeignKey to User)
- text: 评论内容
- created_date: 评论时间
```

## 权限系统

### 用户角色
- **匿名用户**：浏览文章、查看评论
- **注册用户**：发布文章、发表评论、点赞文章
- **文章作者**：编辑/删除自己的文章

### 权限保护
- 使用 `@login_required` 装饰器保护需要登录的视图
- 使用 `UserPassesTestMixin` 确保只有作者可以编辑/删除文章
- 使用 `LoginRequiredMixin` 保护基于类的视图

## 主要URL路由

| 路径 | 视图 | 描述 |
|------|------|------|
| `/` | `PostListView` | 首页，显示所有文章 |
| `/post/<int:pk>/` | `PostDetailView` | 文章详情页 |
| `/post/new/` | `PostCreateView` | 创建新文章 |
| `/post/<int:pk>/edit/` | `PostUpdateView` | 编辑文章 |
| `/post/<int:pk>/delete/` | `PostDeleteView` | 删除文章 |
| `/post/<int:pk>/comment/` | `add_comment` | 添加评论 |
| `/post/<int:pk>/like/` | `like_post` | 点赞文章 |
| `/register/` | `register` | 用户注册 |
| `/profile/<str:username>/` | `profile` | 用户个人资料页 |

## 界面特性

### 1. 现代化设计
- 渐变背景和阴影效果
- 圆角卡片设计
- 平滑过渡动画
- 响应式网格布局

### 2. 交互体验
- 实时点赞计数更新（无需刷新页面）
- 表单验证和错误提示
- 加载状态提示
- 确认对话框（删除操作）

### 3. 文章展示
- 文章卡片布局
- 分页功能（每页5篇文章）
- 标签分类显示
- 阅读进度指示

### 功能
- [-] 用户认证系统
- [-] 文章CRUD操作
- [-] 评论和点赞系统
- [-] 权限控制和验证
- [-] 响应式界面设计
- [-] 图片上传功能

## 致谢

感谢以下开源项目：
- [Django](https://www.djangoproject.com/) - Web框架