<script setup lang="ts">
import App from "@/App.vue";

const {t} = useI18n()

</script>

<template>
  <v-app>
    <Suspense>
      <template v-slot:default>
        <App />
      </template>
      <template v-slot:fallback>
        <v-container
            fluid
            class="fill-height"
        >
          <v-row
            justify="center"
          >
            <v-col
                cols="12"
                md="10"
                lg="8"
                class="pb-16"
            >
              <v-card
                  class="fill-width"
              >
                <template v-slot:loader>
                  <v-progress-linear
                      indeterminate
                      active
                      color="primary"
                  />
                </template>
                <template v-slot:text>
                  <span
                    class="d-flex justify-center"
                  >
                    {{t('app.loading_content')}}
                  </span>
                </template>
              </v-card>
            </v-col>
          </v-row>
        </v-container>
      </template>
    </Suspense>
  </v-app>
</template>

<style scoped lang="scss">

</style>