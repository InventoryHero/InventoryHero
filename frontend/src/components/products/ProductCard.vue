<script lang="ts">
import {defineComponent} from 'vue'


export default defineComponent({
  name: "ProductCard",
  emits: {
    expand(){
      return true;
    },
  },
  computed:
  {
    date(){
      let date: string|number = this.creationDate
      if(date === "")
        date = -1
      return this.$d(new Date(date))
    }
  },
  props: {
    id: {
      type: Number,
      required: true
    },
    name: {
      type: String,
      required: true
    },
    totalAmount: {
      type: Number,
      default: 0
    },
    starred: {
      type: Boolean,
      default: false,
    },
    creationDate: {
      type: String,
      default: "",
    }
  },
  data(){
    return{
        hover: false,
        elementExpanded: false,
        overlayVisible: false
    }
  },
  methods: {
    toggleElement(){
      this.$emit('expand')
    }
  }
})
</script>

<template>

    <v-card
      class="product"
      elevation="0"
      @mouseover="hover=true"
      @mouseleave="hover=false"
      :class="{
          'hover': hover,
        }"
      @click="toggleElement()"
    >
      <v-card-title

        class="title"

      >
        <v-row
          :no-gutters="true"
          justify="center"
        >
          <v-col
            cols="12"
            class="text-truncate "
          >
            {{ name }}
          </v-col>
        </v-row>
      </v-card-title>
      <v-card-subtitle
          class="mb-1"
      >
        <v-row

            :no-gutters="true"
            justify="center"
        >
          <v-col
              cols="6"
          >
            {{ $t('products.product.created') }}
          </v-col>
          <v-col
              cols="6"
              class="d-flex justify-end"
          >
            {{ date }}
          </v-col>
        </v-row>
        <v-row

          :no-gutters="true"
          justify="center"
      >
        <v-col
            cols="6"
        >
          {{ $t('products.product.amount') }}
        </v-col>
        <v-col
            cols="6"
            class="d-flex justify-end"
        >
          {{ totalAmount }}
        </v-col>
      </v-row>
      </v-card-subtitle>
    </v-card>
    <slot name="divider" >
      <v-divider
        color="primary"
        class="border-opacity-75"
      />
    </slot>

</template>

<style scoped lang="scss">
  .product {
    &.hover {
      cursor: pointer !important;
    }

    .title {
        margin-bottom: 0 !important;
        padding-bottom: 0 !important;
    }



  }
</style>