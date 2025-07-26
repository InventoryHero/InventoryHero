import {type Component} from "vue";

export const modals = {
    createRoomModal: defineAsyncComponent(() => import('@/components/storage/rooms/CreateRoomModal.vue')),
    createBoxModal: defineAsyncComponent(() => import('@/components/storage/boxes/modals/CreateBoxModal.vue')),
    createItemModal: defineAsyncComponent(() => import('@/components/items/modals/CreateItemModal.vue')),
    createCategoryModal: defineAsyncComponent(() => import('@/components/categories/CreateCategoryModal.vue')),
    scanQrCodeModal: defineAsyncComponent(() => import('@/components/qr/modals/ScanLabel.vue')),
    editItemInstanceModal: defineAsyncComponent(() => import('@/components/items/modals/EditItemInstanceDialog.vue')),
    editItemModal: defineAsyncComponent(() => import('@/components/items/modals/EditItemDialog.vue')),
    editRoomModal: defineAsyncComponent(() => import("@/components/storage/rooms/modals/EditRoomModal.vue")),
    editBoxModal: defineAsyncComponent(() => import("@/components/storage/boxes/modals/EditBoxModal.vue"))
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

    const onBeforeRouteLeaveHandler = () => {
        if(activeModal.value === null){
            return true
        }

        if(isDirty.value){
            isAwaitingConfirmation.value = true
            return false
        }
        activeModal.value = null
        return false
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
        onBeforeRouteLeaveHandler
    }
}