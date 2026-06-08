<template>
  <div class="music-page grid-bg">
    <div class="music-container">
      <!-- 大旋转唱片 -->
      <div class="hero-player">
        <div class="vinyl-section">
          <div
            class="vinyl-disc"
            :class="{ spinning: player.isPlaying && player.currentSong }"
            @click="togglePlayPause"
          >
            <div class="vinyl-label">
              <span class="vinyl-initial">{{ player.currentSong?.name?.charAt(0) || '♪' }}</span>
            </div>
            <div class="vinyl-ring"></div>
            <div class="vinyl-ring-2"></div>
          </div>
          <div class="vinyl-arm" :class="{ lowered: player.currentSong }">
            <div class="arm-base"></div><div class="arm-body"></div><div class="arm-head"></div>
          </div>
        </div>

        <div class="player-info">
          <h2 class="current-title">{{ player.currentSong?.name || '未播放' }}</h2>
          <p class="current-artist">{{ player.currentSong?.artists?.[0]?.name || '点击下方搜索音乐' }}</p>
        </div>

        <!-- 播放控制 -->
        <div class="player-controls">
          <button class="ctrl-btn" @click="prevTrack" :disabled="!player.currentSong">⏮</button>
          <button class="ctrl-btn ctrl-play" @click="togglePlayPause">
            {{ player.isPlaying ? '⏸' : '▶' }}
          </button>
          <button class="ctrl-btn" @click="nextTrack" :disabled="!player.currentSong">⏭</button>
        </div>

        <!-- 进度条 -->
        <div class="progress-section" v-if="player.currentSong">
          <span class="time-label">{{ formatTime(player.currentTime * 1000) }}</span>
          <div class="progress-track" ref="progressBar" @click="seekBar">
            <div class="progress-fill" :style="{ width: progressPercent + '%' }"></div>
            <div class="progress-thumb" :style="{ left: progressPercent + '%' }"></div>
          </div>
          <span class="time-label">{{ formatTime(player.currentSong?.duration || 0) }}</span>
        </div>

        <div class="volume-section">
          <span>🔊</span>
          <input type="range" min="0" max="1" step="0.05" v-model.number="player.volume" @input="onVolume" class="volume-slider" />
        </div>
      </div>

      <!-- 搜索栏 -->
      <div class="search-section">
        <div class="search-bar">
          <input v-model="keyword" class="search-input" placeholder="搜索歌曲、歌手..." @keyup.enter="search" />
          <button class="neon-btn" @click="search">🔍 搜索</button>
        </div>
      </div>

      <!-- 两列布局：搜索结果 + 歌词 -->
      <div class="bottom-columns">
        <!-- 左列：搜索结果 -->
        <div class="column playlist-column">
          <h3 class="column-title">🎶 搜索结果</h3>
          <div v-if="loading" class="column-loading"><div class="spinner-sm"></div><p>搜索中...</p></div>
          <div v-else-if="results.length > 0" class="playlist-list">
            <div
              v-for="(song, idx) in results"
              :key="song.id"
              class="playlist-item"
              :class="{ active: player.currentSongId === song.id }"
              @click="playSong(song)"
            >
              <span class="pl-idx">{{ idx + 1 }}</span>
              <div class="pl-info">
                <span class="pl-name">{{ song.name }}</span>
                <span class="pl-artist">{{ song.artists?.[0]?.name || '未知' }}</span>
              </div>
              <span class="pl-duration">{{ formatTime(song.duration) }}</span>
              <span class="pl-indicator" v-if="player.currentSongId === song.id">
                {{ player.isPlaying ? '🔊' : '⏸' }}
              </span>
            </div>
          </div>
          <div v-else class="column-empty">
            <p v-if="searched">未找到相关歌曲</p>
            <p v-else>搜索你想听的歌曲</p>
          </div>
        </div>

        <!-- 右列：歌词（使用全局歌词） -->
        <div class="column lyric-column">
          <h3 class="column-title">📝 歌词</h3>
          <div class="lyric-list" ref="lyricList">
            <div
              v-for="(line, idx) in player.lyrics"
              :key="idx"
              class="lyric-line"
              :class="{ active: player.currentLyricIdx === idx }"
            >
              {{ line.text }}
            </div>
            <div v-if="player.lyrics.length === 0 && player.currentSong" class="column-empty">
              <p>暂无歌词</p>
            </div>
            <div v-if="!player.currentSong" class="column-empty">
              <p>播放歌曲显示歌词</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { player, playSong, togglePlayPause, formatTime, setVolume } from '../player'

const keyword = ref('')
const results = ref([])
const loading = ref(false)
const searched = ref(false)
const progressBar = ref(null)
const lyricList = ref(null)

