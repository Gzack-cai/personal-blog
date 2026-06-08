<template>
  <div class="grid-bg" style="min-height: calc(100vh - 70px);">
    <div class="container">
      <div class="page-header">
        <h1 class="page-title">文章</h1>
        <p class="page-subtitle">我的技术博客</p>
      </div>
      <div v-if="articles.length === 0" class="empty-state">暂无文章</div>
      <div v-else class="articles-list">
        <div v-for="a in articles" :key="a.id" class="article-card neon-card">
          <div>
            <small style="color: var(--text-secondary);">{{ a.date }}</small>
            <h3>{{ a.title }}</h3>
            <p style="color: var(--text-secondary); font-size: 14px;">{{ a.summary }}</p>
          </div>
          <a :href="a.url" target="_blank" class="article-link">阅读全文 →</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
const articles = ref([])
onMounted(async () => {
  try { const r = await fetch('/api/articles'); const j = await r.json(); if (j.data) articles.value = j.data; } catch(e) { console.log('API unavailable') }
})
</script>

<style scoped>
.articles-list { max-width: 800px; margin: 0 auto 40px; display: flex; flex-direction: column; gap: 16px; }
.article-card { display: flex; justify-content: space-between; align-items: flex-start; gap: 16px; }
.article-card h3 { font-size: 18px; margin: 6px 0; }
.article-link { white-space: nowrap; padding: 8px 16px; border: 1px solid var(--border); border-radius: var(--radius-sm); font-size: 14px; color: var(--accent); text-decoration: none; }
.article-link:hover { border-color: var(--accent); box-shadow: var(--shadow-glow); }
@media (max-width: 600px) { .article-card { flex-direction: column; } }
</style>
