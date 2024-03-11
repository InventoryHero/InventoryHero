<script lang="ts">
import {defineComponent} from 'vue'
import {HouseholdEndpoint} from "@/api/http";
import useNewAxios from "@/composables/useNewAxios.ts";

export default defineComponent({
  name: "InviteModal",
  setup(){
    const householdEndpoint = useNewAxios("household")
    return {
      endpoint: householdEndpoint.axios as HouseholdEndpoint
    }
  },
  watch: {
    modelValue(){
      if(this.modelValue){
        this.endpoint.createInviteCode(this.householdId).then((data) => {
          if(data.success)
          {
            this.code = data.code
            return
          }

        })
      }
    }
  },
  emits:{
    "update:modelValue"(newValue: boolean){
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
        subject: this.$t('invite.email.subject'),
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
    }
  },
  methods: {
    share(){
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
      this.$notify({
        title: this.$t('toasts.titles.success.copied_to_clipboard'),
        text: this.$t('toasts.text.success.copied_to_clipboard'),
        type: "success"
      })
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
          >
            <template v-slot:append>
              <v-icon
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
            v-else
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