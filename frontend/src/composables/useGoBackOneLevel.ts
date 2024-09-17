import { useRouter, useRoute } from 'vue-router';

export default ({hasId = false} = {}) => {
    const router = useRouter();
    const route = useRoute();

    const goBackOneLevel = async () => {
        const pathSegments = route.path.split('/');
        pathSegments.pop();
        if (hasId) {
            pathSegments.pop();
        }
        const newPath = pathSegments.join('/');
        await router.push(newPath);
    };

    return {
        goBackOneLevel
    };
}