<template>
  <h1> Login </h1>
  <div id="loginPos">
    <input-text class="inputText" place_holder="Username" :is_pssw="false" @valueUpdated=updateUsername />
    <input-text class="inputText" place_holder="Password" :is_pssw="true" @valueUpdated=updatePassword />
    <login-button class="loginButton" @click=login() />
  </div>

  <a id="posRegister" @click="this.$router.push('/register')">Register</a>

</template>

<script>
import InputText from '@/components/InputText.vue';
import LoginButton from '@/components/LoginButton.vue';

import { DB_SB_login } from '@/db/supabase';

import {getUser, setUser} from '@/db/dexie';

export default {
  name: 'App',
  components: {
    InputText,
    LoginButton
  },
  data() {
    return {
      password: "",
      username: "",
    }
  },
  methods: {
    updateUsername(username) {
      this.username = username;
    },
    updatePassword(password) {
      this.password = password;
    },
    login() {
      DB_SB_login(this.username, this.password).then((login_succeeded) => {
        if (login_succeeded) {
          setUser(this.username, this.password).then((res) => {
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

<style>
.inputText {
  margin-bottom: 10px;
}

.loginButton {
  margin-left: 48vw;
}

#loginPos {
  margin-top: 30%;
}

#posRegister {
  position: absolute;
  bottom: 50px;
  transform: translateX(-50%);
  text-decoration: underline;
}
</style>
