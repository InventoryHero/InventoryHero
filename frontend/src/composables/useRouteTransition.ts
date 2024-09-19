import { ref, watch } from 'vue';
import { useRoute } from 'vue-router';

export default () => {
    const route = useRoute();
    const transitionDirection = ref('');

    watch(
        () => route.fullPath,
        (newPath, oldPath) => {
            if (newPath !== oldPath) {
                transitionDirection.value = newPath > oldPath ? 'forward' : 'backward';
            }
        }
    );

    return {
        transitionDirection,
    };
}
