<template>
  <nav class="navbar glass">
    <div class="nav-inner">
      <div class="nav-brand">
        <router-link to="/" class="logo">{{ isLight ? '☀' : '🌙' }}.dev</router-link>
      </div>
      <div class="nav-links">
        <router-link
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          class="nav-link"
          :class="{ active: $route.path === item.path }"
        >
          <span class="nav-icon">{{ item.icon }}</span>
          <span class="nav-text">{{ $t(`nav.${item.key}`) }}</span>
        </router-link>
      </div>
      <div class="nav-actions">
        <MusicPlayer />
        <button class="action-btn" @click="toggleLang" :title="currentLang === 'zh' ? 'English' : '中文'">
          {{ currentLang === 'zh' ? 'EN' : '中' }}
        </button>
        <button class="action-btn" @click="toggleTheme">
          {{ isLight ? '🌙' : '☀️' }}
        </button>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { computed, inject } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import MusicPlayer from './MusicPlayer.vue'

const { locale } = useI18n()
const route = useRoute()
const isLight = inject('isLight')
const toggleTheme = inject('toggleTheme')

const currentLang = computed(() => locale.value)

const toggleLang = () => {
  locale.value = locale.value === 'zh' ? 'en' : 'zh'
  localStorage.setItem('lang', locale.value)
}

const navItems = [
  { path: '/profile', key: 'profile', icon: '👤' },
  { path: '/projects', key: 'projects', icon: '💻' },
  { path: '/articles', key: 'articles', icon: '📝' },
  { path: '/life', key: 'life', icon: '📸' },
  { path: '/friends', key: 'friends', icon: '👥' },
  { path: '/contact', key: 'contact', icon: '📞' },
]
</script>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  padding: 0 20px;
  height: 64px;
  border-bottom: 1px solid var(--border);
  background: var(--bg-glass);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
}

.nav-inner {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  height: 100%;
  gap: 20px;
}

.logo {
  font-family: var(--font-display);
  font-size: 20px;
  font-weight: 700;
  background: linear-gradient(135deg, var(--accent), var(--accent-secondary));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  white-space: nowrap;
}

.nav-links {
  display: flex;
  gap: 4px;
  flex: 1;
  justify-content: center;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  border-radius: var(--radius-sm);
  color: var(--text-secondary);
  font-size: 14px;
  transition: all var(--transition-fast);
  white-space: nowrap;
  text-decoration: none;
}

.nav-link:hover {
  color: var(--text-primary);
  background: rgba(0, 240, 255, 0.08);
}

.nav-link.active {
  color: var(--accent);
  background: rgba(0, 240, 255, 0.1);
  border: 1px solid var(--border);
}

.nav-icon {
  font-size: 16px;
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.action-btn {
  background: none;
  border: 1px solid var(--border);
  color: var(--text-primary);
  padding: 6px 10px;
  border-radius: var(--radius-sm);
  cursor: pointer;
  font-size: 14px;
  transition: all var(--transition-fast);
}

.action-btn:hover {
  border-color: var(--accent);
  background: rgba(0, 240, 255, 0.1);
}

@media (max-width: 900px) {
  .nav-text { display: none; }
  .nav-link { padding: 8px 10px; }
  .nav-icon { font-size: 20px; }
}
</style>
