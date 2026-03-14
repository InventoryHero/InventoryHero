// src/stores/bannerStore.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'

type ShowBannerOptions = {
    title: string,
    subtitle?: string,
    callback?: (() => void)
}

export default defineStore('banner', () => {
    const isVisible = ref(false)
    const title = ref('')
    const subtitle = ref<string|null>(null)
    const actionCallback = ref<(() => void) | null>(null)

    function showBanner(options: ShowBannerOptions) {
        title.value = options.title
        subtitle.value = options.subtitle ?? null
        actionCallback.value = options.callback ?? null
        isVisible.value = true
    }

    function clearBanner() {
        isVisible.value = false
        title.value = ''
        actionCallback.value = null
    }

    return { isVisible, title, subtitle, actionCallback, showBanner, clearBanner }
})