const progressPercent = computed(() => {
  const dur = player.currentSong?.duration || 0
  if (!dur || !player.currentTime) return 0
  return (player.currentTime / (dur / 1000)) * 100
})

const search = async () => {
  if (!keyword.value.trim()) return
  loading.value = true; searched.value = true
  try {
    const res = await fetch(`/music-api/search?keywords=${encodeURIComponent(keyword.value)}&limit=30`)
    const data = await res.json()
    if (data.code === 200 && data.result) {
      results.value = data.result.songs || []
    } else { results.value = [] }
  } catch (e) { results.value = [] }
  loading.value = false
}

const seekBar = (e) => {
  if (!progressBar.value || !player.audio) return
  const rect = progressBar.value.getBoundingClientRect()
  const pct = (e.clientX - rect.left) / rect.width
  player.audio.currentTime = pct * (player.currentSong.duration / 1000)
}

const onVolume = () => setVolume(player.volume)

const prevTrack = () => {
  const idx = results.value.findIndex(s => s.id === player.currentSongId)
  if (idx > 0) playSong(results.value[idx - 1])
}
const nextTrack = () => {
  const idx = results.value.findIndex(s => s.id === player.currentSongId)
  if (idx < results.value.length - 1) playSong(results.value[idx + 1])
}

// 歌词高亮时自动滚动
watch(() => player.currentLyricIdx, async (idx) => {
  if (idx < 0 || !lyricList.value) return
  await nextTick()
  const el = lyricList.value.querySelectorAll('.lyric-line')[idx]
  if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' })
})
</script>

<style scoped>
.music-container { max-width: 1200px; margin: 0 auto; padding: 0 20px 40px; }

/* 大唱片机 */
.hero-player { display: flex; flex-direction: column; align-items: center; padding: 10px 0 20px; }
.vinyl-section { position: relative; width: 220px; height: 220px; margin: 0 auto; }

.vinyl-disc {
  width: 200px; height: 200px; border-radius: 50%;
  background: linear-gradient(135deg, #111 0%, #222 40%, #333 50%, #222 60%, #111 100%);
  border: 3px solid var(--accent);
  box-shadow: 0 0 40px rgba(0,240,255,0.2), 0 0 80px rgba(0,240,255,0.1),
              inset 0 0 30px rgba(0,0,0,0.5);
  display: flex; align-items: center; justify-content: center;
  position: relative; cursor: pointer; transition: box-shadow 0.3s;
  margin: 10px auto;
}
.vinyl-disc:hover { box-shadow: 0 0 60px rgba(0,240,255,0.3), 0 0 100px rgba(0,240,255,0.15); }
.vinyl-disc.spinning { animation: vinyl-spin 4s linear infinite; }
.vinyl-disc.spinning:hover { animation-play-state: paused; }
@keyframes vinyl-spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }

