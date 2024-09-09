import { ref } from 'vue';
import { useI18n } from 'vue-i18n';

export default (errorMessage: string) => {
    const isTaken = ref(false); // This should be updated based on your actual logic

    const validateField = (_: string) => {
        if (isTaken.value) {
            return errorMessage
        }
        return true;
    };

    return { isTaken, validateField };
}
