<script lang="ts">
import {defineComponent} from 'vue'
import {ApiStorage} from "@/types";

export default defineComponent({
  name: "PrintQrModal",
  computed:{
    visible:{
      get(){
        return this.modelValue
      },
      set(value: boolean){
        this.$emit('update:model-value',value)
      }
    },
    allSelected:{
      get(){
        return this.storage.every(storage => this.checkedItems[storage.id] === true)
      },
      set(value: boolean){
        if(!value)
        {
          this.checkedItems = {} as {[key: number]: boolean}//Object.fromEntries(this.storage.map(x => [x.id, false]))
          return
        }
        this.checkedItems = Object.fromEntries(this.storage.map(x => [x.id, true]))
      }
    },
    indeterminate(){
      return this.storage.some(storage => this.checkedItems[storage.id]) && this.storage.some(storage => !this.checkedItems[storage.id])
    },
    qrCodeData(){
      return this.storage.filter(storage => this.checkedItems[storage.id])
    }
  },
  props:{
    modelValue: {
      type: Boolean,
      default: false
    },
    storage: {
      type: Array<ApiStorage>,
      default: []
    }
  },
  data(){
    return{
      select: false,
      checkedItems: {} as {[key: number]: boolean},
      printScreen: false
    }
  },
  methods:{
    closePrintScreen(){
      this.visible=false
      Object.assign(this.$data, this.$options.data.apply(this))
    },
    showPrintScreen(){
      if(this.storage.some(storage => this.checkedItems[storage.id])){
        this.printScreen = true
        return
      }
      this.$notify({
        title: this.$t('toasts.error.title.print_no_selection'),
        text: this.$t('toasts.error.text.print_no_selection'),
        type: "error"
      })


    }
  }
})
</script>

<template>
<v-dialog
    transition="dialog-bottom-transition"
    :persistent="true"
    v-model="visible"
    :no-click-animation="true"
>

  <v-row
    justify="center"
    :no-gutters="true"
  >
    <v-col
      cols="12"
      lg="6"
    >
      <v-card

      >
        <v-card-title>
          <v-row
              justify="space-between"
          >
            <v-col v-if="printScreen">
              {{ $t('print.qr_code') }}
            </v-col>
            <v-col v-else>
              {{ $t('print.select_storage') }}
            </v-col>
            <v-col
                cols="1"
                class="d-flex align-center justify-end"
            >
              <app-icon-btn
                  size="large"
                  icon="mdi-close"
                  @click="closePrintScreen()"
              />
            </v-col>
          </v-row>
        </v-card-title>
        <template v-if="!printScreen">
          <v-card-text
              class="select"
          >
            <v-virtual-scroll
                :items="storage"
            >
              <template v-slot:default="{item}">
                <v-list-item
                    :title="item.name"
                >
                  <template v-slot:prepend>
                      <v-checkbox-btn
                          density="comfortable"
                          color="primary"
                          v-model="checkedItems[item.id]"

                      ></v-checkbox-btn>

                  </template>
                </v-list-item>
              </template>
            </v-virtual-scroll>
          </v-card-text>
          <v-card-actions
              class="d-flex justify-space-between"
          >
            <v-checkbox
                :label="!allSelected ? $t('print.select_all') : $t('print.deselect_all')"
                :hide-details="true"
                v-model="allSelected"
                :indeterminate="indeterminate"
                color="primary"
            />

            <v-btn
                prepend-icon="mdi-printer"
                @click="showPrintScreen()"
                variant="elevated"
                color="primary"
            >
              {{ $t('print.select_ok')}}
            </v-btn>
          </v-card-actions>
        </template>
        <app-print-qr-code
            class="me-2"
            v-model="printScreen"
            :storage="qrCodeData"
        />
      </v-card>
    </v-col>
  </v-row>
</v-dialog>
</template>

<style scoped lang="scss">
.select{
  max-height: 70svh;
  overflow: auto;
}
</style>