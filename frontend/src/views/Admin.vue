<template>
  <div class="admin-page">
    <!-- 登录页 -->
    <div v-if="!loggedIn" class="login-page grid-bg">
      <div class="login-card neon-card">
        <h1 class="login-title">⚙ 管理后台</h1>
        <p class="login-subtitle">请输入密码</p>
        <form @submit.prevent="doLogin" class="login-form">
          <input
            v-model="password"
            type="password"
            placeholder="密码"
            class="form-input"
            autofocus
          />
          <p v-if="loginError" class="error-msg">密码错误，请重试</p>
          <button type="submit" class="neon-btn login-btn">进入管理</button>
        </form>
      </div>
    </div>

    <!-- 管理页 -->
    <div v-else class="admin-dashboard">
      <div class="admin-header">
        <h1>⚙ 管理后台</h1>
        <div class="admin-header-actions">
          <span class="admin-user">🔑 已登录</span>
          <button class="action-btn" @click="logout">退出</button>
          <router-link to="/profile" class="action-btn">← 返回前台</router-link>
        </div>
      </div>

      <div class="admin-tabs">
        <button
          v-for="tab in tabs"
          :key="tab.key"
          class="tab-btn"
          :class="{ active: activeTab === tab.key }"
          @click="activeTab = tab.key; loadData(tab.key)"
        >
          {{ tab.icon }} {{ tab.label }}
        </button>
      </div>

      <div class="admin-content">
        <!-- 个人介绍 -->
        <div v-if="activeTab === 'profile'" class="admin-section">
          <div class="form-grid">
            <div class="form-group">
              <label>姓名</label>
              <input v-model="profileForm.name" class="form-input" />
            </div>
            <div class="form-group">
              <label>头衔</label>
              <input v-model="profileForm.title" class="form-input" />
            </div>
            <div class="form-group">
              <label>头像URL</label>
              <input v-model="profileForm.avatar" class="form-input" />
            </div>
            <div class="form-group">
              <label>邮箱</label>
              <input v-model="profileForm.email" class="form-input" placeholder="xxx@example.com" />
            </div>
            <div class="form-group">
              <label>手机号</label>
              <input v-model="profileForm.phone" class="form-input" placeholder="138xxxx" />
            </div>
            <div class="form-group">
              <label>GitHub</label>
              <input v-model="profileForm.github" class="form-input" placeholder="https://github.com/xxx" />
            </div>
            <div class="form-group">
              <label>哔哩哔哩</label>
              <input v-model="profileForm.bilibili" class="form-input" placeholder="https://space.bilibili.com/xxx" />
            </div>
            <div class="form-group">
              <label>CSDN</label>
              <input v-model="profileForm.csdn" class="form-input" placeholder="https://blog.csdn.net/xxx" />
            </div>
            <div class="form-group">
              <label>微信</label>
              <input v-model="profileForm.wechat" class="form-input" placeholder="微信号" />
            </div>
            <div class="form-group">
              <label>QQ</label>
              <input v-model="profileForm.qq" class="form-input" placeholder="QQ号" />
            </div>
            <div class="form-group">
              <label>技能标签（用逗号分隔）</label>
              <input v-model="profileSkills" class="form-input" placeholder="如: Python, JavaScript, Vue" />
            </div>
            <div class="form-group full-width">
              <label>个人简介</label>
              <textarea v-model="profileForm.bio" class="form-input form-textarea" rows="4"></textarea>
            </div>
          </div>
          <button class="neon-btn" @click="saveProfile">💾 保存个人介绍</button>
        </div>

        <!-- 项目 -->
        <div v-if="activeTab === 'projects'" class="admin-section">
          <div class="section-actions">
            <button class="neon-btn" @click="showProjectForm = true; editProject = null; projectForm = {}">
              ＋ 新增项目
            </button>
          </div>
          <div v-if="showProjectForm" class="form-card neon-card">
            <h3>{{ editProject ? '编辑' : '新增' }}项目</h3>
            <div class="form-grid">
              <div class="form-group">
                <label>项目名称</label>
                <input v-model="projectForm.title" class="form-input" />
              </div>
              <div class="form-group">
                <label>排序</label>
                <input v-model.number="projectForm.sort_order" type="number" class="form-input" />
              </div>
              <div class="form-group">
                <label>截图URL</label>
                <input v-model="projectForm.image" class="form-input" />
              </div>
              <div class="form-group">
                <label>演示链接</label>
                <input v-model="projectForm.demo_url" class="form-input" />
              </div>
              <div class="form-group">
                <label>源码链接</label>
                <input v-model="projectForm.github_url" class="form-input" />
              </div>
              <div class="form-group">
                <label>技术栈（逗号分隔）</label>
                <input v-model="projectTech" class="form-input" />
              </div>
              <div class="form-group full-width">
                <label>描述</label>
                <textarea v-model="projectForm.description" class="form-input form-textarea" rows="3"></textarea>
              </div>
            </div>
            <div class="form-actions">
              <button class="neon-btn" @click="saveProject">💾 保存</button>
              <button class="action-btn cancel-btn" @click="showProjectForm = false">取消</button>
            </div>
          </div>
          <table class="data-table" v-if="projects.length">
            <thead>
              <tr><th>排序</th><th>名称</th><th>技术栈</th><th>操作</th></tr>
            </thead>
            <tbody>
              <tr v-for="p in projects" :key="p.id">
                <td>{{ p.sort_order }}</td>
                <td>{{ p.title }}</td>
                <td><span v-for="t in p.tech_stack" :key="t" class="tag">{{ t }}</span></td>
                <td class="action-cells">
                  <button class="action-btn" @click="editProjectItem(p)">✏</button>
                  <button class="action-btn delete-btn" @click="deleteItem('projects', p.id)">🗑</button>
                </td>
              </tr>
            </tbody>
          </table>
          <div v-else-if="!showProjectForm" class="empty-state">暂无项目</div>
        </div>

        <!-- 文章 -->
        <div v-if="activeTab === 'articles'" class="admin-section">
          <div class="section-actions">
            <button class="neon-btn" @click="showArticleForm = true; editArticle = null; articleForm = {}">
              ＋ 新增文章
            </button>
          </div>
          <div v-if="showArticleForm" class="form-card neon-card">
            <h3>{{ editArticle ? '编辑' : '新增' }}文章</h3>
            <div class="form-grid">
              <div class="form-group">
                <label>标题</label>
                <input v-model="articleForm.title" class="form-input" />
              </div>
              <div class="form-group">
                <label>CSDN链接</label>
                <input v-model="articleForm.url" class="form-input" placeholder="https://blog.csdn.net/..." />
              </div>
              <div class="form-group">
                <label>日期</label>
                <input v-model="articleForm.date" type="date" class="form-input" />
              </div>
              <div class="form-group">
                <label>排序</label>
                <input v-model.number="articleForm.sort_order" type="number" class="form-input" />
              </div>
              <div class="form-group full-width">
                <label>摘要</label>
                <textarea v-model="articleForm.summary" class="form-input form-textarea" rows="3"></textarea>
              </div>
            </div>
            <div class="form-actions">
              <button class="neon-btn" @click="saveArticle">💾 保存</button>
              <button class="action-btn cancel-btn" @click="showArticleForm = false">取消</button>
            </div>
          </div>
          <table class="data-table" v-if="articles.length">
            <thead>
              <tr><th>排序</th><th>标题</th><th>日期</th><th>操作</th></tr>
            </thead>
            <tbody>
              <tr v-for="a in articles" :key="a.id">
                <td>{{ a.sort_order }}</td>
                <td>{{ a.title }}</td>
                <td>{{ a.date }}</td>
                <td class="action-cells">
                  <button class="action-btn" @click="editArticleItem(a)">✏</button>
                  <button class="action-btn delete-btn" @click="deleteItem('articles', a.id)">🗑</button>
                </td>
              </tr>
            </tbody>
          </table>
          <div v-else-if="!showArticleForm" class="empty-state">暂无文章</div>
        </div>

        <!-- 精彩生活 -->
        <div v-if="activeTab === 'life'" class="admin-section">
          <div class="section-actions">
            <button class="neon-btn" @click="showLifeForm = true; editLife = null; lifeForm = {}">
              ＋ 新增动态
            </button>
          </div>
          <div v-if="showLifeForm" class="form-card neon-card">
            <h3>{{ editLife ? '编辑' : '新增' }}生活动态</h3>
            <div class="form-grid">
              <div class="form-group">
                <label>标题</label>
                <input v-model="lifeForm.title" class="form-input" />
              </div>
              <div class="form-group">
                <label>图片URL</label>
                <input v-model="lifeForm.image" class="form-input" />
              </div>
              <div class="form-group">
                <label>日期</label>
                <input v-model="lifeForm.date" type="date" class="form-input" />
              </div>
              <div class="form-group full-width">
                <label>内容</label>
                <textarea v-model="lifeForm.content" class="form-input form-textarea" rows="4"></textarea>
              </div>
            </div>
            <div class="form-actions">
              <button class="neon-btn" @click="saveLife">💾 保存</button>
              <button class="action-btn cancel-btn" @click="showLifeForm = false">取消</button>
            </div>
          </div>
          <table class="data-table" v-if="moments.length">
            <thead>
              <tr><th>标题</th><th>日期</th><th>操作</th></tr>
            </thead>
            <tbody>
              <tr v-for="m in moments" :key="m.id">
                <td>{{ m.title }}</td>
                <td>{{ m.date }}</td>
                <td class="action-cells">
                  <button class="action-btn" @click="editLifeItem(m)">✏</button>
                  <button class="action-btn delete-btn" @click="deleteItem('life', m.id)">🗑</button>
                </td>
              </tr>
            </tbody>
          </table>
          <div v-else-if="!showLifeForm" class="empty-state">暂无动态</div>
        </div>

        <!-- 好友 -->
        <div v-if="activeTab === 'friends'" class="admin-section">
          <div class="section-actions">
            <button class="neon-btn" @click="showFriendForm = true; editFriend = null; friendForm = {}">
              ＋ 新增好友
            </button>
          </div>
          <div v-if="showFriendForm" class="form-card neon-card">
            <h3>{{ editFriend ? '编辑' : '新增' }}好友</h3>
            <div class="form-grid">
              <div class="form-group">
                <label>名称</label>
                <input v-model="friendForm.name" class="form-input" />
              </div>
              <div class="form-group">
                <label>头像URL</label>
                <input v-model="friendForm.avatar" class="form-input" />
              </div>
              <div class="form-group">
                <label>博客链接</label>
                <input v-model="friendForm.blog_url" class="form-input" />
              </div>
              <div class="form-group">
                <label>排序</label>
                <input v-model.number="friendForm.sort_order" type="number" class="form-input" />
              </div>
              <div class="form-group full-width">
                <label>简介</label>
                <textarea v-model="friendForm.description" class="form-input form-textarea" rows="2"></textarea>
              </div>
            </div>
            <div class="form-actions">
              <button class="neon-btn" @click="saveFriend">💾 保存</button>
              <button class="action-btn cancel-btn" @click="showFriendForm = false">取消</button>
            </div>
          </div>
          <table class="data-table" v-if="friends.length">
            <thead>
              <tr><th>排序</th><th>名称</th><th>博客链接</th><th>操作</th></tr>
            </thead>
            <tbody>
              <tr v-for="f in friends" :key="f.id">
                <td>{{ f.sort_order }}</td>
                <td>{{ f.name }}</td>
                <td><a :href="f.blog_url" target="_blank" style="font-size:12px;">链接</a></td>
                <td class="action-cells">
                  <button class="action-btn" @click="editFriendItem(f)">✏</button>
                  <button class="action-btn delete-btn" @click="deleteItem('friends', f.id)">🗑</button>
                </td>
              </tr>
            </tbody>
          </table>
          <div v-else-if="!showFriendForm" class="empty-state">暂无好友</div>
        </div>

        <!-- 留言 -->
        <div v-if="activeTab === 'messages'" class="admin-section">
          <table class="data-table" v-if="messages.length">
            <thead>
              <tr><th>时间</th><th>姓名</th><th>邮箱</th><th>消息</th><th>操作</th></tr>
            </thead>
            <tbody>
              <tr v-for="m in messages" :key="m.id">
                <td style="white-space:nowrap;">{{ m.created_at?.slice(0,10) }}</td>
                <td>{{ m.name }}</td>
                <td>{{ m.email }}</td>
                <td style="max-width:300px;overflow:hidden;text-overflow:ellipsis;">{{ m.message }}</td>
                <td><button class="action-btn delete-btn" @click="deleteMessage(m.id)">🗑</button></td>
              </tr>
            </tbody>
          </table>
          <div v-else class="empty-state">暂无留言</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const ADMIN_PASSWORD = 'admin123'

