<script lang="ts">
import {defineComponent} from 'vue'
import {UserEndpoint} from "@/api/http";
import useNewAxios from "@/composables/useNewAxios.ts";

// TODO VERIFICCATION FAILURE

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
    this.verified = await this.userEndpoint.confirmEmail(this.code)

  }
})
</script>

<template>
  <v-row
    justify="center"
    class="fill-height mt-4"
  >
    <v-col
      cols="8"
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
        something went wrong sorry
      </v-card>
    </v-col>
  </v-row>
</template>

<style scoped lang="scss">

</style>