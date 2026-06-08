<template>
  <div class="music-player" :class="{ playing: isPlaying }">
    <button class="player-btn" @click="togglePlay" :title="isPlaying ? $t('music.pause') : $t('music.play')">
      <span class="icon">{{ isPlaying ? '⏸' : '▶' }}</span>
    </button>
    <span class="track-name">{{ currentTrack || '--' }}</span>
    <button class="player-btn" @click="nextTrack" title="下一首">⏭</button>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const isPlaying = ref(false)
const currentTrack = ref('')
const tracks = ref([
  { name: 'Cyber Pulse', src: '' },
  { name: 'Neon Dreams', src: '' },
])
const currentIndex = ref(0)
let audio = null

onMounted(() => {
  audio = new Audio()
  audio.addEventListener('ended', nextTrack)
})

onUnmounted(() => {
  if (audio) {
    audio.pause()
    audio = null
  }
})

const togglePlay = () => {
  isPlaying.value = !isPlaying.value
  if (isPlaying.value) {
    if (audio.src) {
      audio.play()
    }
  } else {
    audio.pause()
  }
}

const nextTrack = () => {
  currentIndex.value = (currentIndex.value + 1) % tracks.value.length
  currentTrack.value = tracks.value[currentIndex.value].name
  if (isPlaying.value && tracks.value[currentIndex.value].src) {
    audio.src = tracks.value[currentIndex.value].src
    audio.play()
  }
}
</script>

<style scoped>
.music-player {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 4px 8px;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  background: rgba(0, 240, 255, 0.05);
}

.player-btn {
  background: none;
  border: none;
  color: var(--text-primary);
  cursor: pointer;
  font-size: 14px;
  padding: 2px 4px;
  transition: color var(--transition-fast);
}

.player-btn:hover {
  color: var(--accent);
}

.track-name {
  font-size: 12px;
  color: var(--text-secondary);
  max-width: 80px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.playing .player-btn:first-child {
  color: var(--accent);
}
</style>
