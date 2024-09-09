<script setup lang="ts">
import {useAuthStore} from "@/store";

const authStore = useAuthStore()

onMounted(() => {
  authStore.logout()
})

</script>

<template>
    <v-row
        justify="center"
        class="fill-height align-content-center"
    >
      <v-col
          cols="8"
          lg="8"
          class="fill-height"
      >
        <div
            class="d-flex flex-column justify-center align-center pt-16"
        >
          <v-progress-circular
              width="10"
              size="140"
              indeterminate
              color="primary"
              class="mt-2"
          />
          <span class="mt-2">
            {{ $t('logging_out') }}
          </span>

        </div>
      </v-col>
    </v-row>

</template>

<style scoped lang="scss">

</style>