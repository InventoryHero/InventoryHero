<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "CreateCard",
  inject: ['loading'],
  emits:{
    clear(){
      return true;
    },
    save(){
      return true
    }
  },
  computed: {
    resourcesLoading(){
      return (this.loading.loadingBoxes ?? false) ||
              (this.loading.loadingProducts ?? false) ||
              (this.loading.loadingLocations ?? false)
    }
  },
  props: {
    requestInProgress: {
      type: Boolean,
      default: false
    },
    title: {
      type: String,
      required: true,
    }
  }
})
</script>

<template>
  <v-card
      elevation="5"
  >

    <v-progress-linear
        :indeterminate="true"
        :active="requestInProgress"
        color="primary"
    />
    <v-card-title
        class="shadowed mb-4"
    >
      {{ title }}
    </v-card-title>
    <v-card-text
        class="create-card-content"
    >
      <slot />

    </v-card-text>

    <v-card-actions
        class="d-flex justify-space-between shadowed mt-4"
    >
      <v-btn
          color="red-lighten-1"
          variant="outlined"
          @click="$emit('clear')"
      >
        <template #prepend>
          <v-icon
              color="red"
              icon="mdi-trash-can"
          />
        </template>
        {{$t('add.clear')}}
      </v-btn>
      <v-btn
          color="primary"
          variant="elevated"
          :disabled="resourcesLoading"
          @click="() => {
            if(!resourcesLoading){
              $emit('save')
            }
          }"
      >
        <template #prepend>
          <v-icon
              icon="mdi-content-save"
          />
        </template>
        {{$t('add.save')}}
      </v-btn>
    </v-card-actions>
  </v-card>

</template>

<style scoped lang="scss">

</style>