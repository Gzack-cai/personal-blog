<template>
  <div class="app" :class="{ 'light-mode': isLight }">
    <canvas ref="particleCanvas" class="particle-canvas"></canvas>

    <nav class="navbar">
      <div class="nav-inner">
        <div class="nav-brand">
          <router-link to="/" class="logo glitch-text" data-text="Zack">Zack</router-link>
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
            <span class="nav-text">{{ item.label }}</span>
          </router-link>
        </div>
        <div class="nav-actions">
          <!-- 导航栏迷你播放器 -->
          <div class="mini-player" @click="goToMusic" :title="player.currentSong ? player.currentSong.name : '点击播放音乐'">
            <div class="mini-disc" :class="{ spinning: player.isPlaying }">
              <div class="mini-disc-inner"></div>
            </div>
            <div class="mini-info">
              <span class="mini-name" v-if="player.currentSong">{{ player.currentSong.name }}</span>
              <span class="mini-name" v-else>点击听歌</span>
              <span class="mini-artist" v-if="player.currentSong">{{ player.currentSong.artists?.[0]?.name || '' }}</span>
            </div>
            <button class="mini-play-btn" @click.stop="togglePlayPause">
              {{ player.isPlaying ? '⏸' : '▶' }}
            </button>
          </div>
          <button class="action-btn" @click="toggleTheme" :title="isLight ? '切换深色' : '切换浅色'">
            {{ isLight ? '🌙' : '☀️' }}
          </button>
          <router-link to="/admin" class="action-btn admin-link" title="管理后台">⚙</router-link>
        </div>
      </div>
    </nav>

    <div class="scanlines"></div>

    <!-- 全局歌词面板（非音乐页面显示） -->
    <LyricsPanel />

    <main class="main-content" :class="{ 'with-lyrics': $route.path !== '/music' }">
      <router-view v-slot="{ Component }">
        <transition name="page" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { player, initAudio, playDefault, togglePlayPause, setVolume } from './player'
import LyricsPanel from './components/LyricsPanel.vue'

const route = useRoute()
const router = useRouter()
const isLight = ref(localStorage.getItem('theme') === 'light')
const particleCanvas = ref(null)

const toggleTheme = () => {
  isLight.value = !isLight.value
  localStorage.setItem('theme', isLight.value ? 'light' : 'dark')
  document.documentElement.classList.toggle('light-mode', isLight.value)
}

const initTheme = () => {
  if (isLight.value) {
    document.documentElement.classList.add('light-mode')
  }
}
initTheme()

const goToMusic = () => {
  if (route.path !== '/music') {
    router.push('/music')
  }
}

const navItems = [
  { path: '/profile', label: '个人介绍', icon: '👤' },
  { path: '/projects', label: '项目展示', icon: '💻' },
  { path: '/articles', label: '文章', icon: '📝' },
  { path: '/life', label: '精彩生活', icon: '📸' },
  { path: '/music', label: '音乐', icon: '🎵' },
  { path: '/friends', label: '我的好友', icon: '👥' },
  { path: '/contact', label: '联系我', icon: '📞' },
]

// 粒子背景
let animId = null

