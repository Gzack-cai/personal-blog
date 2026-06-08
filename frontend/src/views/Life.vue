<template>
  <div class="life-page grid-bg">
    <div class="page-header">
      <h1 class="page-title">精彩生活</h1>
      <p class="page-subtitle">记录生活的美好瞬间 · 点击节点查看</p>
    </div>

    <!-- 3D 网状布局 -->
    <div v-if="moments.length > 0" class="network-container">
      <div class="network-scene" ref="scene" @mousemove="onMouseMove">
        <div class="network-rotator" ref="rotator" :style="rotatorStyle">
          <div
            v-for="(m, idx) in moments"
            :key="m.id"
            class="node"
            :class="{ active: selectedId === m.id }"
            :style="getNodeStyle(idx)"
            @click="selectNode(m)"
          >
            <div class="node-dot">
              <span class="node-initial">{{ m.title?.charAt(0) || '♪' }}</span>
            </div>
            <div class="node-label">{{ m.title }}</div>
          </div>

          <!-- 连接线（SVG） -->
          <svg class="network-lines" :width="sceneSize" :height="sceneSize">
            <line
              v-for="(line, i) in lines"
              :key="'line-'+i"
              :x1="line.x1" :y1="line.y1"
              :x2="line.x2" :y2="line.y2"
              class="net-line"
              :class="{ active: line.active }"
            />
          </svg>
        </div>
      </div>

      <!-- 选中节点的详情弹出 -->
      <transition name="fade">
        <div v-if="selectedNode" class="detail-modal" @click.self="selectedNode = null">
          <div class="detail-card neon-card">
            <button class="detail-close" @click="selectedNode = null">✕</button>
            <div v-if="selectedNode.image" class="detail-image">
              <img :src="selectedNode.image" :alt="selectedNode.title" />
            </div>
            <div class="detail-body">
              <h2 class="detail-title">{{ selectedNode.title }}</h2>
              <p class="detail-date">{{ selectedNode.date }}</p>
              <p class="detail-content">{{ selectedNode.content }}</p>
            </div>
          </div>
        </div>
      </transition>
    </div>

    <div v-else class="empty-state">暂无内容</div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const moments = ref([])
const scene = ref(null)
const rotator = ref(null)
const selectedId = ref(null)
const selectedNode = ref(null)
const sceneSize = 600
const radius = 200
const mouseX = ref(0)
const mouseY = ref(0)
const autoRotate = ref(0)
let animFrame = null

// 计算节点在3D球体上的位置
const getNodePos = (idx, total) => {
  // 均匀分布在球面上 (Fibonacci sphere)
  const phi = Math.acos(1 - 2 * (idx + 0.5) / total)
  const theta = Math.PI * (1 + Math.sqrt(5)) * (idx + 0.5)
  return {
    x: radius * Math.sin(phi) * Math.cos(theta),
    y: radius * Math.sin(phi) * Math.sin(theta),
    z: radius * Math.cos(phi),
  }
}

const nodes = computed(() => {
  return moments.value.map((m, idx) => ({
    ...getNodePos(idx, moments.value.length),
    item: m,
  }))
})

const getNodeStyle = (idx) => {
  const p = getNodePos(idx, moments.value.length)
  // 投影到屏幕坐标 (忽略Z，Z决定大小)
  const scale = 0.8 + (p.z + radius) / (radius * 2) * 0.4
  const cx = sceneSize / 2
  const cy = sceneSize / 2
  return {
    left: `${cx + p.x - 20}px`,
    top: `${cy + p.y - 20}px`,
    transform: `scale(${scale})`,
    zIndex: Math.round(p.z + radius),
  }
}

// 连接线
const lines = computed(() => {
  const result = []
  const n = nodes.value
  for (let i = 0; i < n.length; i++) {
    for (let j = i + 1; j < n.length; j++) {
      // 只有距离近的连
      const dx = n[i].x - n[j].x
      const dy = n[i].y - n[j].y
      const dz = n[i].z - n[j].z
      const dist = Math.sqrt(dx * dx + dy * dy + dz * dz)
      if (dist < radius * 1.6) {
        const cx = sceneSize / 2
        const cy = sceneSize / 2
        const active = selectedId.value === n[i].item.id || selectedId.value === n[j].item.id
        result.push({
          x1: cx + n[i].x, y1: cy + n[i].y,
          x2: cx + n[j].x, y2: cy + n[j].y,
          active,
        })
      }
    }
  }
  return result
})

const selectNode = (m) => {
  selectedId.value = m.id
  selectedNode.value = m
}

// 鼠标控制旋转
const onMouseMove = (e) => {
  if (!scene.value) return
  const rect = scene.value.getBoundingClientRect()
  mouseX.value = ((e.clientX - rect.left) / rect.width - 0.5) * 2
  mouseY.value = ((e.clientY - rect.top) / rect.height - 0.5) * 2
}

