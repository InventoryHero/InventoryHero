<script setup lang="ts">

import {computed, ref} from "vue";

type CardTypes = "login"|"register"

const selected = ref<CardTypes>("login")
const forgotPassword = ref(false)
const isRegisterCard = computed(() => {
  return selected.value === "register"
})

function changeCard(to: CardTypes){
  selected.value = to
}

</script>

<template>
  <v-row
    justify="center"
    class="fill-height"
  >
    <v-col
      cols="12"
      lg="8"
    >
      <v-card
          elevation="5"
          min-height="40svh"
          height="fit-content"
          max-height="80svh"
          class="d-flex flex-column"
      >
        <v-card-title
          class="d-flex shadowed mb-3"
        >
            <template v-if="!forgotPassword">
              <v-btn
                  :color="isRegisterCard ? undefined : 'primary'"
                  variant="tonal"
                  rounded="xl"
                  :text="$t('login.login.title')"
                  class="me-5"
                  @click="changeCard('login')"
              />
              <v-spacer />
              <v-btn
                  @click="changeCard('register')"
                  :color="isRegisterCard ? 'primary' : undefined"
                  variant="tonal"
                  rounded="xl"
                  :text="$t('login.register.title')"
              />
            </template>
            <template v-else >
              {{ $t('password_reset.reset_password') }}
            </template>
        </v-card-title>

        <forgot-password-card
            v-if="forgotPassword"
            @close="forgotPassword=false"
        />
        <login-card
            v-else-if="selected==='login'"
            @reset-password="forgotPassword=true"
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



</style>