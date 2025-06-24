<script setup lang="ts">

const name = ref<string|undefined>(undefined)
</script>

<template>
  <v-card>
    <v-card-title>
      byebye
    </v-card-title>
    <v-card-text>
      <v-list>
        <v-list-item
            v-for="i in [1, 1]"
        >
          <v-text-field
            v-model="name"
          />
        </v-list-item>
      </v-list>
    </v-card-text>
    <v-card-actions>
      add
    </v-card-actions>
  </v-card>
</template>

<style scoped lang="scss">

</style>