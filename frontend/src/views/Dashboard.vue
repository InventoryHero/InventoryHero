<script setup lang="ts">
import {useModal} from "@/composables-new/useModal.ts";

const {openModal} = useModal()
const test = ref(true)
</script>

<template>
 <v-row
     dense
     class="fill-width"
     justify="center"
 >
   <v-col
       cols="12"
       md="10"
       lg="8"
   >
     <household-quick-select-card
         :collapsible="true"
         class="fill-width"
     />
   </v-col>
 </v-row>

</template>

<style scoped lang="scss">

</style>
