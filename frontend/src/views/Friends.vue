<template>
  <div class="grid-bg" style="min-height: calc(100vh - 70px);">
    <div class="container">
      <div class="page-header">
        <h1 class="page-title">我的好友</h1>
        <p class="page-subtitle">友情链接</p>
      </div>
      <div v-if="friends.length === 0" class="empty-state">暂无好友</div>
      <div v-else class="friends-grid">
        <div v-for="f in friends" :key="f.id" class="friend-card neon-card">
          <div class="friend-avatar">
            <img :src="f.avatar || ''" :alt="f.name" />
          </div>
          <h3>{{ f.name }}</h3>
          <p class="friend-desc">{{ f.description }}</p>
          <a :href="f.blog_url" target="_blank" class="neon-btn">访问博客 →</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
const friends = ref([])
onMounted(async () => {
  try { const r = await fetch('/api/friends'); const j = await r.json(); if (j.data) friends.value = j.data; } catch(e) { console.log('API unavailable') }
})
</script>

<style scoped>
.friends-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 24px; padding-bottom: 40px; }
.friend-card { text-align: center; padding: 30px 20px; }
.friend-avatar { width: 80px; height: 80px; border-radius: 50%; border: 2px solid var(--accent-secondary); overflow: hidden; margin: 0 auto 16px; }
.friend-avatar img { width: 100%; height: 100%; object-fit: cover; }
.friend-card h3 { font-family: monospace; font-size: 18px; margin-bottom: 8px; }
.friend-desc { color: var(--text-secondary); font-size: 13px; margin-bottom: 16px; }
@media (max-width: 768px) { .friends-grid { grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); } }
</style>
