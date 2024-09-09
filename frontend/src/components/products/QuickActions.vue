<script setup lang="ts">

const $emit = defineEmits<{
  (e: 'deleteMe'): void,
  (e: 'updateAmount', increment: number): void,
  (e: 'showDetails'): void
}>()

const {requestInProgress=false, disabled=false} = defineProps<{
  requestInProgress: boolean,
  disabled?: boolean,
}>()


</script>

<template>
  <v-row
      :no-gutters="true"
      justify="space-evenly"
      class="product-actions mt-2 mb-1 position-relative"
      :class="{
        'request': requestInProgress
      }"
  >
    <v-overlay
        :contained="true"
        :model-value="requestInProgress"
        width="100%"
        class="align-center justify-center test"
    >
      <v-progress-linear
          :indeterminate="true"
          color="primary"
          :active="true"

      />
    </v-overlay>
    <v-col>
      <app-icon-btn
          :disabled="disabled"
          icon="mdi-trash-can"
          @click="$emit('deleteMe')"
      />
    </v-col>
    <v-col>
      <app-icon-btn
          :disabled="disabled"
          icon="mdi-minus"
          @click="$emit('updateAmount', -1)"
      />
    </v-col>
    <v-col>
      <app-icon-btn
          :disabled="disabled"
          icon="mdi-plus"
          @click="$emit('updateAmount', +1)"
      />
    </v-col>

    <v-col>
      <app-icon-btn
          :disabled="disabled"
          @click="$emit('showDetails')"
          icon="mdi-information"
      />
    </v-col>


  </v-row>
</template>

<style scoped lang="scss">
:deep(.v-col){
  display: flex;
  justify-content: center;
  align-items: center;
}


.request{
  :deep(.v-icon){
    &.v-theme--dark{
      color: rgba(255, 255, 255, 0.45);
    }
    &.v-theme--light{
      color: rgba(0, 0, 0, 0.45);
    }
  }
}
</style>