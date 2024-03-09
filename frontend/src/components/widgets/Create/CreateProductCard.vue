<script lang="ts">
import {defineComponent} from 'vue'
import {ProductLocations, ProductOnly, StorageTypes} from "@/types";
import {useAuthStore} from "@/store";
import useNewAxios from "@/composables/useNewAxios.ts";
import {ProductEndpoint} from "@/api/http";

type Views = "product" | "box" | "location"
type Clear = {
  [K in Views]: boolean
}

export default defineComponent({
  name: "CreateProductCard",
  setup(){
    const productEndpoint = useNewAxios("product")
    const user = useAuthStore();
    return {
      user,
      productEndpoint: productEndpoint.axios as ProductEndpoint
    }
  },
  computed:{
    comboboxHint() {
      return {
        active: this.hints.combobox !== '',
        hint: this.hints.combobox
      }
    },
    locationSelectHint(){
      return {
        active: this.hints.locationSelect !== '',
        hint: this.hints.locationSelect
      }
    },
    amountHint(){
      return {
        active: this.hints.amount !== '',
        hint: this.hints.amount
      }
    },
    starHint(){
      return {
        active: this.hints.star !== '',
        hint: this.hints.star

      }
    }
  },
  data(){
    return {
      postingProduct: false,
      productsLoading: false,
      products: [] as Array<ProductOnly>,
      product: null as (string | ProductOnly | null),
      location: null as (null|Storage),
      amount: null as (null|number),
      starred: false,
      hints: {
        locationSelect: '',
        combobox: '',
        amount: '',
        star: ''
      },
      rules: {
        isNumber: (value: any) => !isNaN(parseInt(value)) || this.$t('add.product.rules.amount_nan'),
        positive: (value: number) => value >= 0 || this.$t('add.product.rules.amount_negative'),
        needProduct: (value: any) => value !== null && value !== undefined && value !== '' || this.$t('add.product.rules.need_product')
      }
    }
  },
  methods: {
    enableHint(hint: keyof typeof this.hints)
    {
      this.$refs["add-form"].resetValidation();
      Object.keys(this.hints).forEach(v => this.hints[v as keyof typeof this.hints] = '')
      if(this.hints[hint] === '') {
        this.hints[hint] = this.$t(`add.product.hints.${hint}`)
      }
      else {
        this.hints[hint] = ''
      }
    },
    disableHint(hint: keyof typeof this.hints)
    {
      this.hints[hint] = ''
    },
    updateStarred(){
      if(typeof this.product === "string"){
        this.starred = false
        return
      }
      if(this.product === null)
      {
        this.starred = false
        return
      }
      this.starred = this.product.starred
    },
    clear(){
      this.$refs["add-form"].reset()
    },
    async save(){
      const validation = await this.$refs["add-form"].validate()

      if(!validation.valid){
        return
      }
      let data = {
        amount: this.amount!,
        starred: this.starred,
        storage_id: this.location?.id,
        storage_type: this.location?.type ?? 0
      } as Partial<ProductOnly & ProductLocations>

      let addToList = false
      if(typeof this.product === "string")
      {
        // case new product
        data.name = this.product
        addToList = true
      }
      else {
        data.id = this.product?.id
      }
      this.postingProduct = true
      const {success, product} = await this.productEndpoint.createProduct(data)
      this.postingProduct = false

      if(!success)
        return

      this.$refs["add-form"].reset()
      this.$notify({
        title: this.$t('toasts.titles.success.add_product', {
          name: data.name || this.product?.name,
          amount: data.amount
        }),
        text: this.$t('toasts.text.success.add_product'),
        type: "success"
      })

      if (addToList) {
        this.products.push(product!)
      }
    },
    getIcon(type: StorageTypes){
      switch(type){
        case StorageTypes.Location:
          return "fa:fas fa-building"
        case StorageTypes.Box:
          return "fa:fas fa-boxes"
        default:
          return ""
      }
    },

  },
  async mounted(){
    this.productsLoading=true
    this.products = await this.productEndpoint.getProducts({
      getStoredAt: false
    })
    this.productsLoading = false
  }
})
</script>

