<script lang="ts">
import {defineComponent} from 'vue'
import AppIconBtn from "@/components/ui/AppIconBtn.vue";

export default defineComponent({
  name: "TextFilter",
  emits: {
    updateFilter(payload: string){
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
  data(){
    return {
      needle: this.filter
    }
  },
  methods: {
    updateFilter(clear: boolean = false)
    {
      if(clear)
      {
        this.needle = ""
      }
      this.$emit('updateFilter', this.needle)
    }
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
            v-model="needle"
            :placeholder="placeHolderText"
            :label="placeHolderText"
            :clearable="true"
            :persistent-clear="true"
            @update:model-value="updateFilter()"
            @click:clear="updateFilter(true)"
        >

        </v-text-field>
      </v-col>
    </v-row>
  </v-card>
</template>

<style scoped lang="scss">

</style>