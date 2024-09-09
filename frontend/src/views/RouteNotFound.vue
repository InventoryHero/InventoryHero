<script setup lang="ts">

const {t} = useI18n()
const router = useRouter()

</script>

<template>
  <v-row
      justify="center"
      class="fill-height"
  >
    <v-col
        cols="12"
        md="6"
        lg="6"
    >
      <v-card>
        <v-empty-state
            class="pa-0"
            image="https://vuetifyjs.b-cdn.net/docs/images/components/v-empty-state/astro-cat.svg"
            size="200"
        >
          <template v-slot:media>
            <v-sheet class="py-4 mb-4" color="#fdefff">
              <v-img></v-img>
            </v-sheet>
          </template>

          <template v-slot:text>
            <div class="text-body-2 font-weight-medium text-medium-emphasis">
              {{t('not_found')}}
            </div>
          </template>

          <template v-slot:actions>
            <v-spacer></v-spacer>

            <v-btn
                color="primary"
                :text="t('back_to_home')"
                @click="router.push('/')"
            />

            <v-spacer></v-spacer>
          </template>
        </v-empty-state>
      </v-card>
    </v-col>
  </v-row>
</template>

<style scoped lang="scss">

</style>