onMounted(() => {
  // 初始化音频并播放默认歌曲
  initAudio()
  setTimeout(() => playDefault(), 1000)

  // 粒子动画
  const canvas = particleCanvas.value
  if (!canvas) return
  const ctx = canvas.getContext('2d')

  const resize = () => { canvas.width = window.innerWidth; canvas.height = window.innerHeight }
  window.addEventListener('resize', resize)
  resize()

  const particles = []
  for (let i = 0; i < 60; i++) {
    particles.push({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      vx: (Math.random() - 0.5) * 0.5,
      vy: (Math.random() - 0.5) * 0.5,
      r: Math.random() * 2 + 1,
    })
  }

  const animate = () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    for (const p of particles) {
      p.x += p.vx; p.y += p.vy
      if (p.x < 0 || p.x > canvas.width) p.vx *= -1
      if (p.y < 0 || p.y > canvas.height) p.vy *= -1
      ctx.beginPath()
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2)
      ctx.fillStyle = isLight.value ? 'rgba(0,119,255,0.4)' : 'rgba(0,240,255,0.4)'
      ctx.fill()
    }
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x
        const dy = particles[i].y - particles[j].y
        const dist = Math.sqrt(dx * dx + dy * dy)
        if (dist < 150) {
          const alpha = (1 - dist / 150) * 0.25
          ctx.beginPath()
          ctx.moveTo(particles[i].x, particles[i].y)
          ctx.lineTo(particles[j].x, particles[j].y)
          ctx.strokeStyle = isLight.value ? `rgba(0,119,255,${alpha})` : `rgba(0,240,255,${alpha})`
          ctx.lineWidth = 0.5
          ctx.stroke()
        }
      }
    }
    animId = requestAnimationFrame(animate)
  }
  animate()

  onUnmounted(() => {
    cancelAnimationFrame(animId)
    window.removeEventListener('resize', resize)
  })
})
</script>

<style>
* { margin: 0; padding: 0; box-sizing: border-box; }

:root {
  --bg-primary: #0a0e27;
  --bg-secondary: #131740;
  --bg-card: rgba(255,255,255,0.05);
  --bg-glass: rgba(10,14,39,0.75);
  --accent: #00f0ff;
  --accent-secondary: #7b2ff7;
  --accent-pink: #ff2d78;
  --text-primary: #fff;
  --text-secondary: rgba(255,255,255,0.6);
  --border: rgba(0,240,255,0.2);
  --border-glow: rgba(0,240,255,0.5);
  --shadow-glow: 0 0 15px rgba(0,240,255,0.3);
  --shadow-glow-strong: 0 0 30px rgba(0,240,255,0.5);
  --radius-sm: 8px;
  --radius-md: 12px;
}

html.light-mode, .light-mode {
  --bg-primary: #f0f4ff;
  --bg-secondary: #e8eeff;
  --bg-card: rgba(255,255,255,0.85);
  --bg-glass: rgba(240,244,255,0.85);
  --accent: #0077ff;
  --accent-secondary: #6b3fa0;
  --accent-pink: #ff5a9e;
  --text-primary: #1a1a2e;
  --text-secondary: #555;
  --border: rgba(0,119,255,0.2);
  --border-glow: rgba(0,119,255,0.4);
  --shadow-glow: 0 0 15px rgba(0,119,255,0.2);
}

body {
  font-family: 'Microsoft YaHei', sans-serif;
  background: var(--bg-primary);
  color: var(--text-primary);
  overflow-x: hidden;
}

.app { min-height: 100vh; background: var(--bg-primary); position: relative; }

.particle-canvas {
  position: fixed; top: 0; left: 0;
  width: 100vw; height: 100vh;
  z-index: 0; pointer-events: none;
}

.scanlines {
  position: fixed; top: 0; left: 0;
  width: 100vw; height: 100vh;
  pointer-events: none; z-index: 1;
  background: repeating-linear-gradient(
    0deg, transparent 0px, transparent 2px,
    rgba(0,0,0,0.03) 2px, rgba(0,0,0,0.03) 4px
  );
}

/* 导航栏 */
.navbar {
  position: fixed; top: 0; left: 0; right: 0; z-index: 1000;
  height: 64px; padding: 0 20px;
  border-bottom: 1px solid var(--border);
  background: var(--bg-glass);
  backdrop-filter: blur(20px) saturate(1.5);
}

.nav-inner {
  max-width: 1400px; margin: 0 auto;
  display: flex; align-items: center; height: 100%; gap: 20px;
}

