<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {Location} from '@/types'

export default defineComponent({
  name: "BoxCard",
  emits:{
    showOverlay(){
      return true;
    }
  },
  props: {
    id: {
      type: Number,
      required: true
    },
    name: {
      type: String,
      required: true
    },
    creationDate: {
      type: String,
      required: true
    },
    productAmount: {
      type: Number,
      default: 0
    },
    location: {
      type: Object as PropType<Location>,
      default: undefined
    }
  }
})
</script>

<template>
  <v-hover>
    <template v-slot:default="{isHovering}">
      <v-card

          :elevation="0"
          :class="{
            'hovering': isHovering
          }"
          @click="$emit('showOverlay')"
      >
        <v-card-title
          class="title"
        >
          {{ name }}
        </v-card-title>
        <v-card-subtitle
            class="mb-1"
        >
          <v-row
              :no-gutters="true"
              justify="center"
          >
            <v-col
                cols="6"
            >
              {{ $t('boxes.box.created') }}
            </v-col>
            <v-col
                cols="6"
                class="d-flex justify-end"
            >
              {{ $d(new Date(creationDate)) }}
            </v-col>
          </v-row>
          <v-row

              :no-gutters="true"
              justify="center"
          >
            <v-col
                cols="6"
            >
              {{ $t('boxes.box.product_amount') }}
            </v-col>
            <v-col
                cols="6"
                class="d-flex justify-end"
            >
              {{ productAmount }}
            </v-col>
          </v-row>
          <v-row

              :no-gutters="true"
              justify="center"
              v-if="location !== undefined"
          >
            <v-col
                cols="6"
            >
              {{ $t('boxes.box.product_amount') }}
            </v-col>
            <v-col
                cols="6"
                class="d-flex justify-end"
            >
              {{ location!.name }}
            </v-col>
          </v-row>
        </v-card-subtitle>
      </v-card>
      <slot name="divider" >
        <v-divider
            color="primary"
            class="border-opacity-75"
        />
      </slot>
    </template>
  </v-hover>
</template>

<style scoped lang="scss">
  .title {
    margin-bottom: 0 !important;
    padding-bottom: 0 !important;
  }

  .hovering{
    background-color: rgba(var(--v-theme-primary), 0.15);
  }
</style>