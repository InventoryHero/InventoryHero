<script lang="ts">

import {useAuthStore} from "@/store";
import {defineComponent} from "vue";
import AppPasswordTextfield from "@/components/ui/AppPasswordTextfield.vue";
import useAxios from "@/composables/useAxios.ts";
import {GeneralEndpoint} from "@/api/http";

export default defineComponent({
  name: "LoginCard",
  components: {AppPasswordTextfield},
  emits: {
    resetPassword(){
      return true
    }
  },
  setup(){
    const authStore = useAuthStore();
    const {axios} = useAxios("general")
    return {
      authStore,
      generalEndpoint: axios as GeneralEndpoint
    }
  },
  computed: {

  },
  data() {
    return {
      loading: false,
      username: "",
      password: '',
      rules: {
        usernameNeeded: (value: string) => value !== '' || this.$t('login.login.rules.username_needed'),
        passwordNeeded: (value: string) => value !== '' || this.$t('login.login.rules.password_needed')
      },
      smtpEnabled: false,

    }
  },
  methods:{

    async login(){
      let validation = await this.$refs["login-form"].validate()
      if(validation.valid)
      {
        this.loading=true;
        await this.authStore.login(this.username, this.password)
        this.loading = false;
      }
    },
    resetPassword(){
      this.$emit('resetPassword')
    }
  },
  beforeMount(){
    this.generalEndpoint.checkSmtp().then((enabled: boolean) => {
      this.smtpEnabled = enabled
    })
  }
})
</script>

<template>
  <v-card-text>
    <v-form
      ref="login-form"
      @submit.prevent
    >
      <v-text-field
          density="compact"
          variant="outlined"
          :label="$t('login.login.username')"
          :rules="[rules.usernameNeeded]"
          type="text"
          v-model="username"
          @keyup.enter="login"
      />
      <app-password-textfield
        density="compact"
        variant="outlined"
        :rules="[rules.passwordNeeded]"
        :label="$t('login.login.password')"
        v-model="password"
        :disable-min-length="true"
        @keyup.enter="login"
      />
    </v-form>
  </v-card-text>
  <v-divider/>
  <v-card-actions :class="{
      'justify-space-between': smtpEnabled,
      'justify-end': !smtpEnabled
    }"
  >
    <v-btn
        v-if="smtpEnabled"
        variant="text"
        class="justify-space-between"
        @click="resetPassword"
    >
      {{ $t("login.login.forgot_password_btn") }}
    </v-btn>
    <v-btn
        :loading="loading"
        prepend-icon="mdi-lock"
        variant="elevated"
        color="green-lighten-1"
        @click="login()"
    >

      {{ $t("login.login.btn") }}
    </v-btn>
  </v-card-actions>
</template>

<style scoped lang="scss">

</style>