.logo {
  font-family: monospace; font-size: 22px; font-weight: 700;
  color: var(--accent); text-decoration: none;
  text-shadow: 0 0 10px var(--accent), 0 0 20px var(--accent);
  position: relative;
}

.glitch-text::before, .glitch-text::after {
  content: attr(data-text);
  position: absolute; top: 0; left: 0;
  width: 100%; height: 100%; opacity: 0;
}
.glitch-text:hover::before {
  color: #ff2d78;
  animation: glitch-1 0.3s ease infinite;
  opacity: 0.8;
}
.glitch-text:hover::after {
  color: #00f0ff;
  animation: glitch-2 0.3s ease infinite reverse;
  opacity: 0.8;
}
@keyframes glitch-1 {
  0% { transform: translate(0); }
  20% { transform: translate(-2px, 2px); }
  40% { transform: translate(2px, -1px); }
  60% { transform: translate(-1px, 2px); }
  80% { transform: translate(1px, 1px); }
  100% { transform: translate(0); }
}
@keyframes glitch-2 {
  0% { transform: translate(0); }
  20% { transform: translate(2px, -1px); }
  40% { transform: translate(-1px, 2px); }
  60% { transform: translate(1px, -2px); }
  80% { transform: translate(-2px, -1px); }
  100% { transform: translate(0); }
}

.nav-links { display: flex; gap: 4px; flex: 1; justify-content: center; }

.nav-link {
  display: flex; align-items: center; gap: 6px;
  padding: 8px 14px; border-radius: var(--radius-sm);
  color: var(--text-secondary); font-size: 14px;
  text-decoration: none; transition: all 0.2s; position: relative;
}
.nav-link::after {
  content: ''; position: absolute; bottom: 2px; left: 50%;
  transform: translateX(-50%) scaleX(0);
  width: 60%; height: 2px;
  background: var(--accent);
  box-shadow: 0 0 8px var(--accent);
  transition: transform 0.2s;
}
.nav-link:hover::after, .nav-link.active::after { transform: translateX(-50%) scaleX(1); }
.nav-link:hover { color: var(--text-primary); }
.nav-link.active {
  color: var(--accent);
  background: rgba(0,240,255,0.08);
  border: 1px solid var(--border-glow);
  box-shadow: inset 0 0 15px rgba(0,240,255,0.1), 0 0 10px rgba(0,240,255,0.1);
}
.nav-icon { font-size: 16px; }

.nav-actions { display: flex; align-items: center; gap: 8px; }

