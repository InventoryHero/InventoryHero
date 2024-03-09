<script lang="ts">
import {defineComponent} from 'vue'
import {UserEndpoint} from "@/api/http";
import useNewAxios from "@/composables/useNewAxios.ts";


export default defineComponent({
  name: "Confirmation",
  setup(){
    const {axios} = useNewAxios("user")
    return {
      userEndpoint: axios as UserEndpoint
    }
  },
  computed:{
    progressBarState(){
      return (this.countdown-this.time) * (100/this.countdown)
    }
  },
  props:{
    code: {
      type: String,
      required: true
    }
  },
  data(){
    return {
      verified: false,
      status: "",
      countdown: 5,
      time: 5
    }
  },
  methods:{
    updateProgress(seconds: number)
    {
      this.time = seconds
    }
  },
  async mounted() {
    const {verified, status} = await this.userEndpoint.confirmEmail(this.code)
    this.verified = verified
    this.status = status
  }
})
</script>

<template>
  <v-row
    justify="center"
    class="fill-height mt-4"
  >
    <v-col
      cols="12"
      lg="6"
    >
      <v-card
          v-if="verified"
      >
        <v-card-title>
          {{ $t('confirmation.email_confirmed')}}
        </v-card-title>
        <v-card-text
          class="mt-2 d-flex justify-center"
        >
          <v-progress-circular
              :model-value="progressBarState"
              :size="150"
              :width="8"
              color="primary"
          >
            <vue-countdown
                :time="countdown*1000" :interval="1000" :auto-start="true"
                v-slot="{seconds}"
                @progress="updateProgress($event.seconds)"
                @end="this.$router.push('/login')"
            >
              <span class="text-wrap">
                {{ $t('confirmation.redirect_in', {seconds: seconds}) }}
              </span>
            </vue-countdown>
          </v-progress-circular>

        </v-card-text>
        <v-card-actions
          class="justify-end"
        >
          <v-btn
            variant="outlined"
            color="primary"
            @click="this.$router.push('/login')"
          >
            {{ $t('confirmation.redirect_now') }}
          </v-btn>
        </v-card-actions>
      </v-card>
      <v-card v-else>
        <v-card-title>
          {{ $t('confirmation.failure') }}
        </v-card-title>
        <v-card-text>
          {{ $t(`confirmation.${status}`) }}
        </v-card-text>
        <v-card-actions
          class="justify-end">
          <v-btn
            variant="elevated"
            color="primary"
            @click="$router.push('/login')"
          >
            {{ $t('confirmation.go_to_login')}}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-col>
  </v-row>
</template>

<style scoped lang="scss">

</style>