<script lang="ts">
import {defineComponent} from 'vue'
import useNewAxios from "@/composables/useAxios.ts";
import {UserEndpoint} from "@/api/http";

export default defineComponent({
  name: "PasswordReset",
  setup(){
    const {axios} = useNewAxios("user")
    return {
      userEndpoint: axios as UserEndpoint
    }
  },
  props: {
    id: {
      type: String,
      required: true
    }
  },
  data(){
    return {
      allowed: false,
      preflightCheck: true,
      password: "",
      password_repeat: "",
      rules: {
        passwordNeeded: (value: string) => value !== '' || this.$t('password_reset.password_needed'),
        repeatNotEqual: (value: string) => value === this.password || this.$t('password_reset.passwords_not_equal'),
      }
    }
  },
  beforeMount(){
    this.userEndpoint.resetPasswordPreflight(this.id).then((allowed) => {
      this.allowed = allowed
      this.preflightCheck = false;
    })
  }
})
</script>

<template>
  <v-row
      justify="center"
      class="fill-height mt-4"
  >
    <v-col
        cols="12"
        lg="6"
    >

      <v-card>
        <v-card-title
            class="shadowed mb-3"
        >
          {{ $t('password_reset.card.title') }}
        </v-card-title>
        <v-card-text

        >
          <app-progress-circular
              v-if="preflightCheck"
              :indeterminate="true"
              color="primary"
              :width="10"
              :message="$t('password_reset.loading_preflight')"
          />
          <template v-else>
            <v-form
                ref="login-form"
                @submit.prevent
                class="fill-width"
            >
              <app-password-textfield
                  v-model="password"
                  :label="$t('password_reset.password')"
                  :rules="[rules.passwordNeeded]"
                  density="compact"
                  variant="outlined"
                  class="mb-2"
              />
              <app-password-textfield
                  :label="$t('password_reset.repeat_password')"
                  v-model="password_repeat"
                  :rules="[rules.repeatNotEqual]"
                  density="compact"
                  variant="outlined"
              />
            </v-form>
          </template>
        </v-card-text>
        <v-card-action
          class="d-flex justify-space-between"

        >
          <v-btn>
            back
          </v-btn>
          <v-btn
              v-if="!preflightCheck"
          >
            save
          </v-btn>
        </v-card-action>
      </v-card>
    </v-col>
  </v-row>

</template>

<style scoped lang="scss">
:deep(.v-card-text){
  min-height: calc(100svh * 0.3);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-content: center;
  align-items: center;
}

</style>