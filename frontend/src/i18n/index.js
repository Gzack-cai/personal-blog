import { createI18n } from 'vue-i18n'
import zh from '@/locales/zh.json'
import en from '@/locales/en.json'

const savedLang = localStorage.getItem('lang') || 'zh'

const i18n = createI18n({
  legacy: true,
  locale: savedLang,
  fallbackLocale: 'zh',
  messages: { zh, en },
})

export default i18n
