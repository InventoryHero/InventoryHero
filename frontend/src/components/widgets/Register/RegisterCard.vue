<script lang="ts">
import {useAuthStore} from "@/store";
import {defineComponent} from "vue";

export default defineComponent({
  name: "RegisterCard",
  setup(){
    const authStore = useAuthStore()
    return {authStore}
  },
  emits: {
    registered(){
      return true
    }
  },
  data() {
    return {
      loading: false,
      username: "",
      password: "",
      password_repeat: "",
      email: "",
      rules: {
        usernameNeeded: (value: string) => value !== '' || this.$t('login.register.username_needed'),
        passwordNeeded: (value: string) => value !== '' || this.$t('login.register.password_needed'),
        repeatNotEqual: (value: string) => value === this.password || this.$t('login.register.passwords_not_equal'),
        emailNeeded: (value: string) => value !== '' || this.$t('login.register.email_needed')
      }
    }
  },
  methods:{
    async register() {
      this.loading=true;
      let validation = await this.$refs["register-form"].validate();
      if(!validation.valid)
      {
        return
      }


      let success = await this.authStore.register(this.username, this.password, this.email, "")
      if (success) {
        this.password = "";
        this.password_repeat = "";
        this.username = "";
        this.email = "";
        this.loading=false
        this.$emit('registered')
      }
      else
      {
        this.loading = false
      }
    },
  }
})
</script>

<template>
  <v-card-text>
    <v-form
      @submit.prevent
      ref="register-form"
    >
      <v-text-field
          density="compact"
          variant="outlined"
          hide-details="auto"
          :label="$t('login.register.username')"
          type="text"
          v-model="username"
          :rules="[rules.usernameNeeded]"
      />
      <v-text-field
          density="compact"
          variant="outlined"
          hide-details="auto"
          :label="$t('login.register.email')"
          type="email"
          v-model="email"
          :rules="[rules.emailNeeded]"
      />
      <app-password-textfield
          v-model="password"
          :label="$t('login.register.password')"
          :rules="[rules.passwordNeeded]"
      />
      <app-password-textfield
          :label="$t('login.register.repeat_password')"
          v-model="password_repeat"
          :rules="[rules.repeatNotEqual]"
      />

    </v-form>
  </v-card-text>
  <v-card-actions class="justify-end">
    <v-btn
        :loading="loading"
        variant="elevated"
        color="green-lighten-1"
        @click="register()"
        prepend-icon="fa:fas fa-lock"
    >
      <template #prepend>
        <v-icon size="small"/>
      </template>
      {{ $t("login.register.btn") }}
    </v-btn>
  </v-card-actions>
</template>

<style scoped lang="scss">
.v-text-field{
  margin-bottom: 16px;
}
</style>