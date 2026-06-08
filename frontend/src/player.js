// 全局音乐播放器状态
import { reactive } from 'vue'

export const player = reactive({
  currentSong: null,
  currentSongId: null,
  isPlaying: false,
  currentTime: 0,
  duration: 0,
  volume: 0.5,
  audio: null,
  // 歌词
  lyrics: [],
  currentLyricIdx: -1,
  // 默认歌曲：老男孩（筷子兄弟）
  defaultSong: {
    id: 2688454170,
    name: '老男孩',
    artists: [{ name: '筷子兄弟' }],
    duration: 300000,
  },
})

// 初始化音频（在 App.vue mounted 中调用）
export function initAudio() {
  if (player.audio) return
  const audio = new Audio()
  audio.volume = player.volume

  audio.addEventListener('timeupdate', () => {
    player.currentTime = audio.currentTime
    updateLyricTime(audio.currentTime)
  })
  audio.addEventListener('ended', () => {
    player.isPlaying = false
  })
  audio.addEventListener('loadedmetadata', () => {
    player.duration = audio.duration
  })
  audio.addEventListener('play', () => { player.isPlaying = true })
  audio.addEventListener('pause', () => { player.isPlaying = false })

  player.audio = audio
  return audio
}

// 播放指定歌曲（先获取播放URL）
export async function playSong(song) {
  if (!player.audio) return
  player.currentSong = song
  player.currentSongId = song.id
  player.currentTime = 0
  player.currentLyricIdx = -1
  try {
    const res = await fetch(`/music-api/song/url/v1?id=${song.id}&level=standard`)
    const data = await res.json()
    if (data.code === 200 && data.data?.[0]?.url) {
      player.audio.src = data.data[0].url
      player.audio.play()
    }
    // 同时获取歌词
    fetchLyrics(song.id)
  } catch (e) {
    console.error('Play failed:', e)
  }
}

// 获取歌词
export async function fetchLyrics(songId) {
  if (!songId) { player.lyrics = []; return }
  try {
    const res = await fetch(`/music-api/lyric?id=${songId}`)
    const data = await res.json()
    const lrc = data?.lrc?.lyric || ''
    if (lrc) {
      player.lyrics = parseLrc(lrc)
    } else {
      player.lyrics = []
    }
  } catch (e) {
    player.lyrics = []
  }
}

// 解析 LRC 歌词
const parseLrc = (lrc) => {
  const lines = lrc.split('\n')
  const result = []
  const timeRe = /\[(\d{2}):(\d{2})\.(\d{2,3})\]/
  for (const line of lines) {
    const match = line.match(timeRe)
    if (match) {
      const min = parseInt(match[1])
      const sec = parseInt(match[2])
      const ms = parseInt(match[3].padEnd(3, '0'))
      const time = min * 60 + sec + ms / 1000
      const text = line.replace(timeRe, '').trim()
      if (text) result.push({ time, text })
    }
  }
  return result.sort((a, b) => a.time - b.time)
}

// 根据当前时间更新歌词索引
const updateLyricTime = (currentTime) => {
  if (!currentTime || player.lyrics.length === 0) {
    player.currentLyricIdx = -1
    return
  }
  let idx = -1
  for (let i = player.lyrics.length - 1; i >= 0; i--) {
    if (currentTime >= player.lyrics[i].time) { idx = i; break }
  }
  player.currentLyricIdx = idx
}

// 播放默认歌曲
export function playDefault() {
  playSong(player.defaultSong)
}

// 切换播放/暂停
export function togglePlayPause() {
  if (!player.audio || !player.currentSong) {
    playDefault()
    return
  }
  if (player.audio.paused) {
    player.audio.play()
  } else {
    player.audio.pause()
  }
}

// 设置音量
export function setVolume(val) {
  player.volume = val
  if (player.audio) player.audio.volume = val
}

// 跳转进度
export function seek(time) {
  if (player.audio) player.audio.currentTime = time
}

// 格式化时间
export function formatTime(ms) {
  if (!ms || ms <= 0) return '00:00'
  const totalSec = Math.floor(ms / 1000)
  const min = Math.floor(totalSec / 60)
  const sec = totalSec % 60
  return `${String(min).padStart(2, '0')}:${String(sec).padStart(2, '0')}`
}
