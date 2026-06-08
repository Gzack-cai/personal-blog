<template>
  <div class="grid-bg" style="min-height: calc(100vh - 70px);">
    <div class="container">
      <div class="page-header">
        <h1 class="page-title">项目展示</h1>
        <p class="page-subtitle">我的作品集</p>
      </div>
      <div v-if="projects.length === 0" class="empty-state">暂无项目</div>
      <div v-else class="projects-grid">
        <div v-for="p in projects" :key="p.id" class="project-card neon-card">
          <div class="project-image">
            <img :src="p.image || ''" :alt="p.title" />
          </div>
          <div class="project-body">
            <h3>{{ p.title }}</h3>
            <p class="project-desc">{{ p.description }}</p>
            <div class="project-tags">
              <span v-for="tech in p.tech_stack" :key="tech" class="tag">{{ tech }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
const projects = ref([])
onMounted(async () => {
  try { const r = await fetch('/api/projects'); const j = await r.json(); if (j.data) projects.value = j.data; } catch(e) { console.log('API unavailable') }
})
</script>

<style scoped>
.projects-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 24px; padding-bottom: 40px; }
.project-card { overflow: hidden; padding: 0; }
.project-image { width: 100%; height: 200px; overflow: hidden; background: var(--bg-secondary); }
.project-image img { width: 100%; height: 100%; object-fit: cover; }
.project-body { padding: 20px; }
.project-body h3 { font-family: monospace; font-size: 16px; margin-bottom: 8px; }
.project-desc { color: var(--text-secondary); font-size: 13px; line-height: 1.6; margin-bottom: 12px; }
.project-tags { display: flex; flex-wrap: wrap; gap: 6px; }
@media (max-width: 768px) { .projects-grid { grid-template-columns: 1fr; } }
</style>