// 登录
const password = ref('')
const loginError = ref(false)
const loggedIn = ref(sessionStorage.getItem('admin_logged') === 'yes')

const doLogin = () => {
  if (password.value === ADMIN_PASSWORD) {
    loggedIn.value = true
    loginError.value = false
    sessionStorage.setItem('admin_logged', 'yes')
  } else {
    loginError.value = true
  }
}

const logout = () => {
  loggedIn.value = false
  sessionStorage.removeItem('admin_logged')
}

// 标签
const tabs = [
  { key: 'profile', label: '个人介绍', icon: '👤' },
  { key: 'projects', label: '项目', icon: '💻' },
  { key: 'articles', label: '文章', icon: '📝' },
  { key: 'life', label: '精彩生活', icon: '📸' },
  { key: 'friends', label: '好友', icon: '👥' },
  { key: 'messages', label: '留言', icon: '📩' },
]
const activeTab = ref('profile')

// API 封装
const api = {
  async get(path) { const r = await fetch(path); return r.json() },
  async post(path, data) { return fetch(path, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) }).then(r => r.json()) },
  async put(path, data) { return fetch(path, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) }).then(r => r.json()) },
  async del(path) { return fetch(path, { method: 'DELETE' }).then(r => r.json()) },
}

// ====== 个人介绍 ======
const profileForm = ref({})
const profileSkills = ref('')

