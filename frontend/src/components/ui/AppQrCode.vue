<script setup lang="ts">
import { ref } from 'vue'
import { useQRCode } from '@vueuse/integrations/useQRCode'

const {
  iconWidth=30
} = defineProps<{
  iconWidth?: number
}>()

const iconWidthInPx = computed(() => {
  return `${iconWidth}px`
})

const options = ref<{
  errorCorrectionLevel?: string,
  margin?: number,
  width?: number,
  scale?: number
}>({
  errorCorrectionLevel: "H",
  margin: 1,
  //width: 150,
  scale: 5
})


const text = ref('text-to-encode')
const qrcode = useQRCode(text, options.value)
</script>

<template>
<div class="qr-code-wrapper">
  <img :src="qrcode" alt="QR Code" class="qr-code" />
  <!-- Use the favicon in the center of the QR code -->
  <img src="/favicon.ico" alt="Favicon" class="center-image" />
</div>

</template>

<style scoped lang="scss">
.qr-code-wrapper {
  position: relative;
  display: inline-block;
}

.qr-code {
  display: block;
  width: 100%;
  height: auto;
}

.center-image {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: v-bind(iconWidthInPx); /* Adjust size as needed */
  height: v-bind(iconWidthInP); /* Adjust size as needed */
  border-radius: 50%; /* Optional: If you want a circular image */
}
</style>