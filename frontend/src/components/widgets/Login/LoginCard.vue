<script lang="ts">

import {useAuthStore} from "@/store";
import {defineComponent} from "vue";
import AppPasswordTextfield from "@/components/ui/AppPasswordTextfield.vue";
import useAxios from "@/composables/useAxios.ts";
import {GeneralEndpoint} from "@/api/http";

export default defineComponent({
  name: "LoginCard",
  components: {AppPasswordTextfield},
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
        usernameNeeded: (value: string) => value !== '' || this.$t('login.login.username_needed'),
        passwordNeeded: (value: string) => value !== '' || this.$t('login.login.password_needed')
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
      />
      <app-password-textfield
        density="compact"
        variant="outlined"
        :rules="[rules.passwordNeeded]"
        :label="$t('login.login.password')"
        v-model="password"
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
    >
      {{ $t("login.login.forgot_password_btn") }}
    </v-btn>
    <v-btn
        :loading="loading"
        prepend-icon="fa:fas fa-lock"
        variant="elevated"
        color="green-lighten-1"
        @click="login()"
    >
      <template #prepend>
        <v-icon size="small"/>
      </template>
      {{ $t("login.login.btn") }}
    </v-btn>
  </v-card-actions>
</template>

<style scoped lang="scss">

</style>