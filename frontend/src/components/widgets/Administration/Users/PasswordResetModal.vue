<script lang="ts">
import {defineComponent} from 'vue'
import {useDisplay} from "vuetify";
import useAxios from "@/composables/useAxios.ts";
import {AdministrationEndpoint} from "@/api/http";

export default defineComponent({
  name: "PasswordResetModal",
  setup(){
    const {mobile} = useDisplay()
    const {axios} = useAxios("administration")

    return {
      mobile,
      adminEndpoint: axios as AdministrationEndpoint
    }
  },
  emits:{
  },
  computed:{
    active: {
      get(){
        return this.modelValue !== undefined
      },
      set(value: boolean){
        if(!value)
        {
          this.$emit('update:modelValue', undefined)
        }
      }
    },
    fullscreen(){
      return this.mobile
    },
    textFieldStyle(){
      return {
        variant: "solo-filled",
        rounded: "lg",
        color: "primary",
        clearable: true,
        persistentClear: true,
        hideDetails: "auto",
        class: "mb-4",
        disabled: false
      } as Partial<{}>
    }
  },
  props: {
    modelValue: {
      type: Number,
      default: undefined,
    },
    userName: {
      type: String,
      default: ""
    },
  },
  data() {
    return {
      password: "" as string,
      passwordRepeat: "" as string,
      saving: false,
      rules: {
        required: (value: string) => value !== '' || this.$t('administration.users.password_reset.password_needed'),
        mismatch: (value: string) => this.password === value || this.$t('administration.users.password_reset.passwords_not_equal'),
      }
    }
  },
  methods: {
    async savePassword(){
      const {valid} = await (this.$refs.passwordForm as HTMLFormElement).validate()
      if(!valid){
        return
      }
      this.saving = true
      const {success} = await this.adminEndpoint.resetPassword(this.modelValue!, this.password)
      this.saving = false

      if(success) {
        this.$notify({
          title: this.$t('toasts.titles.success.password_reset'),
          text: this.$t('toasts.text.success.password_reset'),
          type: "success"
        })
      }
    },
    closeModal(){
      this.password = "";
      this.passwordRepeat = "";
      this.active = false;
    }
  }
})
</script>

<template>
  <v-dialog
      v-model="active"
      :persistent="true"
      :no-click-animation="true"
  >
    <v-expand-transition>
      <v-row
          :no-gutters="true"
          justify="center"
          class="fill-height"
          v-if="active"
      >
        <v-col
            lg="6"
            cols="12"
        >
          <v-card
              v-bind="$attrs"
              max-height="60vh"
              class="d-flex flex-column"
          >
            <template v-slot:loader>
              <v-progress-linear
                  color="primary"
                  indeterminate
                  :active="saving"
              />
            </template>
            <v-card-title
              class="d-flex justify-lg-space-between align-center"
            >
              {{ $t("administration.users.password_reset.title", {username: userName}) }}
              <v-btn
                  density="compact"
                  icon="mdi-close"
                  @click="closeModal"
              />
            </v-card-title>
            <v-card-text>
              <v-banner
                  class="my-4"
                  bg-color="accent"
                  :rounded="true"
              >
                <v-banner-text>
                  {{  $t("administration.users.password_reset.email_disabled") }}
                </v-banner-text>
              </v-banner>
              <v-form
                  ref="passwordForm"
              >
                <app-password-textfield
                    v-bind="textFieldStyle"
                    :label="$t('administration.users.password_reset.password')"
                    class="mb-4"
                    v-model="password"
                    :rules="[rules.required]"
                />

                <app-password-textfield
                    v-bind="textFieldStyle"
                    :label="$t('administration.users.password_reset.password_repeat')"
                    class="mb-4"
                    v-model="passwordRepeat"
                    :rules="[rules.mismatch]"
                />
              </v-form>
            </v-card-text>
            <v-card-actions
              class="justify-space-between"
            >
              <v-btn
                  prepend-icon="mdi-cancel"
                  :text="$t('administration.users.password_reset.cancel')"
                  @click="closeModal"
                  :disabled="saving"
              />
              <v-btn
                  prepend-icon="mdi-content-save"
                  :text="$t('administration.users.password_reset.save')"
                  @click="savePassword"
                  :disabled="saving"
              />
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-expand-transition>
  </v-dialog>
</template>

<style scoped lang="scss">

</style>