<template>
  <create-card
      :title="$t(`add.product.title`)"
      @save="save()"
      @clear="clear()"
      :loading="postingProduct"
  >
    <v-form
        @submit.prevent
        ref="add-form"
        :disabled="postingProduct"
    >

      <v-row
          :no-gutters="true"
          class="mb-2"
      >
        <v-col
            cols="12"
        >
          <v-combobox
              ref="combobox"
              :clearable="true"
              :persistent-clear="true"
              :hide-no-data="false"
              density="comfortable"
              auto-select-first="exact"
              v-model="product"
              :label="$t('add.product.labels.product')"
              :items="products"
              item-title="name"
              :persistent-hint="comboboxHint.active"
              :hint="comboboxHint.hint"
              :rules="[rules.needProduct]"
              @update:model-value="updateStarred()"
              :disabled="productsLoading"
              @keydown.enter="() => {
                $refs.combobox.blur()
              }"

          >
            <template #loader>
              <v-progress-linear
                  color="primary"
                  :indeterminate="true"
                  :active="productsLoading"
              />
            </template>
            <template #no-data>
              <v-list-item>
                <v-list-item-title
                    v-if="product !== null && product !== ''"
                >
                   {{ $t('add.product.new_product')}}
                    <p class="text-primary font-weight-bold d-inline">{{product}}</p>
                </v-list-item-title>
                <v-list-item-title
                  v-else
                >
                  {{ $t('add.product.start_typing')}}
                </v-list-item-title>

              </v-list-item>
            </template>
            <template #append>
              <app-help-indicator
                  @click:outside="disableHint('combobox')"
                  @click="enableHint('combobox')"
              />
            </template>
          </v-combobox>
        </v-col>
      </v-row>
      <v-row
          :no-gutters="true"
          class="mb-2"
      >
        <v-col
            cols="12"
        >
          <app-storage-select
            v-model="location"
            density="comfortable"
            :label="$t('add.product.labels.location')"
            :persistent-hint="locationSelectHint.active"
            :hint="locationSelectHint.hint"
            :hide-details="false"
            content-type="product"
          >
            <template #hint>
              <app-help-indicator
                  @click:outside="disableHint('locationSelect')"
                  @click="enableHint('locationSelect')"
              />
            </template>
          </app-storage-select>
        </v-col>
      </v-row>
      <v-row
          :no-gutters="true"
          class="mb-2 justify-space-between"
      >
        <v-col
            cols="7"
        >
          <v-text-field
              :hint="amountHint.hint"
              :persistent-hint="amountHint.active"
              type="number"
              density="comfortable"
              :label="$t('add.product.labels.amount')"
              v-model.number="amount"
              :rules="[rules.isNumber, rules.positive]"
              class="num-input"
          >
            <template #append>
              <app-help-indicator
                  @click:outside="disableHint('amount')"
                  @click="enableHint('amount')"
              />
            </template>
          </v-text-field>
        </v-col>
        <v-col
            class="d-flex flex-column justify-center"
            cols="4"
        >
          <v-label
              class="floating"
              style="margin: 0 !important;padding: 0 !important;"
          >
            {{ $t('add.product.labels.star') }}
          </v-label>
          <v-switch
              class="starred-switch"
              density="compact"
              v-model="starred"
              color="primary"
              style="margin: 0 !important;padding: 0 !important;"
              :hide-details="true"
          >

            <template #append>
              <app-help-indicator
                  @click:outside="disableHint('star')"
                  @click="enableHint('star')"
              />
            </template>
          </v-switch>
          <p
              class="v-messages v-messages__message"
          >
            {{starHint.hint}}
          </p>
        </v-col>
      </v-row>

    </v-form>
  </create-card>



</template>

<style scoped lang="scss">
:deep(.v-selection-control-group ){
  justify-content: space-evenly;
}

.num-input {
  :deep(.v-field__field){
    input {
      text-align: right;
    }
    label{
      text-align: right;
    }
  }
}

.starred-switch {
  :deep(.v-selection-control) {
    min-height: 0 !important;
  }
}

.floating{
  text-align: left;
  font-size: 0.9em;
}


</style>