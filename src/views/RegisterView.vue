<template>
    <h1> Register </h1>
    <div id="loginPos">
      <input-text class="inputText" :place_holder="this.$t('login_view.username')" :is_pssw="false" @valueUpdated=updateUsername />
      <input-text class="inputText" :place_holder="this.$t('login_view.password')" :is_pssw="true" @valueUpdated=updatePassword />
      <register-button @click="register()"/>
    </div>
  <a id="posLogin" @click="this.$router.push('/')">{{ this.$t('login_view.login') }}</a>
    
  </template>
  
  <script>
  import InputText from '@/components/InputText.vue';
  import RegisterButton from '@/components/RegisterButton.vue';
  
  import { DB_SB_register } from '@/db/supabase';
  
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

  
#posLogin {
  position: absolute;
  bottom: 50px;
  transform: translateX(-50%);
  text-decoration: underline;
}
  </style>
  