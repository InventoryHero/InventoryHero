<script lang="ts">
import {defineComponent, PropType, ref} from 'vue'
import {type Box, ProductLocations, ProductOnly, Location} from "@/types";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import AppStorageSelect from "@/components/ui/AppStorageSelect.vue";
import AppPrintQrCode from "@/components/widgets/QrCode/Print/AppPrintQrCode.vue";
import useStorageTitle from "@/composables/useStorageTitle.ts";
import useNewAxios from "@/composables/useAxios.ts";
import {BoxEndpoint, ProductEndpoint} from "@/api/http";

export default defineComponent({
  name: "BoxOverlay",
  components: {AppPrintQrCode, AppStorageSelect, FontAwesomeIcon},
  setup() {

    const {axios} = useNewAxios('box')
    const productEndpoint = useNewAxios('product')
    return {
      axios: axios as BoxEndpoint,
      productEndpoint: productEndpoint.axios as ProductEndpoint
    }
  },
  emits:{
    deleted(){
      return true;
    },
    deleteProduct(id: number, callback: () => void){
      return true
    },
    contentChanged(currentBox: number, newBox: number|undefined){
      return true
    },
    updated(box: Box){
      return true;
    },
    'update:modelValue'(value: Box|undefined){
      return true;
    }
  },
  watch: {
    box(newVal){
      if(newVal !== undefined)
      {
        this.loadProducts()
      }
    }
  },
  computed:{
    boxProducts() {
      return this.products ?? []
    },
    boxContainer:{
      get(): Location|null{
        if(this.container !== undefined){
          return this.container
        }
        return this.box?.location ?? null
      },
      set(value: Location|null){
        this.container = value
      }
    },
    storageTitle(){
      return useStorageTitle(ref(this.box?.location))
    },
    box(){
      return this.modelValue
    },
    visible:{
      get(): boolean{
        return this.modelValue !== undefined && this.modelValue !== null
      },
      set(value: boolean){
        this.$emit('update:modelValue', undefined)
        this.reset()

      }
    },
    name: {
      get(): string{
        if(this.newName !== undefined)
          return this.newName
        return this.box?.name ?? ''
      },
      set(value: string)
      {
        this.newName = value
      }
    },
    productName(){
      return this.product?.name ?? ''
    },
  },
  props: {
    modelValue: {
      type: Object as PropType<Box> | undefined,
      default: undefined
    }
  },
  data(){
    return {
      productsLoading: false,
      products: []as Array<ProductOnly & ProductLocations>,
      deleting: false,
      saving: false,
      newName: undefined as (string|undefined),
      container: undefined as (Location|undefined|null),
      rules: {
        not_empty: (value: string) => value !== '' || this.$t('boxes.box.rules.new_name_empty')
      },
      edit: false,
      saveClicked: false,
      deleteClicked: false,
      product: undefined as undefined|ProductLocations
    }
  },
  methods: {
    async loadProducts() {
      this.productsLoading = true

      const {products} = await this.axios.getContent(this.box?.id ?? null)
      this.products = products
      this.productsLoading = false
    },
    reset() {
      Object.assign(this.$data, this.$options.data.apply(this))
    },
    redirectToContainer() {
      if (!this.box?.location?.id)
        return;


      this.$router.push("/storage/locations/" + this.box!.location!.id + "/" + this.$t('box', {name: this.box!.name ?? ''}))
    },
    toggleEdit(event: boolean) {
      this.edit = event
      if (!this.edit) {
        this.newName = undefined
        this.container = undefined
      }
    },
    async handleDelete(event: string) {
      if (event === "accept") {
        this.deleting = true

        let status = await this.axios.deleteStorage(this.box?.id ?? null)
        this.deleting = false
        if (status) {
          this.visible = false
          this.$notify({
            title: this.$t('toasts.titles.success.deleted_box'),
            text: this.$t('toasts.text.success.deleted_box'),
            type: "success"
          })
          this.$emit('deleted')
        }
        return status
      }
    },
    async handleSave(event: string) {
      if (event !== "accept") {
        return false
      }

      // TODO EMPTY NAMES SHOULD NOT BE ALLOWED EVEN WHEN RENAMING!!!!
      this.saving = true
      const {updated} = await this.axios.updateBox(this.box?.id ?? null, {
        name: this.name,
        location_id: this.boxContainer?.id
      })

      this.saving = false
      if (updated !== undefined) {
        this.$emit('updated', updated)
        this.$notify({
          title: this.$t('toasts.titles.success.updated_box'),
          text: this.$t('toasts.text.success.updated_box'),
          type: "success"
        })
      }
    },
    async eventHandler(event: string, type: string, callback: () => void) {
      switch (type) {
        case "delete":
          this.deleteClicked = false
          await this.handleDelete(event)
          this.deleting = false
          break;
        case "save":
          this.saveClicked = false
          await this.handleSave(event)
          this.saving = false
          break
      }
      callback()
    },
    async deleteProduct(id: number, product_id: number, callback: () => void) {

      let success = await this.productEndpoint.deleteProductAt(id)
      if (success) {
        this.$notify({
          title: this.$t('toasts.titles.success.deleted_detail'),
          text: this.$t('toasts.text.success.deleted_detail'),
          type: "success"
        })
        this.products = []
        this.loadProducts()
        this.$emit('contentChanged', this.box?.id)
      }
      callback()
      this.product = undefined
    },
    async updateProduct(mapping: ProductLocations, update: Partial<ProductLocations>, callback: () => void) {
      const {success, updated, deleted} = await this.productEndpoint.updateProductAt(mapping.id, update)
      if(!success)
      {
        callback()
        return false;
      }

      callback()
      this.products = []
      this.loadProducts()
      this.$notify({
        title: this.$t('toasts.titles.success.updated_detail'),
        text: this.$t('toasts.text.success.updated_detail'),
        type: "success"
      })
      if(
          deleted !== undefined ||
          updated!.id !== this.product?.id ||
          updated!.storage?.id !== this.box?.id
      )
      {
        this.$emit('contentChanged', this.box?.id, updated?.storage?.id)
        this.product = undefined
      }

    }
  }
})
</script>

