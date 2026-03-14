import { type Component } from 'vue'

export const modals = {
  createRoomModal: defineAsyncComponent(
    () => import('@/components/storage/rooms/CreateRoomModal.vue')
  ),
  createBoxModal: defineAsyncComponent(
    () => import('@/components/storage/boxes/modals/CreateBoxModal.vue')
  ),
  createItemModal: defineAsyncComponent(
    () => import('@/components/items/modals/CreateItemModal.vue')
  ),
  createCategoryModal: defineAsyncComponent(
    () => import('@/components/categories/CreateCategoryModal.vue')
  ),
  scanQrCodeModal: defineAsyncComponent(
    () => import('@/components/qr/modals/ScanLabel.vue')
  ),
  editItemInstanceModal: defineAsyncComponent(
    () => import('@/components/items/modals/EditItemInstanceDialog.vue')
  ),
  editItemModal: defineAsyncComponent(
    () => import('@/components/items/modals/EditItemDialog.vue')
  ),
  editRoomModal: defineAsyncComponent(
    () => import('@/components/storage/rooms/modals/EditRoomModal.vue')
  ),
  editBoxModal: defineAsyncComponent(
    () => import('@/components/storage/boxes/modals/EditBoxModal.vue')
  )
}

export type ModalName = keyof typeof modals

const activeModal = ref<{
  component: Component
  props?: Record<string, any>
} | null>(null)

export default () => {
  const openModal = (
    name: ModalName,
    props: Record<string, any> | undefined = undefined
  ) => {
    activeModal.value = {
      component: markRaw(modals[name]),
      props
    }
  }

  return {
    activeModal,
    openModal
  }
}
