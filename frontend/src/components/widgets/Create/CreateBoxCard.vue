<script lang="ts">
import {defineComponent} from 'vue'
import {isMobile} from "mobile-device-detect";
import {Box, Location} from "@/types";
import {useAuthStore} from "@/store";
import useNewAxios from "@/composables/useAxios.ts";
import {BoxEndpoint, LocationEndpoint} from "@/api/http";

type Views = "product" | "box" | "location"
type Clear = {
  [K in Views]: boolean
}

export default defineComponent({
  name: "CreateBoxCard",
  components: {},
  setup(){
    const {axios} = useNewAxios("box")
    const locationEndpoint = useNewAxios("location")
    const user = useAuthStore();
    return {
      axios: axios as BoxEndpoint,
      locationEndpoint: locationEndpoint.axios as LocationEndpoint,
      user
    }
  },
  data(){
    return {
      postingBox: false,
      locationsLoading: false,
      box: "",
      boxes: [] as Array<Box>,
      location: null as null|Location,
      locations: [] as Array<Location>,
      hints: {
        boxName: '',
        locationSelect: ''
      },
      rules: {
        needName: (value: string) => value !== "" || this.$t('add.box.rules.name_needed')
      },
    }
  },
  computed:{
    boxNameHint(){
      return{
        active: this.hints.boxName !== '',
        hint: this.hints.boxName
      }
    },
    locationSelectHint(){
      return{
        active: this.hints.locationSelect !== '',
        hint: this.hints.locationSelect
      }
    }
  },
  methods: {
    isMobile() {
      return isMobile
    },
    clear(){
      this.$refs["add-form"].reset()
    },
    enableHint(hint: keyof typeof this.hints)
    {
      this.$refs["add-form"].resetValidation();
      Object.keys(this.hints).forEach(v => this.hints[v as keyof typeof this.hints] = '')
      if(this.hints[hint] === '') {
        this.hints[hint] = this.$t(`add.box.hints.${hint}`)
      }
      else {
        this.hints[hint] = ''
      }
    },
    disableHint(hint: keyof typeof this.hints)
    {
      this.hints[hint] = ''
    },
    async save(){
      const validation = await this.$refs["add-form"].validate()

      if(!validation.valid){
        return
      }

      this.postingBox = true
      const {success, newBox} = await this.axios.createBox({
        name: this.box,
        location_id: this.location?.id ?? undefined
      })
      this.postingBox = false

      if(success){


        this.$notify({
          title: this.$t('toasts.titles.success.add_box', {
            name: this.box
          }),
          text: this.$t('toasts.text.success.add_box'),
          type: "success"
        })
        this.$refs["add-form"].reset()
      }

    }
  },
  async beforeMount(){
    this.locationsLoading = true
    this.locations = await this.locationEndpoint.getLocations({
      contained: false
    });
    this.locationsLoading = false
  }
})
</script>

<template>
  <create-card
      :title="$t(`add.box.title`)"
      @save="save()"
      @clear="clear()"
      :loading="postingBox"
  >
    <v-form
        @submit.prevent
        ref="add-form"
        :disabled="postingBox"
    >

      <v-row
          :no-gutters="true"
          class="mb-2"
      >
        <v-col
            cols="12"
        >
          <v-text-field
              :clearable="true"
              :persistent-clear="true"
              density="comfortable"
              auto-select-first="exact"
              v-model="box"
              :label="$t('add.box.labels.box')"
              item-title="name"
              :persistent-hint="boxNameHint.active"
              :hint="boxNameHint.hint"
              :rules="[rules.needName]"
          >
            <template #append>
              <app-help-indicator
                  @click:outside="disableHint('boxName')"
                  @click="enableHint('boxName')"
              />
            </template>
          </v-text-field>
        </v-col>
      </v-row>
      <v-row
          :no-gutters="true"
          class="mb-2"
      >
        <v-col
            cols="12"
        >
          <app-storage-select
              v-model="location"
              :storage="locations"
              density="comfortable"
              :label="$t('add.box.labels.location')"
              :persistent-hint="locationSelectHint.active"
              :hint="locationSelectHint.hint"
              :hide-details="false"
              content-type="box"
          >
            <template #hint>
              <app-help-indicator
                  @click:outside="disableHint('locationSelect')"
                  @click="enableHint('locationSelect')"
              />
            </template>
          </app-storage-select>


        </v-col>
      </v-row>
    </v-form>
  </create-card>
</template>

<style scoped lang="scss">
</style>