const loadProfile = async () => {
  const res = await api.get('/api/profile')
  if (res.data) {
    profileForm.value = { ...res.data }
    profileSkills.value = Array.isArray(res.data.skills) ? res.data.skills.join(', ') : ''
  }
}

const saveProfile = async () => {
  const data = {
    ...profileForm.value,
    skills: JSON.stringify(profileSkills.value.split(/[,，]/).map(s => s.trim()).filter(Boolean)),
  }
  await api.put('/api/profile', data)
  alert('✅ 保存成功！')
}

// ====== 项目 ======
const projects = ref([])
const showProjectForm = ref(false)
const projectForm = ref({})
const projectTech = ref('')
const editProject = ref(null)

const loadProjects = async () => {
  const res = await api.get('/api/projects')
  if (res.data) projects.value = res.data
}

const saveProject = async () => {
  const data = {
    ...projectForm.value,
    tech_stack: JSON.stringify(projectTech.value.split(/[,，]/).map(s => s.trim()).filter(Boolean)),
  }
  if (editProject.value) {
    await api.put(`/api/projects/${editProject.value.id}`, data)
  } else {
    await api.post('/api/projects', data)
  }
  showProjectForm.value = false
  loadProjects()
  alert('✅ 保存成功！')
}

const editProjectItem = (p) => {
  editProject.value = p
  projectForm.value = { ...p }
  projectTech.value = Array.isArray(p.tech_stack) ? p.tech_stack.join(', ') : ''
  showProjectForm.value = true
}

