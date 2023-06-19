<template>
    <div class="viewContainer" :class="this.theme">
      <h1 class="loginTitle"> Login </h1>
      <div id="loginPos">
        <input-text class="inputUsername" :place_holder="this.$t('login_view.username')" :is_pssw="false" @valueUpdated=updateUsername />
        <input-text class="inputPassword" :place_holder="this.$t('login_view.password')" :is_pssw="true" @valueUpdated=updatePassword />
   
        <button class="settingsButton" @click="redirectToSettings"> <v-icon>fa:fas fa-cog</v-icon> </button>
      </div>
      <div class="buttonContainer">
      <login-button class="loginButton" @click=login() />
        <register-button class="posRegister" @click="redirectToRegister">{{ this.$t('login_view.register') }}</register-button>
      </div>
      
    </div>
</template>

<script>
import InputText from '@/components/InputText.vue';
import LoginButton from '@/components/LoginButton.vue';
import RegisterButton from '@/components/RegisterButton.vue';

import { DB_SB_login } from '@/db/supabase';

import {getUser, setUser} from '@/db/dexie';
import { global_theme } from "@/db/dexie"
export default {
  name: 'App',
  components: {
    InputText,
    LoginButton,
    RegisterButton
  },
  data() {
    return {
      password: "",
      username: "",
      theme: global_theme
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
          console.log("[ERR] wrong username or password")
        }
      });
    
    }
  },
  beforeMount() {
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


.inputUsername {
  margin-bottom: 10%;
}

.buttonContainer {
  position: relative;
  margin-top: 10%;
}

.inputPassword {
  margin-bottom: 10%;
}

.loginButton {
  position: absolute;

  right: 25%;

}

#loginPos {
  margin-top: 30%;
}

.posRegister {
  position: absolute;
  right: 45%;
  transform: translateX(-50%);


}

.loginTitle {
  margin-top: 10%;
  text-align: center;
  color: rgb(243, 243, 243);
  font-size: 50px;
  position: relative;
  top: 10%;
}

.settingsButton {
  position: absolute;
  top: 20px;
  right: 20px;
  background-color: transparent;
  border: none;
  cursor: pointer;
  font-size: 24px;
}
</style>
