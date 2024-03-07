<script lang="ts">

import {defineComponent} from "vue";

type CardTypes = "login"|"register"

export default defineComponent({
  name: "Login",
  data() {
    return {
      selected: "login" as CardTypes
    }
  },
  computed:{
    isRegisterCard(): boolean{
      return this.selected === "register"
    },
  },
  methods:{
    changeCard(to: CardTypes){
      this.selected = to
    },
  }
})
</script>

<template>
  <v-row
    justify="center"
    class="mt-4"
  >
    <v-col
      cols="12"
      lg="8"
    >
      <v-card
          elevation="5"
      >
        <v-card-title
          class="d-flex justify-space-between shadowed mb-3"
        >
            <v-btn
                :color="isRegisterCard ? undefined : 'primary'"
                variant="outlined"
                rounded="xl"
                :text="$t('login.login.title')"
                class="me-5"
                @click="changeCard('login')"
            />

            <v-btn
                @click="changeCard('register')"
                :color="isRegisterCard ? 'primary' : undefined"
                variant="outlined"
                rounded="xl"
                :text="$t('login.register.title')"
            />
        </v-card-title>
        <login-card
            v-if="selected==='login'"
        />
        <register-card
            v-else
            @registered="changeCard('login')"
        />
      </v-card>
    </v-col>
  </v-row>
</template>

<style scoped lang="scss">
:deep(.v-card-text){
  min-height: calc(100svh * 0.3);
  display: flex;
  flex-direction: column;
  justify-content: center;
}
</style>