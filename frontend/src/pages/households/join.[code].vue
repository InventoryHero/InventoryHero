<script setup lang="ts">
import useAuthStore from "@/store/useAuthStore";
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
    router.push("/")
  })
}


onBeforeMount(() => {
  console.log(code)
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

  <v-card
      v-if="inviteOk"
      :title="t('households.join.title', {owner: inviterName})"
  >
    <template v-slot:text>
      <i18n-t keypath="households.join.text">
        <template #name>
          <span class="text-primary">{{householdName}}</span>
        </template>
        <template #owner>
          <span class="text-primary">{{inviterName}}</span>
        </template>
      </i18n-t>
    </template>
    <v-card-actions
        class="d-flex flex-wrap justify-end"
    >
      <v-btn
        variant="tonal"
        color="red-lighten-2"
        @click="deny"
      >
        {{ t('households.join.deny')}}
      </v-btn>
      <v-btn
        variant="elevated"
        color="primary"
        @click="accept"
        :loading="accepting"
      >
        {{ t('households.join.accept')}}
      </v-btn>
    </v-card-actions>
  </v-card>

  <v-card
      v-else
      :title="t('households.join.invite_invalid')"
      :text="t(`households.join.${errorMessage}`)"
  >
    <v-card-actions>
      <v-spacer/>
      <v-btn
          variant="elevated"
          color="primary"
          @click="router.push('/')"
      >
        {{ t('home')}}
      </v-btn>
    </v-card-actions>
  </v-card>


</template>

<style scoped lang="scss">
:deep(b){
  color: rgba(var(--v-theme-primary), 1);
}
</style>

<route>
{
  "props": true,
  "meta": {
    "requiresAuth": true,
    "requiresHousehold": false,
    "title": 'titles.join_household'
  }
}
</route>