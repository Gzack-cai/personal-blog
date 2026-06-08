<template>
  <div class="lyrics-panel" v-if="player.currentSong && player.lyrics.length > 0 && !isMusicPage">
    <div class="lp-header">
      <span class="lp-title">🎵 {{ player.currentSong.name }}</span>
      <span class="lp-artist">{{ player.currentSong.artists?.[0]?.name }}</span>
    </div>
    <div class="lp-list" ref="lpList">
      <div
        v-for="(line, idx) in player.lyrics"
        :key="idx"
        class="lp-line"
        :class="{ active: player.currentLyricIdx === idx }"
      >
        {{ line.text }}
      </div>
      <div v-if="player.lyrics.length === 0" class="lp-empty">暂无歌词</div>
    </div>
    <div class="lp-disc" :class="{ spinning: player.isPlaying }">
      <div class="lp-disc-inner">{{ player.currentSong.name?.charAt(0) || '♪' }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { player } from '../player'

const route = useRoute()
const lpList = ref(null)

const isMusicPage = computed(() => route.path === '/music')

// 歌词变化和高亮时自动滚动
watch(() => player.currentLyricIdx, async (idx) => {
  if (idx < 0 || !lpList.value) return
  await nextTick()
  const el = lpList.value.querySelectorAll('.lp-line')[idx]
  if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' })
})
</script>

<style scoped>
.lyrics-panel {
  position: fixed; top: 80px; right: 0; bottom: 0;
  width: 260px; z-index: 10;
  background: var(--bg-glass);
  backdrop-filter: blur(20px);
  border-left: 1px solid var(--border);
  display: flex; flex-direction: column;
  transition: transform 0.3s;
  overflow: hidden;
}

.lp-header {
  padding: 16px 16px 8px;
  border-bottom: 1px solid var(--border);
  flex-shrink: 0;
}

.lp-title {
  display: block; font-size: 13px; font-weight: 600;
  color: var(--accent);
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}

.lp-artist {
  display: block; font-size: 11px; color: var(--text-muted); margin-top: 2px;
}

.lp-list {
  flex: 1; overflow-y: auto; padding: 8px 0;
  scroll-behavior: smooth;
}
.lp-list::-webkit-scrollbar { width: 2px; }

.lp-line {
  padding: 8px 16px;
  font-size: 13px; line-height: 1.5;
  color: var(--text-muted);
  transition: all 0.3s;
  border-left: 2px solid transparent;
}
.lp-line.active {
  color: var(--accent);
  font-size: 14px;
  font-weight: 600;
  border-left-color: var(--accent);
  background: rgba(0,240,255,0.05);
}

.lp-empty { text-align: center; padding: 40px 16px; color: var(--text-muted); font-size: 13px; }

.lp-disc {
  width: 40px; height: 40px; border-radius: 50%;
  background: linear-gradient(135deg, #1a1a2e, #333);
  border: 2px solid var(--accent);
  display: flex; align-items: center; justify-content: center;
  margin: 12px auto;
  flex-shrink: 0;
  box-shadow: 0 0 10px rgba(0,240,255,0.2);
}
.lp-disc.spinning { animation: spin 3s linear infinite; }
.lp-disc-inner {
  width: 16px; height: 16px; border-radius: 50%;
  background: var(--accent);
  color: #0a0e27;
  font-size: 10px; font-weight: 700;
  display: flex; align-items: center; justify-content: center;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@media (max-width: 1100px) {
  .lyrics-panel { display: none; }
}
</style>
