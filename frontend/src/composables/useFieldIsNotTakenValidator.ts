import { ref } from 'vue';

export default (errorMessage: string) => {
    const isTaken = ref(false); // This should be updated based on your actual logic

    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const validateField = (_: string) => {
        if (isTaken.value) {
            return errorMessage
        }
        return true;
    };

    return { isTaken, validateField };
}
