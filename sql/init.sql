CREATE DATABASE IF NOT EXISTS personal_blog CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE personal_blog;

-- 个人介绍表
CREATE TABLE IF NOT EXISTS profile (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    title VARCHAR(200) NOT NULL,
    avatar VARCHAR(500),
    bio TEXT,
    skills TEXT COMMENT 'JSON array of skill tags',
    email VARCHAR(200),
    phone VARCHAR(50),
    github VARCHAR(500),
    bilibili VARCHAR(500),
    csdn VARCHAR(500),
    wechat VARCHAR(200),
    qq VARCHAR(50),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 项目表
CREATE TABLE IF NOT EXISTS projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    image VARCHAR(500),
    tech_stack TEXT COMMENT 'JSON array of tech stack tags',
    demo_url VARCHAR(500),
    github_url VARCHAR(500),
    sort_order INT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 文章表
CREATE TABLE IF NOT EXISTS articles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    summary TEXT,
    url VARCHAR(500) NOT NULL,
    date DATE,
    sort_order INT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 精彩生活表
CREATE TABLE IF NOT EXISTS life_moments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200),
    content TEXT,
    image VARCHAR(500),
    date DATE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 好友表
CREATE TABLE IF NOT EXISTS friends (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    avatar VARCHAR(500),
    description TEXT,
    blog_url VARCHAR(500) NOT NULL,
    sort_order INT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 联系消息表
CREATE TABLE IF NOT EXISTS contact_messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 插入初始数据
INSERT INTO profile (name, title, avatar, bio, skills, email, phone, github, bilibili) VALUES
('Your Name', '全栈开发者 / 学生', '/avatar.jpg', '热爱编程，专注于Web开发与人工智能。喜欢探索新技术，热衷于开源社区。', '["Python", "JavaScript", "Vue", "FastAPI", "MySQL", "Git"]', 'your-email@example.com', '138xxxx', 'https://github.com/yourusername', 'https://space.bilibili.com/xxx');

INSERT INTO projects (title, description, image, tech_stack, demo_url, github_url, sort_order) VALUES
('个人博客网站', '基于FastAPI和Vue3的个人品牌展示网站，赛博朋克科技风设计', '/project1.jpg', '["FastAPI", "Vue3", "MySQL", "Vite"]', '#', '#', 1),
('示例项目二', '项目描述文字', '/project2.jpg', '["Python", "React"]', '#', '#', 2);

INSERT INTO articles (title, summary, url, date, sort_order) VALUES
('我的第一篇技术博客', '这是一篇关于Web开发的入门教程...', 'https://blog.csdn.net/your-article-1', '2026-01-15', 1),
('FastAPI最佳实践', '分享FastAPI在实际项目中的使用经验和技巧...', 'https://blog.csdn.net/your-article-2', '2026-03-20', 2);

INSERT INTO life_moments (title, content, image, date) VALUES
('周末的代码时光', '享受周末 coding 的宁静时光', '/life1.jpg', '2026-05-20'),
('技术交流会', '参加本地技术交流活动，收获满满', '/life2.jpg', '2026-04-15');

INSERT INTO friends (name, avatar, description, blog_url, sort_order) VALUES
('好友A', '/friend1.jpg', '前端开发工程师', 'https://friend-a-blog.com', 1),
('好友B', '/friend2.jpg', '后端架构师', 'https://friend-b-blog.com', 2);

INSERT INTO contact_messages (name, email, message) VALUES
('测试用户', 'test@example.com', '你好，看了你的项目非常感兴趣！');

-- 如果表已存在，补充新增字段（重复执行会报错，忽略即可）
-- ALTER TABLE profile ADD COLUMN phone VARCHAR(50) AFTER email;
-- ALTER TABLE profile ADD COLUMN bilibili VARCHAR(500) AFTER github;
-- ALTER TABLE profile ADD COLUMN csdn VARCHAR(500) AFTER bilibili;
-- ALTER TABLE profile ADD COLUMN wechat VARCHAR(200) AFTER csdn;
-- ALTER TABLE profile ADD COLUMN qq VARCHAR(50) AFTER wechat;
-- 或在 MySQL 中执行: ALTER TABLE personal_blog.profile ADD COLUMN (phone VARCHAR(50), bilibili VARCHAR(500), csdn VARCHAR(500), wechat VARCHAR(200), qq VARCHAR(50));
