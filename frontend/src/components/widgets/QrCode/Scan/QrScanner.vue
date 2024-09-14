
<script setup lang="ts">
// TODO once this is resolved, remove
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
//@ts-nocheck see: https://github.com/gruhn/vue-qrcode-reader/issues/429

import {BoxEndpoint, LocationEndpoint} from "@/api/http";
import useAxios from "@/composables/useAxios.ts";

const {axios: boxEndpoint} = useAxios<BoxEndpoint>("box");
const {axios: locationEndpoint} = useAxios<LocationEndpoint>("location");
const emit = defineEmits<{
  (e: 'close'): void
}>()

const {t} = useI18n()

type ScannedStorage = {
  url: string,
  id: number,
  type: string,
  name?: string
}

function paintOutline(detectedCodes, ctx) {
  for (const detectedCode of detectedCodes) {
    const [firstPoint, ...otherPoints] = detectedCode.cornerPoints

    ctx.strokeStyle = 'red'

    ctx.beginPath()
    ctx.moveTo(firstPoint.x, firstPoint.y)
    for (const { x, y } of otherPoints) {
      ctx.lineTo(x, y)
    }
    ctx.lineTo(firstPoint.x, firstPoint.y)
    ctx.closePath()
    ctx.stroke()
  }
}

async function onDetect(detectedCodes) {
  paused.value = true
  parsingScans.value = true
  const baseUrlRegex = new RegExp(`^${window.location.origin}/storage/(locations|boxes)/(\\d+)$`);

  const scanned =  detectedCodes
      .filter((code) => {
        const fullUrl = code.rawValue as string
        return baseUrlRegex.test(fullUrl)
      })
      .map((code) => {
        const fullUrl = code.rawValue as string
        const relativeUrl = fullUrl.replace(window.location.origin, "")
        const parts = relativeUrl.split('/')
        return {
          url: relativeUrl,
          id: parts.pop() || -1,
          type: parts.pop() || ''
        }
      })


  scannedStorages.value = []
  for(let i = 0; i < scanned.length; i++){
    const scan = scanned[i]
    let result = {success: false};
    if(scan.type === "boxes"){
      result = await boxEndpoint.getBoxName(scan.id)
    } else if(scan.type === "locations"){
      result = await locationEndpoint.getLocationName(scan.id)
    }
    if(!result.success){
      continue
    }
    scannedStorages.value.push({
      ...scan,
      name: result.name
    })
  }
  parsingScans.value = false
}

function toggleTorch(){
  loadingCamera.value = true
  torchActive.value = !torchActive.value
}

function onCameraOn(capabilites){
  loadingCamera.value = false
  torchSupport.value = capabilites.torch

}

function close(){
  emit('close')
}

function onError(error){
  console.log(error)
}

const scannedStorages = ref<Array<string>>([])
const paused = ref(false)
const loadingCamera = ref(true)
const torchActive = ref(false)
const torchSupport = ref(false)
const parsingScans = ref(false)
const selected = ref<MediaDeviceInfo | undefined>(undefined)
const devices = ref([] as MediaDeviceInfo[])
const loadingDevices = ref(true)

const torchIcon = computed(() => {
  if(torchActive.value){
    return 'mdi-flashlight-off'
  }
  return 'mdi-flashlight'
})

onMounted(async () => {
  await navigator.mediaDevices.getUserMedia({video: true})
  devices.value = (await navigator.mediaDevices.enumerateDevices()).filter(
      ({ kind }) => kind === 'videoinput'
  )
  loadingDevices.value = false
})
</script>

<template>

<v-card
  height="100vh"
>
  <v-card-title
    class="flex-0-0 d-flex justify-space-between align-center"
  >
    {{ $t('scan.qr_code.title')}}
    <app-icon-btn
        icon="mdi-close"
        size="large"
        @click="close()"
    />
  </v-card-title>
  <v-card-subtitle
      class="flex-0-0 pa-0"
  >
    <v-select
        density="compact"
        :loading="loadingDevices"
        :disabled="loadingDevices"
        v-model="selected"
        :items="devices"
        item-title="label"
        return-object
        :placeholder="t('scan.select_camera')"
        @update:model-value="torchActive = false"
        hide-details
        color="primary"

    />
  </v-card-subtitle>
  <v-card-text
    class="flex-1-1 overflow-hidden"
  >
    <v-card
      class="qr-stream"
    >
      <qrcode-stream
          v-if="selected !== undefined"
          :constraints="{ deviceId: selected.deviceId }"
          v-memo="[torchActive, selected.deviceId]"
          :torch="torchActive"
          :paused="paused"
          @detect="onDetect"
          :track="paintOutline"
          @camera-on="onCameraOn"
          @error="onError"
      >
        <v-card
            v-if="torchSupport"
            class="d-flex justify-center align-center switch-camera"
            rounded="20"
            @click="toggleTorch"
        >
          <app-icon-btn
              :icon="torchIcon"
              color="primary"
              size="x-large"
              class="pa-1"
          />
        </v-card>
        <v-overlay
            contained
            :model-value="paused||loadingCamera"
            class="fill-height d-flex justify-center align-center"
        >
          <v-container>
            <v-card
                v-if="paused"
                class="pa-6"
                @click="paused=false"
            >
              {{t('scan.camera_paused')}}
            </v-card>
            <v-card
                :loading="loadingCamera"
                v-if="loadingCamera"
                class="pa-6"
            >
              <template v-slot:loader="{isActive}">
                <v-progress-linear
                    :active="isActive"
                    :indeterminate="isActive"
                    color="primary"
                />
              </template>
              {{t('scan.loading_camera')}}
            </v-card>
          </v-container>
        </v-overlay>
      </qrcode-stream>
    </v-card>


    <v-container
        class="overflow-auto storage-buttons"
    >
      <v-progress-linear
          :active="parsingScans"
          :indeterminate="true"
          color="primary"
      />
      <v-row
          :no-gutters="true"
          justify="space-evenly"
      >
        <v-col
            v-for="(storage, index) in scannedStorages"
            :key="index"
            class="pa-1"
        >
          <v-btn
              variant="elevated"
              color="primary"
              @click="emit('close')"
              :to="storage.url"
          >
            <p>
              {{t('scan.go_to', {name: storage.name})}}
            </p>
          </v-btn>
        </v-col>
      </v-row>
    </v-container>

  </v-card-text>
</v-card>


</template>

<style scoped lang="scss">
.qr-stream{
  height: 60%;
}

.storage-buttons{
  height: 40%;
}


.switch-camera{
  position: absolute;
  width: fit-content;
  height: fit-content;
  right: 8px;
  top: 8px
}
</style>