.vinyl-label {
  width: 70px; height: 70px; border-radius: 50%;
  background: linear-gradient(135deg, var(--accent), var(--accent-secondary));
  display: flex; align-items: center; justify-content: center; z-index: 2; position: relative;
  box-shadow: 0 0 15px rgba(0,240,255,0.3);
}
.vinyl-initial { font-size: 28px; font-weight: 700; color: #0a0e27; font-family: monospace; }
.vinyl-ring { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 140px; height: 140px; border-radius: 50%; border: 1px solid rgba(255,255,255,0.05); pointer-events: none; }
.vinyl-ring-2 { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 180px; height: 180px; border-radius: 50%; border: 1px solid rgba(255,255,255,0.03); pointer-events: none; }

.vinyl-arm { position: absolute; top: 20px; right: -20px; width: 60px; height: 8px; transform-origin: right center; transform: rotate(30deg); transition: transform 0.6s; z-index: 3; }
.vinyl-arm.lowered { transform: rotate(0deg); }
.arm-base { position: absolute; right: -4px; top: -6px; width: 16px; height: 20px; border-radius: 50%; background: var(--accent-secondary); box-shadow: 0 0 8px rgba(123,47,247,0.5); }
.arm-body { position: absolute; right: 12px; top: 3px; width: 40px; height: 2px; background: linear-gradient(90deg, var(--accent), var(--accent-secondary)); }
.arm-head { position: absolute; left: 0; top: 0; width: 8px; height: 8px; border-radius: 50%; background: var(--accent); }

.player-info { text-align: center; margin: 12px 0 16px; }
.current-title { font-family: monospace; font-size: 24px; background: linear-gradient(135deg, var(--accent), var(--accent-pink)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.current-artist { color: var(--text-secondary); font-size: 14px; margin-top: 4px; }

.player-controls { display: flex; align-items: center; gap: 20px; margin-bottom: 12px; }
.ctrl-btn { background: none; border: 1px solid var(--border); color: var(--text-primary); width: 40px; height: 40px; border-radius: 50%; cursor: pointer; font-size: 16px; display: flex; align-items: center; justify-content: center; transition: all 0.2s; }
.ctrl-btn:hover { border-color: var(--accent); box-shadow: var(--shadow-glow); }
.ctrl-btn:disabled { opacity: 0.3; cursor: default; }
.ctrl-play { width: 52px; height: 52px; border: 2px solid var(--accent); font-size: 20px; box-shadow: 0 0 20px rgba(0,240,255,0.2); }
.ctrl-play:hover { box-shadow: var(--shadow-glow-strong); }

.progress-section { display: flex; align-items: center; gap: 12px; width: 100%; max-width: 500px; }
.time-label { font-size: 12px; color: var(--text-muted); font-family: monospace; white-space: nowrap; }
.progress-track { flex: 1; height: 4px; background: var(--border); border-radius: 2px; cursor: pointer; position: relative; }
.progress-fill { position: absolute; left: 0; top: 0; height: 100%; background: linear-gradient(90deg, var(--accent), var(--accent-secondary)); border-radius: 2px; transition: width 0.1s; }
.progress-thumb { position: absolute; top: 50%; width: 12px; height: 12px; border-radius: 50%; background: var(--accent); transform: translate(-50%, -50%); box-shadow: 0 0 8px var(--accent); opacity: 0; transition: opacity 0.2s; }
.progress-track:hover .progress-thumb { opacity: 1; }

.volume-section { display: flex; align-items: center; gap: 8px; margin-top: 8px; }
.volume-slider { width: 100px; accent-color: var(--accent); }

.search-section { margin-bottom: 24px; }
.search-bar { display: flex; gap: 12px; max-width: 500px; margin: 0 auto; }
.search-input { flex: 1; padding: 10px 16px; background: var(--bg-secondary); border: 1px solid var(--border); border-radius: var(--radius-sm); color: var(--text-primary); font-size: 14px; outline: none; }
.search-input:focus { border-color: var(--accent); box-shadow: var(--shadow-glow); }

.bottom-columns { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 8px; }
.column { min-height: 300px; max-height: 450px; display: flex; flex-direction: column; }
.column-title { font-size: 16px; font-family: monospace; margin-bottom: 12px; color: var(--accent); letter-spacing: 1px; border-bottom: 1px solid var(--border); padding-bottom: 8px; }
.column-loading { text-align: center; padding: 40px; color: var(--text-secondary); }
.column-empty { text-align: center; padding: 40px; color: var(--text-secondary); }
.spinner-sm { width: 24px; height: 24px; margin: 0 auto 8px; border: 2px solid var(--border); border-top-color: var(--accent); border-radius: 50%; animation: spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

.playlist-list { overflow-y: auto; flex: 1; }
.playlist-list::-webkit-scrollbar { width: 3px; }
.playlist-item { display: flex; align-items: center; gap: 8px; padding: 8px 10px; cursor: pointer; border-radius: 6px; transition: all 0.15s; }
.playlist-item:hover { background: rgba(0,240,255,0.05); }
.playlist-item.active { background: rgba(0,240,255,0.08); border-left: 2px solid var(--accent); }
.pl-idx { width: 20px; color: var(--text-muted); font-size: 12px; text-align: center; }
.pl-info { flex: 1; display: flex; flex-direction: column; min-width: 0; }
.pl-name { font-size: 13px; color: var(--text-primary); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.playlist-item.active .pl-name { color: var(--accent); }
.pl-artist { font-size: 11px; color: var(--text-muted); }
.pl-duration { font-size: 11px; color: var(--text-muted); }
.pl-indicator { font-size: 13px; color: var(--accent); }

.lyric-list { overflow-y: auto; flex: 1; padding: 4px 0; scroll-behavior: smooth; }
.lyric-list::-webkit-scrollbar { width: 3px; }
.lyric-line { padding: 10px 12px; font-size: 14px; color: var(--text-secondary); line-height: 1.6; transition: all 0.3s; border-left: 2px solid transparent; }
.lyric-line.active { color: var(--accent); font-size: 16px; font-weight: 600; border-left-color: var(--accent); background: rgba(0,240,255,0.05); }

@media (max-width: 768px) { .bottom-columns { grid-template-columns: 1fr; } .vinyl-section { width: 170px; height: 170px; } .vinyl-disc { width: 160px; height: 160px; } .vinyl-label { width: 56px; height: 56px; } .vinyl-initial { font-size: 22px; } .vinyl-arm { display: none; } .current-title { font-size: 20px; } }
</style>
