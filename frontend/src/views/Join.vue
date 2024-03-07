<script lang="ts">
import {defineComponent} from 'vue'
import useNewAxios from "@/composables/useNewAxios.ts";
import {HouseholdEndpoint} from "@/api/http";

export default defineComponent({
  name: "Join",
  setup(){
    const householdEndpoint = useNewAxios("household")
    return {
      endpoint: householdEndpoint.axios as HouseholdEndpoint
    }
  },
  props: {
    code: {
      type: String,
      default: ""
    }
  },
  data(){
    return {
      household_meta: {
        name: "",
        owner: ""
      },
      accepting: false
    }
  },
  methods:{
    deny(){
      this.$router.replace("/")
    },
    async accept(){
      this.accepting = true
      const success = await this.endpoint.joinHousehold(this.code)
      if(!success){
        // TODO
        return
      }
      this.$router.push("/households")

    }
  },
  async mounted(){
    const {success, owner, name} = await this.endpoint.getHouseholdMeta(this.code)
    if(!success){
      this.$router.push("/")
      return
    }
    this.household_meta = {
      owner: owner,
      name: name
    }
  }
})
</script>

<template>
<v-row>
  <v-col
    cols="12"
    lg="6"
  >
    <v-card>
      <v-card-title
        class="text-wrap"
      >
        {{ $t('join.title', {owner: this.household_meta.owner}) }}
      </v-card-title>
      <v-card-text
        v-html="$t('join.text', this.household_meta)"
      >

      </v-card-text>
      <v-card-actions
        class="justify-space-between"
      >
        <v-btn
          variant="tonal"
          color="red-lighten-2"
          @click="deny"
        >
          {{ $t('join.deny')}}
        </v-btn>
        <v-btn
          variant="elevated"
          color="primary"
          @click="accept"
          :loading="accepting"
        >
          {{ $t('join.accept')}}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-col>
</v-row>
</template>

<style scoped lang="scss">
:deep(b){
  color: rgba(var(--v-theme-primary), 1);
}
</style>