<template>
  <div class="grid-bg" style="min-height: calc(100vh - 70px);">
    <div class="container">
      <div class="page-header">
        <h1 class="page-title">个人介绍</h1>
        <p class="page-subtitle">全栈开发者 | 技术爱好者</p>
      </div>
      <div class="profile-card neon-card">
        <div class="avatar-frame">
          <img :src="profile.avatar || 'data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><rect fill=%22%23131740%22 width=%22100%22 height=%22100%22/><text x=%2250%22 y=%2255%22 text-anchor=%22middle%22 font-size=%2230%22 fill=%22%2300f0ff%22>U</text></svg>'"
               :alt="profile.name" />
        </div>
        <h2 class="profile-name">{{ profile.name || 'Your Name' }}</h2>
        <p class="profile-title">{{ profile.title || '全栈开发者' }}</p>
        <p class="profile-bio">{{ profile.bio || '热爱编程，专注于Web开发与人工智能。' }}</p>

        <div class="section">
          <h3 class="section-label">技能标签</h3>
          <div class="skills-list">
            <span v-for="skill in profile.skills" :key="skill" class="tag">{{ skill }}</span>
          </div>
        </div>

        <div class="section" v-if="hasContacts">
          <h3 class="section-label">联系方式</h3>
          <div class="contact-grid">
            <a :href="`mailto:${profile.email}`" class="contact-item" v-if="profile.email">
              <span class="ci-icon">✉</span>
              <span class="ci-text">{{ profile.email }}</span>
            </a>
            <a :href="`tel:${profile.phone}`" class="contact-item" v-if="profile.phone">
              <span class="ci-icon">📞</span>
              <span class="ci-text">{{ profile.phone }}</span>
            </a>
            <a :href="profile.github" target="_blank" class="contact-item" v-if="profile.github">
              <span class="ci-icon">⌨</span>
              <span class="ci-text">GitHub</span>
            </a>
            <a :href="profile.bilibili" target="_blank" class="contact-item" v-if="profile.bilibili">
              <span class="ci-icon">📺</span>
              <span class="ci-text">哔哩哔哩</span>
            </a>
            <a :href="profile.csdn" target="_blank" class="contact-item" v-if="profile.csdn">
              <span class="ci-icon">📝</span>
              <span class="ci-text">CSDN</span>
            </a>
            <div class="contact-item" v-if="profile.wechat">
              <span class="ci-icon">💬</span>
              <span class="ci-text">{{ profile.wechat }}</span>
            </div>
            <div class="contact-item" v-if="profile.qq">
              <span class="ci-icon">💭</span>
              <span class="ci-text">QQ: {{ profile.qq }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const profile = ref({
  name: 'Loading...', title: '', avatar: '', bio: '',
  skills: [], email: '', phone: '', github: '', bilibili: '',
  csdn: '', wechat: '', qq: '',
})

const hasContacts = computed(() =>
  profile.value.email || profile.value.phone || profile.value.github ||
  profile.value.bilibili || profile.value.csdn || profile.value.wechat || profile.value.qq
)

onMounted(async () => {
  try {
    const res = await fetch('/api/profile')
    const json = await res.json()
    if (json.data) profile.value = json.data
  } catch (e) {
    console.log('API not available, using defaults')
  }
})
</script>

<style scoped>
.profile-card {
  max-width: 900px; margin: 0 auto 40px; text-align: center; padding: 50px 40px;
}
.avatar-frame {
  width: 140px; height: 140px; border-radius: 50%;
  border: 3px solid var(--accent); box-shadow: var(--shadow-glow);
  overflow: hidden; margin: 0 auto 20px;
}
.avatar-frame img { width: 100%; height: 100%; object-fit: cover; }
.profile-name {
  font-family: monospace; font-size: 28px; margin-bottom: 4px;
  background: linear-gradient(135deg, var(--accent), var(--accent-pink));
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.profile-title { color: var(--accent-secondary); font-size: 16px; margin-bottom: 16px; }
.profile-bio { color: var(--text-secondary); line-height: 1.8; margin-bottom: 24px; }
.section { margin-bottom: 20px; }
.section-label {
  font-size: 14px; color: var(--text-secondary);
  text-transform: uppercase; letter-spacing: 2px; margin-bottom: 12px;
}
.skills-list { display: flex; flex-wrap: wrap; justify-content: center; gap: 8px; }

/* 联系方式网格 - 固定3列等宽 */
.contact-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 12px;
  max-width: 750px;
  margin: 0 auto;
}

.contact-item {
  display: flex; align-items: center; gap: 8px;
  padding: 12px 14px; border-radius: var(--radius-sm);
  border: 1px solid var(--border); color: var(--text-primary);
  transition: all 0.2s; font-size: 14px; text-decoration: none;
}
.contact-item:hover { border-color: var(--accent); box-shadow: var(--shadow-glow); color: var(--accent); }

.ci-icon { font-size: 20px; flex-shrink: 0; }
.ci-text { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

@media (max-width: 700px) {
  .contact-grid { grid-template-columns: 1fr 1fr; }
}
@media (max-width: 480px) {
  .contact-grid { grid-template-columns: 1fr; }
}
</style>
