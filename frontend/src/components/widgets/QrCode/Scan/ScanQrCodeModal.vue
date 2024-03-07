<script lang="ts">
import {defineComponent} from 'vue'
import {StorageQrData, StorageTypes} from "@/types";
import {Html5QrcodeResult} from "html5-qrcode";
import {getName} from "@/api/storage";
import useNewAxios from "@/composables/useNewAxios.ts";
import {BoxEndpoint, LocationEndpoint} from "@/api/http";

export default defineComponent({
  name: "ScanQrCodeModal",
  setup(){
    const locationEndpoint = useNewAxios("location")
    const boxEndpoint = useNewAxios("box")
    return {
      locationEndpoint: locationEndpoint.axios as LocationEndpoint,
      boxEndpoint: boxEndpoint.axios as BoxEndpoint
    }
  },
  emits:{
    'update:model-value'(value: boolean){
      return true;
    }
  },
  computed: {
    visible: {
      get(){
        return this.modelValue
      },
      set(value: boolean){
        this.$emit('update:model-value', value)
      }
    },
    type() {
      switch(this.scanned?.storage_type)
      {
        case StorageTypes.Box:
          return "boxes"
        case StorageTypes.Location:
          return "locations"
        default:
          return ""
      }
    }
  },
  data(){
    return {
      scanned: undefined as undefined | StorageQrData,
      scanSuccess: false,
    }
  },
  props: {
    modelValue: {
      type: Boolean
    }
  },
  methods:{
    async scannedData(data: Html5QrcodeResult)
    {
      let scanned = JSON.parse(data.decodedText) as StorageQrData
      if(scanned.id !== this.scanned?.id || scanned.household_id !== this.scanned.household_id ||
        scanned.storage_type !== this.scanned.storage_type)
      {
        // ONLY FETCH NAME AND UPDATE DATA IF IT DIFFERS
        let name = ""
        switch(scanned.storage_type)
        {
          case StorageTypes.Location:
              name = await this.locationEndpoint.getLocationName(scanned.id)
              break
          case StorageTypes.Box:
              name = name = await this.boxEndpoint.getBoxName(scanned.id)
              break
          default:
            return
        }

        if(name === ""){
          return
        }
        scanned.name = name
        this.scanned = scanned
        this.scanSuccess = true
      }
    },
    goToStorage(){
      this.visible=false
      this.$router.push(`/storage/${this.type}/${this.scanned?.id}/${this.$t('scan.from')}`)
    },
    close(){
      Object.assign(this.$data, this.$options.data.apply(this))
      this.visible=false

    }
  }
})
</script>

<template>
<v-dialog
  v-model="visible"
  :persistent="true"
  :no-click-animation="true"
>
  <v-row
    justify="center"
  >
    <v-col
      cols="12"
      lg="6"
    >
      <v-card>
        <v-card-title>
          <v-row
              :no-gutters="true"
          >
            <v-col>
              {{ $t('scan.qr_code.title')}}
            </v-col>
            <v-col
                class="d-flex justify-end align-center"
            >
              <app-icon-btn
                  icon="mdi-close"
                  size="large"
                  @click="close()"
              />
            </v-col>
          </v-row>
        </v-card-title>
        <v-card-text
        >
          <app-qr-code-scanner
              v-model="visible"
              @scan-result="scannedData($event)"
          />
          <v-row
            justify="center"
          >
            <v-col
              cols="6"
              lg="4"
            >
              <v-sheet
                  class="d-flex justify-center mt-16 pt-4 pb-4"
                  v-if="scanSuccess"
                  color="green-lighten-2"
                  elevation="5"
              >
                <v-row :no-gutters="true">
                  <v-col class="ms-2">
                    {{ $t(`scan.scanned_type.${type}`) }}
                  </v-col>
                  <v-col
                      class="d-flex justify-center align-center"
                  >
                    {{ scanned?.name }}
                  </v-col>
                </v-row>
              </v-sheet>
            </v-col>
          </v-row>
        </v-card-text>
        <v-card-actions
            v-if="scanned !== undefined"
            class="d-flex justify-center"
        >
          <v-btn
              variant="elevated"
              color="primary"
              @click="goToStorage()"
          >
            {{ $t('scan.go_to.'+type)  }}

          </v-btn>
        </v-card-actions>
      </v-card>
    </v-col>
  </v-row>
</v-dialog>
</template>

<style scoped lang="scss">
.v-theme--dark{
  #qr-code-full-region{
    :deep(img) {
      filter: invert(100%) !important;
    }
  }
}
</style>