#!/usr/bin/env node
// 网易云音乐 API 服务
const path = require('path')

// 使用 NeteaseCloudMusicApi 包
const ncmPath = path.resolve(__dirname, 'node_modules', 'NeteaseCloudMusicApi')
const serveNcmApi = require(path.join(ncmPath, 'server')).serveNcmApi

// 设置端口
process.env.PORT = process.env.PORT || '3001'

console.log('🎵 网易云音乐 API 服务启动中...')
console.log(`   端口: ${process.env.PORT}`)
console.log(`   接口: http://localhost:${process.env.PORT}`)

serveNcmApi({
  checkVersion: true,
})
