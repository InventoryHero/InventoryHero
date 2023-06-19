<template>
  <div class="viewContainer" :class="this.theme">
    <h1 class="loginTitle"> Register </h1>
    <div id="loginPos">
      <input-text class="inputUsername" :place_holder="this.$t('login_view.username')" :is_pssw="false" @valueUpdated=updateUsername />
      <input-text class="inputPassword" :place_holder="this.$t('login_view.password')" :is_pssw="true" @valueUpdated=updatePassword />
     
    </div>
    <div class="buttonContainer">
      <register-button @click="register()"/>
       </div>

  <div class ="loginContainer"> <a id="posLogin" @click="this.$router.push('/')">{{ this.$t('login_view.login') }}</a> </div>
 
  </div>
  </template>
  
  <script>
  import InputText from '@/components/InputText.vue';
  import RegisterButton from '@/components/RegisterButton.vue';
  
  import { DB_SB_register } from '@/db/supabase';
  import { global_theme } from "@/db/dexie"
  
  export default {
    name: 'App',
    components: {
      InputText,
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
      updateUsername(username) {
        this.username = username;
      },
      updatePassword(password) {
        this.password = password;
      },
      register() {
        DB_SB_register(this.username, this.password).then((register_succeeded) => {
          if (register_succeeded) {
            this.$router.push("/");
          } else {
            console.log("something went wrong ops");
          }
        });
      
      }
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
  
  .buttonContainer {
  position: relative;
  margin-top: 10%;
}

.loginContainer {
  position: relative;
  margin-top: 10%;
}

.inputPassword {
  margin-bottom: 10%;
}

.inputUsername {
  margin-bottom: 10%;
}

.loginTitle {
  margin-top: 10%;
  text-align: center;
  color: rgb(243, 243, 243);
  font-size: 50px;
  position: relative;
  top: 10%;
}


  
#posLogin {
  position: absolute;

  transform: translateX(-50%);
  text-decoration: underline;
}
  </style>
  