// ====== 文章 ======
const articles = ref([])
const showArticleForm = ref(false)
const articleForm = ref({})
const editArticle = ref(null)

const loadArticles = async () => {
  const res = await api.get('/api/articles')
  if (res.data) articles.value = res.data
}

const saveArticle = async () => {
  if (editArticle.value) {
    await api.put(`/api/articles/${editArticle.value.id}`, articleForm.value)
  } else {
    await api.post('/api/articles', articleForm.value)
  }
  showArticleForm.value = false
  loadArticles()
  alert('✅ 保存成功！')
}

const editArticleItem = (a) => {
  editArticle.value = a
  articleForm.value = { ...a }
  showArticleForm.value = true
}

// ====== 精彩生活 ======
const moments = ref([])
const showLifeForm = ref(false)
const lifeForm = ref({})
const editLife = ref(null)

const loadLife = async () => {
  const res = await api.get('/api/life')
  if (res.data) moments.value = res.data
}

const saveLife = async () => {
  if (editLife.value) {
    await api.put(`/api/life/${editLife.value.id}`, lifeForm.value)
  } else {
    await api.post('/api/life', lifeForm.value)
  }
  showLifeForm.value = false
  loadLife()
  alert('✅ 保存成功！')
}

const editLifeItem = (m) => {
  editLife.value = m
  lifeForm.value = { ...m }
  showLifeForm.value = true
}

// ====== 好友 ======
const friends = ref([])
const showFriendForm = ref(false)
const friendForm = ref({})
const editFriend = ref(null)

const loadFriends = async () => {
  const res = await api.get('/api/friends')
  if (res.data) friends.value = res.data
}

const saveFriend = async () => {
  if (editFriend.value) {
    await api.put(`/api/friends/${editFriend.value.id}`, friendForm.value)
  } else {
    await api.post('/api/friends', friendForm.value)
  }
  showFriendForm.value = false
  loadFriends()
  alert('✅ 保存成功！')
}

const editFriendItem = (f) => {
  editFriend.value = f
  friendForm.value = { ...f }
  showFriendForm.value = true
}

// ====== 留言 ======
const messages = ref([])

const loadMessages = async () => {
  const res = await api.get('/api/contact')
  if (res.data) messages.value = res.data
}