const rotatorStyle = computed(() => ({
  transform: `rotateY(${mouseX.value * 30 + autoRotate.value}deg) rotateX(${mouseY.value * -15}deg)`,
}))

onMounted(async () => {
  try {
    const r = await fetch('/api/life')
    const j = await r.json()
    if (j.data) moments.value = j.data
  } catch (e) { console.log('API unavailable') }

  // 自动缓慢旋转
  const animate = () => {
    if (!selectedNode.value) {
      autoRotate.value += 0.2
    }
    animFrame = requestAnimationFrame(animate)
  }
  animFrame = requestAnimationFrame(animate)
})

onUnmounted(() => {
  if (animFrame) cancelAnimationFrame(animFrame)
})
</script>

<style scoped>
.life-page { min-height: calc(100vh - 70px); }

.network-container {
  display: flex; justify-content: center;
  padding-bottom: 40px;
}

.network-scene {
  width: 600px; height: 600px;
  perspective: 800px;
  cursor: grab;
  position: relative;
}

.network-scene:active { cursor: grabbing; }

.network-rotator {
  width: 100%; height: 100%;
  position: relative;
  transform-style: preserve-3d;
  transition: transform 0.1s ease-out;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 节点 */
.node {
  position: absolute;
  width: 40px; height: 40px;
  cursor: pointer;
  transition: all 0.3s;
  text-align: center;
}

.node:hover .node-dot {
  box-shadow: 0 0 25px var(--accent), 0 0 50px var(--accent-secondary);
  border-color: var(--accent);
  transform: scale(1.3);
}

.node.active .node-dot {
  border-color: var(--accent-pink);
  box-shadow: 0 0 30px var(--accent-pink), 0 0 60px var(--accent-pink);
}

.node-dot {
  width: 40px; height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--bg-secondary), #1a1a3e);
  border: 2px solid var(--accent-secondary);
  display: flex; align-items: center; justify-content: center;
  margin: 0 auto 4px;
  transition: all 0.3s;
  box-shadow: 0 0 10px rgba(0,240,255,0.2);
  position: relative;
}

.node-dot::after {
  content: '';
  position: absolute; inset: -3px;
  border-radius: 50%;
  border: 1px solid rgba(0,240,255,0.1);
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 0.5; }
  50% { transform: scale(1.2); opacity: 1; }
}

.node-initial {
  font-size: 16px; font-weight: 700;
  color: var(--accent);
  font-family: monospace;
}

.node-label {
  font-size: 10px;
  color: var(--text-secondary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 80px;
  margin: 0 auto;
  text-shadow: 0 0 8px rgba(0,0,0,0.8);
}

/* SVG连线 */
.network-lines {
  position: absolute; top: 0; left: 0;
  width: 100%; height: 100%;
  pointer-events: none;
}

.net-line {
  stroke: var(--border);
  stroke-width: 1;
  stroke-dasharray: 4, 3;
  transition: all 0.3s;
}

.net-line.active {
  stroke: var(--accent);
  stroke-width: 1.5;
  stroke-dasharray: none;
  box-shadow: 0 0 6px var(--accent);
}

/* 详情弹窗 */
.detail-modal {
  position: fixed; top: 0; left: 0; right: 0; bottom: 0;
  z-index: 2000;
  background: rgba(0,0,0,0.6);
  backdrop-filter: blur(8px);
  display: flex; align-items: center; justify-content: center;
  padding: 20px;
}

.detail-card {
  max-width: 500px; width: 100%;
  padding: 0; overflow: hidden;
  position: relative;
}

.detail-close {
  position: absolute; top: 12px; right: 12px; z-index: 10;
  background: rgba(0,0,0,0.5); border: 1px solid var(--border);
  color: var(--text-primary); width: 32px; height: 32px;
  border-radius: 50%; cursor: pointer; font-size: 16px;
  display: flex; align-items: center; justify-content: center;
  transition: all 0.2s;
}
.detail-close:hover { border-color: var(--accent); box-shadow: var(--shadow-glow); }

.detail-image {
  width: 100%; height: 280px;
  overflow: hidden;
  background: var(--bg-secondary);
}
.detail-image img { width: 100%; height: 100%; object-fit: cover; }

.detail-body { padding: 24px; }

.detail-title {
  font-family: monospace; font-size: 22px; margin-bottom: 6px;
  background: linear-gradient(135deg, var(--accent), var(--accent-pink));
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
}

.detail-date {
  font-size: 13px; color: var(--text-muted);
  margin-bottom: 16px;
}

.detail-content {
  color: var(--text-secondary); font-size: 15px; line-height: 1.8;
}

/* 过渡动画 */
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

@media (max-width: 700px) {
  .network-scene { width: 360px; height: 360px; perspective: 500px; }
}
</style>
