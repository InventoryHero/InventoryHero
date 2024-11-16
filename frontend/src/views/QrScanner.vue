
<script setup lang="ts">
// TODO once this is resolved, remove
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
//@ts-nocheck see: https://github.com/gruhn/vue-qrcode-reader/issues/429

import {BoxEndpoint, LocationEndpoint} from "@/api/http";
import useAxios from "@/composables/useAxios.ts";
import {useScroll} from "@vueuse/core";
import {useTemplateRef} from "vue";

const {axios: boxEndpoint} = useAxios<BoxEndpoint>("box");
const {axios: locationEndpoint} = useAxios<LocationEndpoint>("location");
const router = useRouter()

const {t} = useI18n()


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
  if(paused.value){
    // on mobile paused doesn't seem to work ...
    return
  }
  paused.value = true
  parsingScans.value = true
  const baseUrlRegex = new RegExp(`^${window.location.origin}/(boxes/box|locations/location)/(\\d+)$`)


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
    if(scan.type === "box"){
      result = await boxEndpoint.getBoxName(scan.id)
    } else if(scan.type === "location"){
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
  router.back()
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

const scroller = useTemplateRef("scroller")
const { y } = useScroll(scroller, {behavior: 'smooth'})

const scrolled = computed(() => y.value > 0)

function scrollToTop(){
  y.value = 0;
}


</script>

<template>

<v-row
    :no-gutters="true"
    justify="center"
    class="fill-height fill-width"
>
  <v-col
      cols="12"
      md="10"
      lg="8"
  >
    <v-card
      class="fill-height  d-flex flex-column "
      density="compact"
    >
      <template v-slot:loader>
        <v-progress-linear
            :active="parsingScans"
            :indeterminate="true"
            color="primary"
        />
      </template>
      <v-card-title
          class="d-flex align-center"
      >
        {{ $t('scan.title')}}
        <v-spacer />
        <app-icon-btn
            icon="mdi-close"
            size="large"
            @click="close()"
        />
      </v-card-title>
      <v-card-subtitle
          class="pa-0 mb-2"
      >
        <v-select
            density="compact"
            variant="solo-filled"
            :loading="loadingDevices"
            :disabled="loadingDevices"
            v-model="selected"
            :items="devices"
            item-title="label"
            return-object
            :placeholder="t('scan.camera')"
            @update:model-value="torchActive = false"
            hide-details
            color="primary"
        />
      </v-card-subtitle>

      <v-container
        fluid
        class="flex-1-1 position-relative "
      >
        <v-card-text
          class="wrapper "
        >
          <div ref="scroller" class="scroll overflow-scroll">
            <v-container
            >
              <qrcode-stream
                  class="qr-stream"
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
                <v-container
                    class="fill-height fill-width d-flex justify-center align-center"
                    :class="{
          'blurred-bg': paused || loadingCamera
        }"
                >
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
              </qrcode-stream>
              <v-card
                  variant="elevated"
                  color="primary"
                  v-else
                  :text="t('scan.select_camera')"
              />
            </v-container>
            <v-row
                dense
                justify="space-evenly"
            >
              <v-col
                  v-for="(storage, index) in scannedStorages"
                  :key="index"
                  class="d-flex justify-center"
              >
                <v-btn
                    variant="elevated"
                    color="primary"
                    :to="storage.url"
                >
                  <p>
                    {{t('scan.go_to', {name: storage.name})}}
                  </p>
                </v-btn>
              </v-col>
            </v-row>
          </div>
        </v-card-text>
      </v-container>
    </v-card>

  </v-col>


</v-row>
  <app-scroll-to-top-btn
      :scrolled-down="scrolled"
      @click.stop="scrollToTop"
  />

</template>

<style scoped lang="scss">
.qr-stream{
  height: 60%;
}




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