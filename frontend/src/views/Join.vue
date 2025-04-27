<script setup lang="ts">
import {defineComponent} from 'vue'
import useNewAxios from "@/composables/useAxiosOld.ts";
import {HouseholdEndpoint} from "@/api/http";
import {useAuthStore} from "@/store";
import {storeToRefs} from "pinia";
import {useNotification} from "@kyvg/vue3-notification";

const {household: householdEndpoint} = useAxios()
const authStore = useAuthStore()
const router = useRouter()
const {notify} = useNotification()
const {t} = useI18n()

const {
  code = ""
} = defineProps<{
  code?: string
}>()

const {returnUrl} = storeToRefs(authStore)

const accepting = ref(false)
const householdName = ref<string>('')
const inviterName = ref<string>('')
const inviteOk = ref(true)
const errorMessage = ref("")

const deny = () => {
  router.push('/')
}

const accept = () => {
  accepting.value = true
  householdEndpoint.acceptInvite(code).then(({success, data, error}) => {
    accepting.value = false
    if(!success){
      inviteOk.value = false
      errorMessage.value = (error as string|undefined) ?? 'other_error'
      return
    }
    returnUrl.value = ""
    router.push("/")
  })
}


onBeforeMount(() => {
  householdEndpoint.checkInviteValidity(code).then(({success, data, error}) => {
    if(!success){
      inviteOk.value = false
      errorMessage.value = (error as string|undefined) ?? 'other_error'
      return

    }

    householdName.value = data?.household_name ?? ''
    inviterName.value = data?.inviter_name ?? ''
    console.log(data)
  })
})

/*export default defineComponent({
  name: "Join",
  setup(){
    const {household: householdEndpoint} = useAxios()
    const authStore = useAuthStore();
    return {
      authStore,
      endpoint: householdEndpoint.axios as HouseholdEndpoint
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
      const {success, household} = await this.endpoint.joinHousehold(this.code)
      if(!success){
        // TODO
        return
      }
      this.authStore.addHousehold(household!)
      // reset return url otherwise user will be redirected to this join route again
      this.authStore.returnUrl = "";
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
})*/
</script>

<template>
<v-row
  justify="center"
>
  <v-col
    cols="12"
    lg="6"
  >
    <v-card
        v-if="inviteOk"
        :title="t('join.title', {owner: inviterName})"
    >
      <template v-slot:text>
        <p v-html="t('join.text', {
          name: householdName,
          owner: inviterName
        })" />
      </template>
      <v-card-actions
        class="justify-space-between"
      >
        <v-btn
          variant="tonal"
          color="red-lighten-2"
          @click="deny"
        >
          {{ t('join.deny')}}
        </v-btn>
        <v-btn
          variant="elevated"
          color="primary"
          @click="accept"
          :loading="accepting"
        >
          {{ t('join.accept')}}
        </v-btn>
      </v-card-actions>
    </v-card>

    <v-card
        v-else
        :title="t('join.invite_invalid')"
        :text="t(`join.${errorMessage}`)"
    >
      <v-card-actions>
        <v-btn
            variant="elevated"
            color="primary"
            @click="router.push('/')"
        >
          {{ t('home')}}
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