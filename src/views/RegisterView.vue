<template>
  <div class="loginCard">
    <div class="modal-toolbar">
      <v-toolbar
              class="justify-space-evenly vuetify-toolbar-override"
              :title="this.$t('login_view.register')"
      >
        <v-icon @click="redirectToSettings" class="me-5" icon="fa:fas fa-cog"></v-icon>
      </v-toolbar>
    </div>
    <div id="loginContainer">
      <input-text-enhanced
              :place_holder="this.$t('login_view.username')"
              @valueUpdated=updateUsername
      />
      <input-text-enhanced
              :place_holder="this.$t('login_view.password')"
              @valueUpdated=updatePassword
              input_type="password"
      />

    </div>
    <v-card-actions  class="loginCardFooter justify-space-evenly">
      <v-btn
              :text="this.$t('login_view.login')"
              class="loginButton"
              @click="this.$router.push('/')"
      />
      <v-btn
              :text="this.$t('login_view.register')"
              class="posRegister"
              @click="register"
      />




    </v-card-actions >

  </div>


  </template>
  
  <script>
  import InputText from '@/components/InputText.vue';
  import RegisterButton from '@/components/RegisterButton.vue';
  
  import { DB_SB_register } from '@/db/supabase';
  import {getSettings} from "@/db/dexie";
  import InputTextEnhanced from "@/components/InputTextEnhanced.vue";
  import {useToast} from "vue-toastification";
  
  export default {
    name: 'App',
    setup(){
      const toast = useToast();
      return {toast};
    },
    components: {
      InputTextEnhanced,
      InputText,
      RegisterButton
    },
    data() {
      return {
        password: "",
        username: "",
        theme: ""
      }
    },
    methods: {
      redirectToSettings() {
        this.$router.push("/settings");
      },
      updateUsername(username) {
        this.username = username;
      },
      updatePassword(password) {
        this.password = password;
      },
      register() {
        DB_SB_register(this.username, this.password).then((register_succeeded) => {
          if (register_succeeded === "") {
            this.toast.success(this.$t("login_view.toasts.success.register"))
            this.$router.push("/");
          } else {
            if(register_succeeded === "username_taken")
            {
              this.toast.error(this.$t("login_view.toasts.error.register.username_taken"));
            }
            else if(register_succeeded === "generic_err")
            {
              this.toast.error(this.$t("login_view.toasts.error.register.generic_error"));
            }
          }
        });

      
      }
    }, beforeMount() {
      getSettings().then((settings) => {
        this.theme =  settings.theme;
      })
    }
  }
  </script>

<style scoped>



.loginButton {
    border: rgba(255,255,255,0.5) solid 1px;
    background-color: rgba(0,0,0,0.4);
    background: var(--color-dark-theme-lighter);
    border-radius: 5px;
    height: fit-content;
    padding-top: 5px;
    padding-bottom: 5px;
}

#loginContainer {
    margin-top: 30px;
    width: 90%;
    margin-left: 5%;

}

.posRegister  {
    border: rgba(255,255,255,0.5) solid 1px;
    background-color: rgba(0,0,0,0.4);
    background: var(--color-dark-theme-lighter);
    border-radius: 5px;
    height: fit-content;
    padding-top: 5px;
    padding-bottom: 5px;
}

.loginCard {
    position: relative;
    background-color: rgba(0,0,0,0.5) !important;
    backdrop-filter: blur(15px) !important;
    border-radius: 10px !important;
    border: white solid 1px !important;
    width: 90%;
    margin-left: 5%;
    margin-top: 30vh;
    height: 40vh;
}

.loginCardFooter {
    position: relative;
    width: 90%;
    margin-left: 5%;
}
</style>