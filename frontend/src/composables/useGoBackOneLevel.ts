import { useRouter, useRoute } from 'vue-router';

export default () => {
    const router = useRouter();
    const route = useRoute();

    const goBackOneLevel = async () => {
        const pathSegments = route.path.split('/');
        const lastSegment = pathSegments[pathSegments.length - 1];

        // Check if the last segment is a number (could be an ID) or something else you want to remove
        if (!isNaN(parseInt(lastSegment))) {
            pathSegments.pop(); // Remove the ID part (or numeric segment)
        }

        pathSegments.pop(); // Remove one more segment (the actual "level" you want to go back to)

        const newPath = pathSegments.join('/');
        await router.push(newPath); // Wait for navigation to complete
    };

    return {
        goBackOneLevel
    };
}