/* 导航栏迷你播放器 */
.mini-player {
  display: flex; align-items: center; gap: 8px;
  padding: 4px 12px 4px 4px;
  border: 1px solid var(--border);
  border-radius: 24px;
  cursor: pointer;
  transition: all 0.2s;
  background: rgba(0,240,255,0.05);
}
.mini-player:hover { border-color: var(--accent); box-shadow: var(--shadow-glow); }
.mini-disc {
  width: 32px; height: 32px; border-radius: 50%;
  background: linear-gradient(135deg, #1a1a2e, #333);
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
  border: 2px solid var(--accent);
  box-shadow: 0 0 8px rgba(0,240,255,0.3);
}
.mini-disc.spinning { animation: disc-spin 3s linear infinite; }
.mini-disc-inner {
  width: 8px; height: 8px; border-radius: 50%;
  background: var(--accent);
}
@keyframes disc-spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
.mini-info { display: flex; flex-direction: column; line-height: 1.2; }
.mini-name { font-size: 12px; color: var(--text-primary); max-width: 80px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.mini-artist { font-size: 10px; color: var(--text-muted); }
.mini-play-btn {
  background: none; border: none; color: var(--accent);
  font-size: 14px; cursor: pointer; padding: 2px;
}

.action-btn {
  background: none; border: 1px solid var(--border);
  color: var(--text-primary); padding: 6px 10px;
  border-radius: var(--radius-sm); cursor: pointer; font-size: 14px;
  transition: all 0.2s; text-decoration: none;
}
.action-btn:hover { border-color: var(--accent); box-shadow: 0 0 8px rgba(0,240,255,0.2); }
.admin-link { text-decoration: none; }

.main-content {
  padding-top: 70px; min-height: calc(100vh - 70px);
  position: relative; z-index: 2;
  transition: padding-right 0.3s;
}
.main-content.with-lyrics {
  padding-right: 270px;
}

.page-enter-active, .page-leave-active { transition: opacity 0.25s, transform 0.25s; }
.page-enter-from { opacity: 0; transform: translateY(15px); }
.page-leave-to { opacity: 0; transform: translateY(-15px); }

.container { max-width: 1200px; margin: 0 auto; padding: 0 20px; position: relative; z-index: 1; }
.page-header { text-align: center; padding: 40px 20px 30px; }
.page-title {
  font-size: 30px; color: transparent;
  background: linear-gradient(135deg, var(--accent), var(--accent-secondary), var(--accent-pink));
  background-size: 200% 200%;
  -webkit-background-clip: text; background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: gradient-shift 3s ease infinite;
  margin-bottom: 8px; display: inline-block;
}
@keyframes gradient-shift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
.page-subtitle { color: var(--text-secondary); font-size: 14px; }

.neon-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 20px;
  backdrop-filter: blur(10px);
  position: relative;
  overflow: hidden;
  transition: all 0.3s;
}
.neon-card::before {
  content: '';
  position: absolute; top: -2px; left: -2px;
  right: -2px; bottom: -2px;
  background: linear-gradient(45deg, transparent 40%, var(--accent) 50%, transparent 60%);
  background-size: 300% 300%;
  z-index: -1;
  border-radius: calc(var(--radius-md) + 2px);
  opacity: 0;
  transition: opacity 0.3s;
}
.neon-card:hover::before {
  opacity: 1;
  animation: border-shine 1.5s linear 1 forwards;
}
@keyframes border-shine {
  0% { background-position: 0% 50%; }
  100% { background-position: 300% 50%; }
}
.neon-card:hover { border-color: transparent; box-shadow: var(--shadow-glow); transform: translateY(-4px); }

.tag {
  display: inline-block; padding: 4px 12px; border-radius: 20px;
  font-size: 12px; border: 1px solid var(--border);
  color: var(--accent); background: rgba(0,240,255,0.05); margin: 2px;
  transition: all 0.2s;
}
.tag:hover { box-shadow: 0 0 8px rgba(0,240,255,0.3); }

.grid-bg {
  background-image:
    linear-gradient(rgba(0,240,255,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,240,255,0.03) 1px, transparent 1px);
  background-size: 40px 40px;
  position: relative;
}
.light-mode .grid-bg {
  background-image:
    linear-gradient(rgba(0,119,255,0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,119,255,0.04) 1px, transparent 1px);
}

.neon-btn {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 10px 24px; border: 1px solid var(--accent);
  border-radius: var(--radius-sm); background: transparent;
  color: var(--accent); font-family: inherit; font-size: 14px;
  cursor: pointer; transition: all 0.3s; position: relative; overflow: hidden;
}
.neon-btn::after {
  content: ''; position: absolute; inset: 0;
  background: linear-gradient(135deg, var(--accent), transparent);
  opacity: 0; transition: opacity 0.3s;
}
.neon-btn:hover::after { opacity: 0.1; }
.neon-btn:hover { box-shadow: var(--shadow-glow); transform: translateY(-2px); }

.empty-state { text-align: center; padding: 60px 20px; color: var(--text-secondary); }

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--accent); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent-secondary); }

@media (max-width: 900px) {
  .nav-text { display: none; }
  .nav-link { padding: 8px 10px; }
  .mini-info { display: none; }
}
@media (max-width: 1100px) {
  .main-content.with-lyrics { padding-right: 20px; }
}
</style>
