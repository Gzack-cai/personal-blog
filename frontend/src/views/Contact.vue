<template>
  <div class="grid-bg" style="min-height: calc(100vh - 70px);">
    <div class="container">
      <div class="page-header">
        <h1 class="page-title">联系我</h1>
        <p class="page-subtitle">有任何问题或合作意向，欢迎联系</p>
      </div>
      <div class="contact-card neon-card">
        <div v-if="success" class="success-msg">
          <p>✅ 消息已发送成功！</p>
        </div>
        <form v-else @submit.prevent="submitForm" class="contact-form">
          <input v-model="form.name" placeholder="你的名字" class="form-input" required />
          <input v-model="form.email" type="email" placeholder="你的邮箱" class="form-input" required />
          <textarea v-model="form.message" placeholder="你的消息" class="form-input form-textarea" rows="5" required></textarea>
          <button type="submit" class="neon-btn">发送消息</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const form = ref({ name: '', email: '', message: '' })
const success = ref(false)
const submitForm = async () => {
  try {
    await fetch('/api/contact', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(form.value) })
    success.value = true
  } catch(e) { console.log('API unavailable') }
}
</script>

<style scoped>
.contact-card { max-width: 600px; margin: 0 auto 40px; padding: 40px 30px; }
.contact-form { display: flex; flex-direction: column; gap: 16px; }
.form-input {
  width: 100%; padding: 12px 16px; background: var(--bg-secondary);
  border: 1px solid var(--border); border-radius: var(--radius-sm);
  color: var(--text-primary); font-size: 14px; outline: none;
}
.form-input:focus { border-color: var(--accent); box-shadow: var(--shadow-glow); }
.form-textarea { resize: vertical; min-height: 120px; }
.submit-btn { align-self: flex-start; padding: 12px 32px; }
.success-msg { text-align: center; padding: 40px; font-size: 18px; }
</style>