const deleteMessage = async (id) => {
  if (!confirm('确定删除这条留言？')) return
  await api.del(`/api/contact/${id}`)
  loadMessages()
}

// ====== 通用删除 ======
const deleteItem = async (type, id) => {
  if (!confirm('确定删除？')) return
  await api.del(`/api/${type}/${id}`)
  loadData(type)
}

const loadData = (tab) => {
  switch (tab) {
    case 'profile': loadProfile(); break
    case 'projects': loadProjects(); break
    case 'articles': loadArticles(); break
    case 'life': loadLife(); break
    case 'friends': loadFriends(); break
    case 'messages': loadMessages(); break
  }
}

onMounted(() => {
  if (loggedIn.value) loadProfile()
})
</script>

<style scoped>
.admin-page { min-height: calc(100vh - 70px); }

/* 登录页 */
.login-page {
  display: flex; align-items: center; justify-content: center;
  min-height: calc(100vh - 70px);
}
.login-card {
  max-width: 400px; width: 100%; text-align: center; padding: 40px;
}
.login-title { font-family: monospace; font-size: 28px; margin-bottom: 8px; }
.login-subtitle { color: var(--text-secondary); margin-bottom: 24px; }
.login-form { display: flex; flex-direction: column; gap: 12px; }
.login-btn { align-self: center; }
.error-msg { color: #ff2d78; font-size: 14px; }

/* 管理头部 */
.admin-header {
  display: flex; justify-content: space-between; align-items: center;
  padding: 20px; border-bottom: 1px solid var(--border);
  background: var(--bg-glass); backdrop-filter: blur(10px);
}
.admin-header h1 { font-family: monospace; font-size: 22px; }
.admin-header-actions { display: flex; gap: 8px; align-items: center; }
.admin-user { font-size: 13px; color: var(--text-secondary); }

/* 标签栏 */
.admin-tabs {
  display: flex; gap: 4px; padding: 12px 20px;
  border-bottom: 1px solid var(--border);
  background: var(--bg-secondary);
  flex-wrap: wrap;
}
.tab-btn {
  padding: 8px 16px; border: 1px solid var(--border);
  border-radius: var(--radius-sm); background: transparent;
  color: var(--text-secondary); cursor: pointer; font-size: 14px;
  transition: all 0.2s;
}
.tab-btn:hover { color: var(--text-primary); border-color: var(--accent); }
.tab-btn.active { color: var(--accent); border-color: var(--accent); background: rgba(0,240,255,0.1); }

/* 内容区 */
.admin-content { padding: 20px; max-width: 1200px; margin: 0 auto; }
.admin-section { min-height: 200px; }

/* 表单 */
.form-grid {
  display: grid; grid-template-columns: 1fr 1fr; gap: 12px;
  margin-bottom: 16px;
}
.form-group { display: flex; flex-direction: column; gap: 4px; }
.form-group label { font-size: 12px; color: var(--text-secondary); }
.form-group.full-width { grid-column: 1 / -1; }
.form-card { margin-bottom: 20px; }
.form-card h3 { margin-bottom: 16px; }
.form-actions { display: flex; gap: 8px; margin-top: 12px; }

.form-input {
  width: 100%; padding: 10px 14px;
  background: var(--bg-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  color: var(--text-primary); font-size: 14px; outline: none;
}
.form-input:focus { border-color: var(--accent); box-shadow: var(--shadow-glow); }
.form-textarea { resize: vertical; }

.cancel-btn { padding: 10px 16px; }

/* 数据表格 */
.data-table {
  width: 100%; border-collapse: collapse; font-size: 14px;
}
.data-table th {
  text-align: left; padding: 10px 12px;
  border-bottom: 1px solid var(--border);
  color: var(--text-secondary); font-size: 12px;
  text-transform: uppercase; letter-spacing: 1px;
}
.data-table td {
  padding: 10px 12px;
  border-bottom: 1px solid rgba(255,255,255,0.05);
}
.data-table tr:hover { background: rgba(0,240,255,0.03); }
.action-cells { display: flex; gap: 4px; }
.action-cells .action-btn { padding: 4px 8px; font-size: 14px; }
.delete-btn:hover { border-color: #ff2d78 !important; color: #ff2d78 !important; }

.section-actions { margin-bottom: 16px; }

@media (max-width: 768px) {
  .form-grid { grid-template-columns: 1fr; }
  .admin-tabs { gap: 4px; }
  .tab-btn { font-size: 12px; padding: 6px 10px; }
}
</style>
