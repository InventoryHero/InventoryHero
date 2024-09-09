<script lang="ts">

import {useAuthStore, useStorage} from "@/store";
import {BoxEndpoint} from "@/api/http";
import useAxios from "@/composables/useAxios.ts";
import {ApiStorage} from "@/types";

export default defineComponent({
  name: "CreateBoxCard",
  inject: ['loading'],
  setup(){
    const {axios} = useAxios<BoxEndpoint>("box")
    const storageStore = useStorage()
    const user = useAuthStore();
    return {
      axios,
      user,
      storageStore
    }
  },
  data(){
    return {
      postingBox: false,
      box: "",
      boxes: [] as Array<ApiStorage>,
      location: undefined as undefined|ApiStorage,
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
        storageId: this.location?.id ?? undefined
      })

      this.postingBox = false

      if(success){

        this.storageStore.addBox(newBox)
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
})
</script>

<template>
  <create-card
        :title="$t(`add.box.title`)"
        @save="save()"
        @clear="clear()"
        :request-in-progress="postingBox"
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
                :storage-loading="loading?.loadingLocations ?? false"
                v-model="location"
                :storage="storageStore.locations"
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