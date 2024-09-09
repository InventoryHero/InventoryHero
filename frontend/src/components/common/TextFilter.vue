<script lang="ts">
import {defineComponent} from 'vue'


export default defineComponent({
  name: "TextFilter",
  emits: {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    'update:filter'(payload: string){
      return true;
    }
  },
  props: {
    placeHolderText: {
      type: String,
      default: 'Filter'
    },
    filter: {
      type: String,
      default: ""
    }
  },
  computed: {
    filterString: {
      get(){
        return this.filter
      }, set(value: string|null){
        this.$emit('update:filter', value ?? '')
      }
    }
  },
  methods: {

  }

})
</script>

<template>
  <v-card
    v-bind="$attrs"
  >
    <v-row
      :no-gutters="true"
      density="compact"
      justify="center"
    >
      <v-col
        class="d-flex justify-center"

      >
        <v-text-field
            color="secondary"
            ref="filter"
            :hide-details="true"
            density="compact"
            v-model="filterString"
            :placeholder="placeHolderText"
            :label="placeHolderText"
            :clearable="true"
            :persistent-clear="true"

        >

        </v-text-field>
      </v-col>
    </v-row>
  </v-card>
</template>

<style scoped lang="scss">

</style>