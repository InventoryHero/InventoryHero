<script setup lang="ts">

const {mdAndUp} = useDisplay()
const {t} = useI18n()

const createExpanded = shallowRef()

const emit = defineEmits<{
  (e: 'openCreateItemModal'): void,
  (e: 'openCreateBoxModal'): void,
  (e: 'openCreateRoomModal'): void,
  (e: 'openCreateCategoryModal'): void,
}>()

const location = computed(() => {
  if(mdAndUp.value) {
    return "right"
  }
  return "bottom"
})
const offset = computed(() => {
  if(mdAndUp.value) {
    return "12"
  }
  return "4"
})
onBeforeRouteLeave(() => {
  createExpanded.value = false
  return true
})
</script>

<template>
  <v-list
      density="compact"
      nav
  >
    <v-list-item
        prepend-icon="mdi-plus-box"
        :title="t('nav.create')"
        :active="createExpanded"
        class="mb-2"
        color="primary"
    >
      <v-menu
          v-model="createExpanded"
          activator="parent"
          :location="location"
          :offset="offset"
          :close-on-back="true"

      >
        <v-list
        >
          <v-list-item
            :title="t('create.item.short_title')"
            @click="emit('openCreateItemModal')"
          />
          <v-list-item
            :title="t('create.box.short_title')"
            @click="emit('openCreateBoxModal')"
          />
          <v-list-item
            :title="t('create.room.short_title')"
            @click="emit('openCreateRoomModal')"
          />
          <v-list-item
            :title="t('create.category.short_title')"
            @click="emit('openCreateCategoryModal')"
          />
        </v-list>
      </v-menu>
    </v-list-item>


    <v-list-item
        to="/items"
        prepend-icon="mdi-invoice-list"
        :title="t('nav.items')"
        color="primary"
    />
    <v-list-item
        to="/storage/boxes"
        prepend-icon="mdi-package-variant"
        :title="t('nav.boxes')"
        color="primary"
    />
    <v-list-item
        to="/storage/rooms"
        prepend-icon="mdi-door"
        :title="t('nav.rooms')"
        color="primary"
    />

    <v-list-item
        to="/households"
        prepend-icon="mdi-home-account"
        :title="t('nav.households')"
        color="primary"
    />
    <v-list-item
      to="/qr"
      prepend-icon="mdi-qrcode-edit"
      :title="t('nav.qrcode-edit')"
      color="primary"
    />

  </v-list>
</template>

<style scoped lang="scss">

</style>
