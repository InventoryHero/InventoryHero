<script setup lang="ts">
import {storeToRefs} from "pinia";
import useContentRefreshStore from "@/store/useContentRefreshStore.ts";
import {useConfigStore} from "@/store";
const contentRefreshStore = useContentRefreshStore()
const configStore = useConfigStore()

const {isVisible, actionCallback, title, subtitle} = storeToRefs(contentRefreshStore)
const handleClickOnRefreshBanner = () => {
  if(actionCallback.value) {
    actionCallback.value()
  }
  contentRefreshStore.clearBanner()
}
const transition = computed(() => {
  if(configStore.transitions){
    return {
      name: "scale",
      mode: "out-in"
    }
  }
  return {
    name: "", mode: ""
  }
})

</script>

<template>
  <v-hover>
    <template v-slot:default="{ isHovering, props }">
      <transition :name="transition.name" :mode="transition.mode">
        <v-alert
            v-if="isVisible"
            v-bind="props"
            density="compact"
            class="text-center content-changed-banner mb-4"
            :class="{
            'hover': isHovering
          }"
            width="100%"
            color="info"
            @click="handleClickOnRefreshBanner"
        >
          <template v-slot:text>
            <span class="text-center text-h5">
              {{ title }}
            </span>
            <br />
            <span v-if="subtitle" class="text-center text-medium-emphasis">
              {{ subtitle }}
            </span>
          </template>
        </v-alert>
      </transition>
    </template>
  </v-hover>
</template>

<style scoped lang="scss">
.hover{
  cursor: pointer;
}
</style>