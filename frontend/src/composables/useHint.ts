import {computed, ref} from "vue";

export default (text: string) => {
    const hint = text
    const hintActive = ref(false)
    const message = computed(() => {
        return hintActive.value ? hint : ''
    })

    return {
        hintActive,
        message
    }
}