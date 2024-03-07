<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {Location} from '@/types'

export default defineComponent({
  name: "LocationCard",
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
    boxesAmount: {
      type: Number,
      default: 0
    },
    location: {
      type: Object as PropType<Location>,
      default: undefined
    },
  }
})
</script>

<template>
  <v-row
      :no-gutters="true"
      justify="center"

  >
    <v-col
        cols="11"
    >
      <v-hover>
        <template #default="{isHovering}">
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
                  {{ $t('locations.location.created') }}
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
                  {{ $t('locations.location.product_amount') }}
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
              >
                <v-col
                    cols="6"
                >
                  {{ $t('locations.location.boxes_amount') }}
                </v-col>
                <v-col
                    cols="6"
                    class="d-flex justify-end"
                >
                  {{ boxesAmount }}
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
    </v-col>
  </v-row>
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