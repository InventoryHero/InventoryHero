<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "AppConfirmModal",
  emits: {
    accept(){
      return true
    },
    deny(){
      return true
    }
  },
  props: {
    title: {
      type: String,
      default: ""
    },
    body: {
      type: String,
      default: ""
    },
    dialog: {
      type: Boolean,
      required: true
    },
    noClickAnimation: {
      type: Boolean,
      default: false
    },
  },
  methods:{

  }
})
</script>

<template>
<v-dialog

  v-model="dialog"
  :persistent="true"
  :no-click-animation="noClickAnimation"

>
  <v-row
    justify="center"
  >
    <v-col
      cols="12"
      lg="6"
    >
      <v-card
          height="60%"
          class="fill-height"
      >
        <v-card-title
            class="shadowed"
        >
          <slot name="title" >
            {{ title }}
          </slot>
        </v-card-title>
        <v-card-text
            class="mt-4"
            style="height: 25svh"
        >
          <slot name="body">
            {{ body }}
          </slot>
        </v-card-text>
        <v-card-actions
          class="d-flex justify-space-evenly"
        >
          <slot>
            <v-btn
                @click="$emit('deny')"
            >
              {{ $t('confirm.actions.abort')}}
            </v-btn>
            <v-btn
                @click="$emit('accept')"
            >
              {{ $t('confirm.actions.proceed')}}
            </v-btn>
          </slot>
        </v-card-actions>
      </v-card>
    </v-col>
  </v-row>
</v-dialog>
</template>

<style scoped lang="scss">

</style>