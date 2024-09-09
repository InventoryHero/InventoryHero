<script lang="ts">
import {defineComponent} from 'vue'
import {useAuthStore} from "@/store";

export default defineComponent({
  name: "HouseholdItem",
  emits: {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    toggleEdit(id: number){
      return true
    },

    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    toggleInvite(id: number){
      return true
    },
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    leaveHousehold(id: number){
      return true
    },
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    setDefaultHousehold(id: number){
      return true
    }
  },
  setup(){
    const authStore = useAuthStore();
    return {authStore}
  },
  props: {
    title: {
      type: String,
      default: ""
    },
    id: {
      type: Number,
      default: -1
    },
    rCols: {
      type: Number,
      default: 6
    },
    titleClass: {
      type: String,
      default: ""
    },
    actions: {
      type: Boolean,
      default: true
    },
    isJoined: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    cols(){
      return [12-this.rCols, this.rCols]
    }
  },
  methods: {
    isNotDefaultHousehold()
    {
      return this.authStore.user.household?.id !== this.id
    },
  }
})
</script>

<template>
  <v-container>
    <v-row
        :no-gutters="true"
    >
      <v-col
          :cols="cols[0]"
          :class="titleClass"
      >
        <slot name="title">
          {{ title }}
        </slot>
      </v-col>
      <v-col
          :cols="cols[1]"
          class="d-flex justify-end align-center"
          v-if="actions"
      >
        <template
          v-if="!isJoined"
          >
           <app-icon-btn
               icon="fa:fas fa-edit"
               size="medium"
               class="me-4"
               @click="$emit('toggleEdit', id)"
           />
           <app-icon-btn
               icon="fa:fas fa-user-plus"
               size="medium"
               class="me-4"
               @click="$emit('toggleInvite', id)"
           />
        </template>
        <app-icon-btn
            v-else
            icon="fa:fas fa-right-from-bracket"
            size="medium"
            class="me-4"
            @click="$emit('leaveHousehold', id)"
        />
        <app-icon-btn
            :icon="isNotDefaultHousehold() ? 'fa:far fa-square' : 'fa:far fa-check-square'"
            size="medium"
            @click="$emit('setDefaultHousehold', id)"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped lang="scss">

</style>