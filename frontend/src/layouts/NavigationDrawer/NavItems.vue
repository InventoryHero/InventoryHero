<script setup lang="ts">
import {useModal} from "@/composables-new/useModal.ts";

const {mdAndUp} = useDisplay()
const {t} = useI18n()
const {openModal} = useModal()



const createExpanded = shallowRef()



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
        color="primary"
        class="mb-2"
    >
      <v-menu
          v-model="createExpanded"
          activator="parent"
          :location="location"
          :offset="offset"

      >
        <v-list
        >
          <v-list-item>
            item
          </v-list-item>
          <v-list-item>
            box
          </v-list-item>
          <v-list-item
            :title="t('create.room.short_title')"
            @click="openModal('createRoomModal', {
              blockNavigation: true
            })"
          />
          <v-list-item>
            category
          </v-list-item>
        </v-list>
      </v-menu>
    </v-list-item>


    <v-list-item
        to="/items"
        prepend-icon="mdi-invoice-list"
        :title="t('nav.items')"
        color="accent"
    />
    <v-list-item
        to="/boxes"
        prepend-icon="mdi-package-variant"
        :title="t('nav.boxes')"
        color="accent"
    />
    <v-list-item
        to="/rooms"
        prepend-icon="mdi-door"
        :title="t('nav.rooms')"
        color="accent"
    />

  </v-list>
</template>

<style scoped lang="scss">

</style>