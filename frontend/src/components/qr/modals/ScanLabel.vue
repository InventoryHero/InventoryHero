
<script setup lang="ts">
import {QrcodeStream} from "vue-qrcode-reader";
import type {DetectedBarcode} from "barcode-detector/pure";
import {BoxResponseSchema, RoomResponseSchema} from "@/api/types/storage.ts";
import {RouteLocationRaw} from "vue-router";
import {useTheme} from "vuetify/framework";

interface Point {
  x: number;
  y: number;
}

const {storage} = useAxios();
const router = useRouter()
const theme = useTheme()
const {onBeforeRouteLeaveHandler} = useGlobalModal()

const {t} = useI18n()

const active = defineModel<boolean>()

const scannedId = ref<string|null|undefined>()
const scannedStorage = ref<BoxResponseSchema | RoomResponseSchema | null>(null)
const loadingCamera = ref(true)
const torchActive = ref(false)
const torchSupport = ref(false)
const selected = ref<MediaDeviceInfo | null>(null)
const devices = ref([] as MediaDeviceInfo[])
const loadingDevices = ref(true)

const torchIcon = computed(() => {
  if(torchActive.value){
    return 'mdi-flashlight-off'
  }
  return 'mdi-flashlight'
})

const scannedStorageChipText = computed(() => {
  if(!scannedStorage.value){
    return
  }
  let translationPath = ""
  switch(scannedStorage.value.storage_type){
    case "box":
      translationPath = "qr.scan.scanned_box"
      break
    case "room":
      translationPath = "qr.scan.scanned_room"
      break
  }
  return t(translationPath, {name: scannedStorage.value.name})
})



const getPointOnLine = (start: Point, end: Point, distance: number): Point => {
  const dx = end.x - start.x;
  const dy = end.y - start.y;
  const lineLength = Math.sqrt(dx * dx + dy * dy);
  if (lineLength === 0) return { ...start };
  const ratio = distance / lineLength;
  return { x: start.x + dx * ratio, y: start.y + dy * ratio };
};
const drawBracket = (ctx: CanvasRenderingContext2D, corner: Point, p1: Point, p2: Point, length: number, radius: number): void => {
  const line1End = getPointOnLine(corner, p1, length);
  const line2End = getPointOnLine(corner, p2, length);
  const arcStart = getPointOnLine(corner, p1, radius);
  const arcEnd = getPointOnLine(corner, p2, radius);

  ctx.beginPath();
  ctx.moveTo(line1End.x, line1End.y);
  ctx.lineTo(arcStart.x, arcStart.y);
  ctx.arcTo(corner.x, corner.y, arcEnd.x, arcEnd.y, radius);
  ctx.lineTo(line2End.x, line2End.y);
  ctx.stroke();
};
const paintOutline = (detectedCodes: DetectedBarcode[], ctx: CanvasRenderingContext2D): void => {
  for (const detectedCode of detectedCodes) {
    const originalCorners = detectedCode.cornerPoints;

    ctx.strokeStyle = theme.current.value.colors.primary || 'white';

    ctx.lineWidth = 5;
    ctx.lineJoin = 'round';
    ctx.lineCap = 'round';

    const bracketLength = 25;
    const offset = 10;
    const cornerRadius = 10;

    const centerX = (originalCorners[0].x + originalCorners[1].x + originalCorners[2].x + originalCorners[3].x) / 4;
    const centerY = (originalCorners[0].y + originalCorners[1].y + originalCorners[2].y + originalCorners[3].y) / 4;
    const center: Point = { x: centerX, y: centerY };

    const offsetCorners = originalCorners.map(corner => {
      const vectorX = corner.x - center.x;
      const vectorY = corner.y - center.y;
      const length = Math.sqrt(vectorX * vectorX + vectorY * vectorY);
      if (length === 0) return corner;

      return {
        x: corner.x + (vectorX / length) * offset,
        y: corner.y + (vectorY / length) * offset
      };
    });

    drawBracket(ctx, offsetCorners[0], offsetCorners[1], offsetCorners[3], bracketLength, cornerRadius);
    drawBracket(ctx, offsetCorners[1], offsetCorners[0], offsetCorners[2], bracketLength, cornerRadius);
    drawBracket(ctx, offsetCorners[2], offsetCorners[1], offsetCorners[3], bracketLength, cornerRadius);
    drawBracket(ctx, offsetCorners[3], offsetCorners[2], offsetCorners[0], bracketLength, cornerRadius);
  }
};


