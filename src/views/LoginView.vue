<template>
      <div class="loginCard">
        <div class="modal-toolbar">
          <v-toolbar
                  class="justify-space-evenly vuetify-toolbar-override"
                  :title="this.$t('login_view.login')"
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
                  :text="this.$t('login_view.register')"
                  class="posRegister"
                  @click="redirectToRegister"
          />
          <v-btn
                  icon="fa:fas fa-long-arrow-alt-right"
                  class="loginButton"
                  @click="login"
          />



        </v-card-actions >

      </div>



</template>

<script>
import InputText from '@/components/InputText.vue';
import LoginButton from '@/components/LoginButton.vue';
import RegisterButton from '@/components/RegisterButton.vue';
import InputTextEnhanced from "@/components/InputTextEnhanced.vue";

import { DB_SB_login } from '@/db/supabase';

import {getSettings, getUser, setUser} from '@/db/dexie';
import {useToast} from "vue-toastification";
export default {
  name: 'App',
  setup(){
    const toast = useToast();
    return {toast};
  },
  components: {
    InputText,
    LoginButton,
    RegisterButton,
    InputTextEnhanced
  },
  data() {
    return {
      password: "",
      username: "",
      settings: Object
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
    redirectToRegister() {
      this.$router.push("/register");
    },
    login() {
      DB_SB_login(this.username, this.password).then((login_succeeded) => {
        if (login_succeeded) {
          setUser(this.username).then((res) => {
            if(res) {
              this.$router.push("/home")
            }
            else {
              console.log("[ERR] dexie cant set user")
            }
          })
        } else {
          this.toast.error(this.$t("login_view.login_invalid"));
        }
      });
    
    }
  },
  beforeMount() {
      getSettings().then((settings) => {
        this.settings = settings;
        console.log(this.settings);
        this.$i18n.locale = this.settings.language;
      })
      getUser().then((user) => {
          if(user !== undefined)
          {
              this.$router.push("/home");
          }
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
    padding-top: 1px;
    padding-bottom: 1px;
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
    margin-top: 50vh;
    transform: translateY(-50%);

}

.loginCardFooter {
  position: relative;
  width: 90%;
  margin-left: 5%;
}
</style>
