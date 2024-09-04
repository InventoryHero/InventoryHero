<script lang="ts">
import {defineComponent, PropType, ref} from 'vue'
import {ProductLocations, Storage} from "@/types";
import useCompareStorage from "@/composables/useCompareStorage.ts";
import useStorageTitle from "@/composables/useStorageTitle.ts";

export default defineComponent({
  name: "ProductDetailOverlay",
  emits:{
    'update:modelValue'(payload: ProductLocations|undefined){
      return true;
    },
    redirectToStorage(payload: Storage|undefined, from: string)
    {
      return true
    },
    "product-mapping:update"(mapping: ProductLocations|undefined, update: Partial<ProductLocations>, callback: () => void){
      return true
    },
    "product-mapping:delete"(mappingId: number, productId: number, callback: () => void){
      return true
    },
  },
  computed:{
    visible:{
      get():boolean{
        return this.modelValue !== undefined
      },
      set(value: boolean){
        this.$emit('update:modelValue', undefined)
      }
    },
    mapping(){
      return this.modelValue
    },
    container:{
      get(): Storage|null{
        if(this.newContainer !== undefined){
          return this.newContainer
        }
        return this.mapping?.storage ?? null
      },
      set(value: Storage|null){
        this.newContainer = value
      }
    },
    containerTitle(){
      return useStorageTitle(ref(this.modelValue?.storage))
    },
    amount:{
      get(): number{
        if(this.newAmount !== undefined)
        {
          return this.newAmount
        }
        return this.mapping?.amount ?? 0
      },
      set(value: number){
        this.newAmount = value
      }
    }
  },
  props:{
    modelValue: {
      type: Object as PropType<ProductLocations>,
      default: undefined
    },
    productName:{
      type: String,
      default: "",
    },
    disableStorageTitle: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      requestInProgress: false,
      edit: false,
      newAmount: undefined as number|undefined,
      saving: false,
      deleting: false,
      newContainer: undefined as Storage|null|undefined,
      deleteClicked: false,
      saveClicked: false
    }
  },
  methods:{
    redirect(){
      this.$emit('redirectToStorage', this.mapping?.storage ?? undefined,  this.$t('product', {name: this.productName}))
    },
    adjustAmount(increment: number){
      this.amount += increment
      if(this.edit)
      {
        return
      }
      this.requestInProgress = true
      this.$emit('product-mapping:update', this.mapping , {
        amount: this.amount
      }, this.callback)
    },
    handleSave(event: string, callback: () => void){
      if(event !== "accept") {
        return false
      }
      // FIX THIS HERE SHOULD ONLY BE UPDATED VALUES POSTED!!
      let update = {} as Partial<ProductLocations>
      const {same} = useCompareStorage(ref(this.mapping?.storage), ref(this.container))
      if(this.newAmount !== undefined)
      {
        update.amount = this.newAmount
      }
      if(!same)
      {
        update.storage = this.newContainer
        update.storage_type = this.newContainer?.type ?? 0
      }
      this.saving=true
      this.$emit('product-mapping:update', this.mapping , update, () => {
        this.callback()
        callback()
        this.saving = false
      })
    },
    handleDelete(event: string, callback: () => void)
    {
      if(event !== "accept") {
        return false
      }

      this.deleting=true
      this.$emit('product-mapping:delete', this.mapping?.id ?? -1, this.mapping?.product_id ?? -1, () => {
        this.callback()
        callback()
        this.deleting = false
      })

    },
    async eventHandler(event: string, type: string, callback: () => void){
      switch(type)
      {
        case "delete":
          this.deleteClicked = false
          this.handleDelete(event, callback)
          break;
        case "save":
          this.saveClicked = false
          this.handleSave(event, callback)
          break
      }
    },
    callback(){
      this.requestInProgress = false
      this.newAmount = undefined
      this.newContainer = null
    },
    toggleEdit(event: boolean){
      if(!event)
      {
        this.newAmount = undefined
        this.newContainer = undefined
      }
      this.edit = event
    }
  }
})
</script>

<template>
  <detail-overlay
      v-model="visible"
      @toggle-edit="toggleEdit($event)"
      @deny="(event: 'save'|'delete', callback: () => void) => eventHandler('deny', event, callback)"
      @accept="(event: 'save'|'delete', callback: () => void) => eventHandler('accept', event, callback)"
      :loading="requestInProgress"
  >
    <template #title>
      <app-overlay-title
          v-model="productName"
      />
    </template>
    <template #subTitle>
      <app-storage-title
          :icon="containerTitle.icon"
          :title="containerTitle.name"
          color="primary"
          @click="redirect()"
          v-if="!edit"
          :disabled="disableStorageTitle"
      />
      <app-storage-select
          class="mt-1"
          content-type="product"
          v-model="container"
          v-else
      />

    </template>


    <template #default>
      <quick-actions
          :amount-only="true"
          @update-amount="adjustAmount($event)"
          :disabled="requestInProgress"
      >
        <template #amount>
          <v-text-field
              v-model.number="amount"
              density="compact"
              :disabled="!edit"
              :hide-details="true"
          >

          </v-text-field>
        </template>
      </quick-actions>
      <div
        class="notice"
      >
        {{ $t('notice.version001.expiration_date') }}
      </div>
    </template>


    <template v-slot:delete-confirm="del">
      <app-confirm-modal
          @deny="del.deny()"
          @accept="del.accept()"
          :dialog="del.active"
          :no-click-animation="true"
          :title="$tc('products.confirm.detail.delete.title', containerTitle.name !== '' ? 0 : 1, {storage: containerTitle.name})"
          :body="$t('products.confirm.detail.delete.body')"
      />
    </template>
    <template v-slot:save-confirm="save">
      <app-confirm-modal
          @deny="save.deny()"
          @accept="save.accept()"
          :dialog="save.active"
          :no-click-animation="true"
          :title="$t('products.confirm.detail.save.title')"
          :body="$t('products.confirm.detail.save.body')"
      />
    </template>
  </detail-overlay>
</template>

<style scoped lang="scss">
.notice{
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-content: center;
  height: 75%;
  width: 100%;
}
:deep(.v-field__input)
{
  text-align: center;
}
</style>