const onDetect = async (detectedCodes: Array<DetectedBarcode>) => {
  if(detectedCodes.length == 0){
    return
  }
  // TODO MAYBE SUPPORT MULTIPLE QR CODE SCANS AT ONCE
  const payload = detectedCodes[0].rawValue
  const parts = payload.split('/');
  const potentialId = parts.filter(part => part.length > 0).pop();
  if (!potentialId) {
    console.error("Could not find a final path segment in the URL:", payload);
    return null;
  }
  const uuidRegex = /^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$/;
  if (uuidRegex.test(potentialId)) {
    scannedId.value = potentialId;
    return
  }
  console.error("URL format not recognized:", payload);
}

const toggleTorch = () => {
  loadingCamera.value = true
  torchActive.value = !torchActive.value
}

const onCameraOn = (capabilites: any) => {
  loadingCamera.value = false
  torchSupport.value = capabilites.torch
}

const close = () => {
  active.value = false
}


const followQrCode = () => {
  if(!scannedStorage.value){
    return
  }
  let route = undefined as undefined | RouteLocationRaw;
  switch(scannedStorage.value!.storage_type){
    case "box":
      route = {
        name: "/storage/boxes/box.[id]",
        params: {
          id: scannedId.value!
        }
      }
      break
    case "room":
      route = {
        name: "/storage/rooms/room.[id]",
        params: {
          id: scannedId.value!
        }
      }
      break
  }
  active.value = false
  router.push(route)
}

watch(scannedId, async (newValue: string|null|undefined) => {
  if(!newValue){
    scannedStorage.value = null
    return
  }
  const {success, data, error} = await storage.getStorageDetail(newValue)
  if(!success){
    scannedStorage.value = null
    // TODO
    return
  }
  scannedStorage.value = data!

})
onBeforeRouteLeave(() => {
  return onBeforeRouteLeaveHandler()
})
onMounted(async () => {
  await navigator.mediaDevices.getUserMedia({video: true})
  devices.value = (await navigator.mediaDevices.enumerateDevices()).filter(
      ({ kind }) => kind === 'videoinput'
  )
  if(devices.value.length > 0){
    selected.value = devices.value[0]
  }
  loadingDevices.value = false
})

</script>

<template>

  <v-dialog
    v-model="active"
    persistent
    no-click-animation
  >
    <v-card
      :title="t('qr.scan.title')"
      density="compact"
    >
      <template v-slot:append>
        <v-icon-btn
            variant="plain"
            icon="mdi-close"
            @click="close()"
        />
      </template>

      <v-card-text
        class="pa-0"

      >
        <v-progress-linear
            :active="loadingCamera"
            :indeterminate="true"
            color="primary"
        />
        <qrcode-stream
            v-if="selected !== null"
            class="qr-stream"
            :constraints="{
              //@ts-expect-error docs do it the same way
              deviceId: selected.deviceId
            }"
            v-memo="[torchActive, selected.deviceId]"
            :torch="torchActive"
            @detect="onDetect"
            :track="paintOutline"
            @camera-on="onCameraOn"
            @error="console.error"
        >
          <v-overlay
              v-model="loadingCamera"
              contained
              class="d-flex flex-column justify-center align-center"
          >
            <!--TODO display errors here?-->
            {{t('qr.scan.loading_camera')}}
          </v-overlay>
          <v-card
              v-if="torchSupport"
              rounded="20"
              @click="toggleTorch"
              class="position-absolute"
              :style="{
                top: '12px',
                right: '12px'
              }"
          >
            <v-icon-btn
                :icon="torchIcon"
                color="primary"
                variant="plain"
                size="x-large"
                class="pa-1"
            />
          </v-card>
          <v-chip
              v-if="scannedStorage"
              class="position-absolute"
              :style="{
                bottom: '12px',
                left: '50%',
                transform: 'translateX(-50%)'
              }"
              @click="followQrCode"
              color="primary"
              variant="elevated"
              :text="scannedStorageChipText"
          />
        </qrcode-stream>
      </v-card-text>
      <v-card-actions>
        <v-select
            density="compact"
            variant="solo-filled"
            :loading="loadingDevices"
            :disabled="loadingDevices"
            v-model="selected"
            :items="devices"
            item-title="label"
            return-object
            :placeholder="t('qr.scan.camera')"
            @update:model-value="torchActive = false"
            hide-details
            color="primary"
        />
      </v-card-actions>
    </v-card>
  </v-dialog>

</template>

<style scoped lang="scss">

.switch-camera{
  position: absolute;
  width: fit-content;
  height: fit-content;
  right: 8px;
  top: 8px
}

.blurred-bg {
  background-color: rgba(255, 255, 255, 0.6); /* Semi-transparent white */
  backdrop-filter: blur(10px); /* Blurs the background */
  -webkit-backdrop-filter: blur(10px); /* For Safari */
}
</style>

