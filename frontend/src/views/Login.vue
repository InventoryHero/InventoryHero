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
    class="mt-4 fill-height"
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
          v-if="!forgotPassword"
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
        <v-card-title
            v-else
            class="shadowed mb-4"
        >
          {{ $t('password_reset.reset_password') }}
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
:deep(.v-card-text){
  min-height: calc(100svh * 0.3);
  display: flex;
  flex-direction: column;
  justify-content: center;
}


</style>