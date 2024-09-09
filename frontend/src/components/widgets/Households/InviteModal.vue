<script lang="ts">
import {defineComponent} from 'vue'
import {HouseholdEndpoint} from "@/api/http";
import {useAuthStore} from "@/store";
import useAxios from "@/composables/useAxios.ts";

export default defineComponent({
  name: "InviteModal",
  setup(){
    const {axios: endpoint} = useAxios<HouseholdEndpoint>("household")
    const userStore = useAuthStore()
    return {
      endpoint,
      userStore
    }
  },
  watch: {
    modelValue(){
      if(this.modelValue){
        this.loading=true;
        this.endpoint.createInviteCode(this.householdId).then((data) => {

          if(data.success)
          {
            this.code = data.code
          }
          this.loading = false
        })
      }
    }
  },
  emits:{
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    "update:modelValue"(_: boolean){
      return true;
    }
  },
  computed:{
    model:{
      get(): boolean{
        return this.modelValue
      },
      set(value: boolean){
        this.$emit("update:modelValue", value)
      }
    },
    invite(){
      return `${window.location.origin}/join/${this.code}`
    },
    householdName(){
      // TODO
      return this.userStore.household.name
    },
    webShareApiSupported(){
      return navigator.share
    },
    whatsAppShare(){
      return {
        text: this.invite,
      }
    },
    emailShare(){
      return {
        subject: this.$t('invite.email.subject', {household: this.householdName}),
        body: this.invite,
        mail: ""
      }
    }
  },
  props:{
    modelValue: {
      type: Boolean
    },
    householdId: {
      type: Number,
      default: NaN
    }
  },
  data(){
    return {
      code: "",
      copiedConfirm: false,
      loading: false,
    }
  },
  methods: {
    share(){
      // TODO NICE TEXT HERE
      navigator.share({
        title: 'HALLO',
        text: 'HALLO',
        url: this.invite
      })
    },
    copyToClipboard(){
      navigator.clipboard.writeText(this.invite);
      this.copiedConfirm = true;
      return
    }
  }
})
</script>

<template>
  <v-snackbar
    v-model="copiedConfirm"
    :timeout="2000"
    elevation="24"
    rounded="pill"
    color="success"
    :multi-line="false"
    @click="copiedConfirm=false"
  >
    {{ $t('toasts.titles.success.copied_to_clipboard')}}
  </v-snackbar>
<v-dialog
  v-model="model"
  :persistent="true"
  :no-click-animation="true"
>
  <v-row
      :no-gutters="true"
    justify="center"
  >
    <v-col
        cols="11"
        lg="4"
    >
      <v-card>
        <v-card-title
            class="d-flex justify-space-between align-center"
        >
          {{ $t('invite.title') }}
          <app-icon-btn icon="mdi-close" @click="model = false"/>
        </v-card-title>
        <v-card-text>
    <span>
      {{ $t('invite.copy_to_clipboard')}}
    </span>
          <v-textarea
              class="mt-2 mb-4 text-overflow align-center"
              :readonly="true"
              v-model="invite"
              :hide-details="true"
              density="compact"
              :auto-grow="true"
              rows="1"
              :loading="loading"
          >
            <template v-slot:append>
              <v-icon
                  :disabled="loading"
                  icon="fa:fas fa-clipboard"
                  @click="copyToClipboard()"
              />
            </template>
          </v-textarea>
          {{ $t('invite.or')}}
        </v-card-text>
        <v-card-actions
            v-if="webShareApiSupported"
            class="justify-end"
        >
          <v-btn
              icon="mdi-share-variant"
              variant="tonal"
              size="small"
              @click="share"
          >
            <v-icon size="large" color="primary" class="me-1"/>
          </v-btn>
        </v-card-actions>
        <v-card-actions
            v-else-if="!loading"
            class="justify-space-evenly"
        >
          <s-email
              :share-options="emailShare"

          >
            <v-btn
                icon="fa:fas fa-envelope"
            >
              <v-icon size="large" color="primary" class="me-1"/>
            </v-btn>
          </s-email>

          <s-whats-app
              :share-options="whatsAppShare"
          >
            <v-btn
                icon="fa:fab fa-whatsapp"
            >
              <v-icon size="large" color="primary" class="me-1"/>
            </v-btn>
          </s-whats-app>
        </v-card-actions>
      </v-card>
    </v-col>
  </v-row>
</v-dialog>
</template>

<style scoped lang="scss">
.text-overflow{
  word-break: break-all;
}
</style>