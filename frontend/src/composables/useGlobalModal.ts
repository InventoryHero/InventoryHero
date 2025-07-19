import {type Component} from "vue";

export const modals = {
    createRoomModal: defineAsyncComponent(() => import('@/components/storage/rooms/CreateRoomModal.vue')),
    createBoxModal: defineAsyncComponent(() => import('@/components/storage/boxes/CreateBoxModal.vue')),
    createItemModal: defineAsyncComponent(() => import('@/components/items/modals/CreateItemModal.vue'))
}

export type ModalName = keyof typeof modals

const activeModal = ref<{component: Component; props?: Record<string, any>} | null>(null)
const isDirty = ref<boolean>(false);
const isAwaitingConfirmation = ref(false);

export default () => {

    const openModal = (name: ModalName, props: Record<string, any>|undefined = undefined) => {
        activeModal.value = {
            component: markRaw(modals[name]),
            props
        }
    }

    const leave = () => {
        isAwaitingConfirmation.value = false
        activeModal.value = null
    }
    const stay = () => {
        isAwaitingConfirmation.value = false
    }

    const forceClose = () => {
        activeModal.value = null
    }

    const close = () => {
        if(isDirty.value){
            isAwaitingConfirmation.value = true
            return false
        }
        activeModal.value = null
        return true
    }

    return {
        activeModal,
        isDirty,
        isAwaitingConfirmation,
        openModal,
        leave,
        stay,
        forceClose,
        close,
    }
}