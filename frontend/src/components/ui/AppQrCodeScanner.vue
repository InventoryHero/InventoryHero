<script lang="ts">
import {defineComponent} from 'vue'
import {Html5QrcodeCameraScanConfig, Html5QrcodeResult, Html5QrcodeScanner} from "html5-qrcode";

export default defineComponent({
  name: "AppQrCodeScanner",
  emits:{
    scanResult(result: Html5QrcodeResult){
      return true;
    }
  },
  watch:{
    modelValue(){
      if(!this.modelValue){
        this.html5QrcodeScanner.clear()
      }
    }
  },
  props: {
    qrbox: {
      type: Number,
      default: 250
    },
    fps: {
      type: Number,
      default: 10
    },
    modelValue: {
      type: Boolean
    }
  },
  data(){
    return {
      html5QrCodeScanner: undefined as undefined | Html5QrcodeScanner
    }
  },
  mounted () {
    const config = {
      fps: this.fps,
      qrbox: this.qrbox,
    } as Html5QrcodeCameraScanConfig
    this.html5QrcodeScanner = new Html5QrcodeScanner('qr-code-full-region', config, false);
    this.html5QrcodeScanner.render(this.onScanSuccess, undefined);
  },
  methods: {
    onScanSuccess (decodedText, decodedResult) {
      this.$emit('scanResult', decodedResult);
      //this.html5QrcodeScanner?.clear();
    },


  }
})
</script>

<template>
  <div id="qr-code-full-region"></div>
</template>

<style scoped lang="scss">
#qr-code-full-region{
  border: none !important;
}

</style>

