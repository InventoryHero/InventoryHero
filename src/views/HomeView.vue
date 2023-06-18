<template>
  <div class="viewContainer" :class="this.theme">

  <div id="posStarredMessages">
    <h3>{{this.$t('home_view.starred_products')}}</h3>
    <list-container :list=this.starred_products />
  </div>

    <div id="posLastUsed">
      <h3>{{this.$t('home_view.last_used')}}</h3>
      <list-container :list="[{name: 'Müssen wir noch'}, {name:'abklären, wie wir'}, {name: 'das machen wollen'}, {name: '😁'}]" />
    </div>
  <add-modal v-model="this.addModalVisibility" @closeModal="closeModal()"/>
  <qr-reader-modal
          v-model="this.qrReaderModalVisibility"
          @closeQrModal="closeQrModal()"
          @loadDetailView="loadDetailView"
  />
  <qr-data-modal
          v-model="this.qrCodeDataModalVisibility"
          v-bind:qr-code-data="this.qrCodeData"
          @closeQrDataModal="this.qrCodeDataModalVisibility=false"

  />
  <dock
    @qrButton="this.qrReaderModalVisibility=true"
    @addButton="this.addModalVisibility = true"
  />
  <SandwichMenu :title="this.$t('home')"/>
</div>
</template>

<script>
import SandwichMenu from "@/components/SandwichMenu.vue";
import ListContainer from '@/components/ListContainer.vue';
import AddModal from '@/modals/AddModal.vue';
import QrReaderModal from "@/modals/QrReaderModal.vue";
import QrDataModal from "@/modals/QrDataModal.vue";
import Dock from "@/components/Dock.vue";

import { global_theme } from "@/db/dexie"
import { DB_SB_getStarredProducts } from '@/db/supabase';

export default {
  name: 'App',
  components: {
    SandwichMenu,
    ListContainer,
    AddModal,
    QrReaderModal,
    QrDataModal,
    Dock
  },
  data() {
    return {
      showTitle: true,
      starred_products: [],
      addModalVisibility: false,
      qrReaderModalVisibility: false,
      qrCodeDataModalVisibility: false,
      qrCodeData: Object,
      theme: global_theme,
    }
  },
  methods: {
    closeQrModal()
    {
      this.qrReaderModalVisibility = false;
    },
    loadDetailView(qr_data)
    {
      this.qrCodeData = qr_data;
      this.qrReaderModalVisibility = false;
      this.qrCodeDataModalVisibility = true;
    },
    closeModal() {
      this.addModalVisibility = false;
      DB_SB_getStarredProducts().then((res) => {
        this.starred_products = res;
      })
    },
  },
  
  beforeMount() {
    DB_SB_getStarredProducts().then((res) => {
      this.starred_products = res;
    })
  }
}
</script>

<style scoped>
#posStarredMessages {
  margin-top: 20vh;
  width: 100%;
}

#posLastUsed {
  margin-top: 5vh;
}

h3 {
  text-align: left;
  margin-left: 10%;
}
</style>
