<template>
    <h1> Login </h1>
    <div id="loginPos">
      <input-text class="inputText" place_holder="Username" :is_pssw="false" @valueUpdated=updateUsername />
      <input-text class="inputText" place_holder="Password" :is_pssw="true" @valueUpdated=updatePassword />
      <login-button class="loginButton" @click=login() />
    </div>
  </template>
  
  <script>
  import InputText from '@/components/InputText.vue';
  import LoginButton from '@/components/LoginButton.vue';
  
  import { DB_SB_login } from '@/db/supabase';
  
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
            this.$router.push("/home")
          } else {
            console.log("wrong username or password")
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
  </style>
  