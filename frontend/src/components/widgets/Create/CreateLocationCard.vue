<script lang="ts">
import {defineComponent} from 'vue'
import {useAuthStore} from "@/store";
import useNewAxios from "@/composables/useNewAxios.ts";
import {LocationEndpoint} from "@/api/http";


export default defineComponent({
  name: "CreateLocationCard",
  setup(){
    const {axios} = useNewAxios("location")
    const user = useAuthStore();
    return {axios: axios as LocationEndpoint, user}
  },
  computed: {
    locationNameHint(){
      return{
        active: this.hints.locationName !== '',
        hint: this.hints.locationName
      }
    },
  },
  data(){
    return {
      postingLocation: false,
      location: "",
      hints: {
        locationName: ''
      },
      rules: {
        needName: (value: string) => value !== "" || this.$t('add.location.rules.name_needed')
      }
    }
  },
  methods: {
    enableHint(hint: keyof typeof this.hints)
    {
      this.$refs["add-form"].resetValidation();
      Object.keys(this.hints).forEach(v => this.hints[v as keyof typeof this.hints] = '')
      if(this.hints[hint] === '') {
        this.hints[hint] = this.$t(`add.location.hints.${hint}`)
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
        this.$emit('save:handled')
        return
      }

      let formData = new FormData();
      formData.append("household", this.user.household)
      formData.append("name", this.location)

      this.$emit('save:handled')
      this.$emit('posting')
      this.postingLocation = true
      const {success, newLocation} = await this.axios.createLocation({
        name: this.location
      })

      this.postingLocation = false
      if(success){
        this.$refs["add-form"].reset()
        this.$emit('posted')
        this.$notify({
          title: 'SUCCESS',
          title: 'ADDED'
        })
      }

    },
    clear(){
      this.$refs["add-form"].reset()
    }

  }
})
</script>

<template>

  <create-card
      :title="$t(`add.location.title`)"
      @save="save()"
      @clear="clear()"
      :loading="postingLocation"
  >
    <v-form
        @submit.prevent
        ref="add-form"
        :disabled="postingLocation"
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
              v-model="location"
              :label="$t('add.location.labels.location')"
              item-title="name"
              :persistent-hint="locationNameHint.active"
              :hint="locationNameHint.hint"
              :rules="[rules.needName]"
          >
            <template #append>
              <app-help-indicator
                  @click:outside="disableHint('locationName')"
                  @click="enableHint('locationName')"
              />
            </template>
          </v-text-field>
        </v-col>
      </v-row>
    </v-form>
  </create-card>

</template>

<style scoped lang="scss">

</style>