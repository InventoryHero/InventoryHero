import {type Component} from "vue";
import {RouteLocationNormalized} from "vue-router";

export const modals = {
    createRoomModal: defineAsyncComponent(() => import('@/components/storage/rooms/CreateRoomModal.vue')),
}

export type ModalName = keyof typeof modals

type ModalOptions = {
    props?: Record<string, any>;
    blockNavigation?: boolean;
}

const activeModal = ref<{component: Component; props?: Record<string, any>} | null>(null)
const isAwaitingConfirmation = ref(false);
const pendingNavigation = ref<RouteLocationNormalized | null>(null);
const forceNavigation = ref<boolean>(false);
let showCloseConfirmation = ref<boolean>(false);

// This function is the only way other components can interact with the state.
export function useModal() {
    const router = useRouter();

    const open = (
        modalName: ModalName,
        options: ModalOptions = {},
    ) => {
        const {props = {}, blockNavigation = false} = options
        activeModal.value = {
            component: markRaw(modals[modalName]),
            props: props
        }
        showCloseConfirmation.value = blockNavigation
    }

    const close = (to: RouteLocationNormalized|null = null) => {
        if(showCloseConfirmation.value && !forceNavigation.value) {
            pendingNavigation.value = to
            isAwaitingConfirmation.value = true
            return true
        }
        if (activeModal.value) {
            forceNavigation.value = false
            activeModal.value = null
        }
    }

    const confirmLeave = () => {
        if(activeModal.value){
            activeModal.value = null
        }
        isAwaitingConfirmation.value = false;
        if(pendingNavigation.value){
            router.push(pendingNavigation.value.fullPath)
        }
    }

    const cancelLeave = () => {
        pendingNavigation.value = null
        isAwaitingConfirmation.value = false;
    }

    return {
        activeModal: readonly(activeModal),
        openModal: open,
        closeModal: close,
        isAwaitingConfirmation: readonly(isAwaitingConfirmation),
        confirmLeave,
        cancelLeave,
        forceNavigation,
    }
}