<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "QuickActions",
  emits:{
    deleteMe(){
      return true;
    },
    updateAmount(increment: number)
    {
      return true;
    },
    showDetails(){
      return true;
    }
  },


  props: {
    requestInProgress: {
      type: Boolean,
      default: false
    },
    amountOnly: {
      type: Boolean,
      default: false
    },
    amount:{
      type: Number,
      default: 0
    },
    disabled: {
      type: Boolean,
      default: false
    }
  }
})
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
        v-model="requestInProgress"
        width="100%"
        class="align-center justify-center test"
    >
      <v-progress-linear
          :indeterminate="true"
          color="primary"
          :active="true"

      />

    </v-overlay>
    <v-col
        v-if="!amountOnly"
    >
      <app-icon-btn
          :disabled="disabled"
          icon="fa:fas fa-trash"
          @click="$emit('deleteMe')"
      />
    </v-col>
    <v-col>
      <app-icon-btn
          :disabled="disabled"
          icon="fa:fas fa-minus"
          @click="$emit('updateAmount', -1)"
      />
    </v-col>
    <v-col
        v-if="amountOnly"
    >
      <slot name="amount"></slot>
    </v-col>
    <v-col>
      <app-icon-btn
          :disabled="disabled"
          icon="fa:fas fa-plus"
          @click="$emit('updateAmount', +1)"
      />
    </v-col>

    <v-col
      v-if="!amountOnly"
    >
      <app-icon-btn
          :disabled="disabled"
          @click="$emit('showDetails')"
          icon="fa:fas fa-info-circle"
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