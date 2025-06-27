// stores/config.js
import { defineStore } from 'pinia'

export const useConfigStore = defineStore('config', {
  state: () => ({
    settings: {
      textModel: { apiUrl: '', apiKey: '' ,name:"" ,params: { temperature: 1.0 ,maxTokens: 2048 ,generateNum: 3 ,generateTextNum: 100}},
      imageModel: { apiUrl: '', apiKey: '' ,name:""},
    }
  }),
  actions: {
    loadSettings() {
      const saved = localStorage.getItem('settings')
      if (saved) {
        this.settings = JSON.parse(saved)
      }
    },
    saveSettings() {
      localStorage.setItem('settings', JSON.stringify(this.settings))
    }
  }
})