<template>
  <product-detail-overlay
      v-model="product"
      :product-name="productName"
      :disable-storage-title="true"
      @product-mapping:delete="deleteProduct"
      @product-mapping:update="updateProduct"

  />



  <detail-overlay
      @toggle-edit="toggleEdit($event)"
      v-model="visible"
      @deny="(event: 'save'|'delete', callback: () => void) => eventHandler('deny', event, callback)"
      @accept="(event: 'save'|'delete', callback: () => void) => eventHandler('accept', event, callback)"
      :loading="productsLoading"
  >
    <template #title>
      <app-overlay-title
        v-model="name"
        :rules="[rules.not_empty]"
        :edit="edit"
      />
    </template>
    <template #subTitle >
      <app-storage-title
          :icon="storageTitle.icon"
          :title="storageTitle.name"
          color="primary"
          @click="redirectToContainer()"
          v-if="!edit"
      />
      <app-storage-select
          class="mt-1"
          v-model="boxContainer"
          v-else-if="edit"
      />
    </template>
    <RecycleScroller
        :items="boxProducts"
        :item-size="90"
    >

      <template #default="{item}">
        <product-card
          :id="item.id"
          :name="item.name"
          :totalAmount="item.amount"
          :creation-date="item.updated_at"
          :is-updated-date="true"
          @expand="product={
            ...item,
            storage: box
          }"
        />
      </template>
      <template #after>
        <v-row
            :no-gutters="true"
            justify="center"
        >
          <p>
            {{ $t("boxes.box.all_displayed")}}
          </p>
        </v-row>
      </template>
    </RecycleScroller>


    <template v-slot:delete-confirm="del">
      <app-confirm-modal
          @deny="del.deny()"
          @accept="del.accept()"
          :dialog="del.active"
          :no-click-animation="true"
          :title="$t('boxes.confirm.delete.title')"
          :body="$t('boxes.confirm.delete.body')"
      />
    </template>
    <template v-slot:save-confirm="save">
      <app-confirm-modal
          @deny="save.deny()"
          @accept="save.accept()"
          :dialog="save.active"
          :no-click-animation="true"
          :title="$t('boxes.confirm.save.title')"
          :body="$t('boxes.confirm.save.body')"
      />
    </template>
  </detail-overlay>
</template>

<style scoped lang="scss">

</style>