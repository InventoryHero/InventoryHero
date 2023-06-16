<template>
  <div id="posStarredMessages">
    <h3>⭐ Starred Products</h3>
    <list-container :list=this.starred_products />
  </div>

    <div id="posLastUsed">
      <h3>⏰ Last Used Products</h3>
      <list-container :list="[{name: 'Müssen wir noch'}, {name:'abklären, wie wir'}, {name: 'das machen wollen'}, {name: '😁'}]" />
    </div>
    

  <add-modal v-if="this.addModalVisibility" @closeModal="closeModal()"/>
  <add-button @click="this.addModalVisibility = true"/>
  <qr-reader-modal v-model="this.qrReaderModalVisibility" @closeQrModal="closeQrModal()" @loadDetailView="loadDetailView"/>
  <qr-button @click="this.qrReaderModalVisibility=true"></qr-button>
  <qr-data-modal v-model="this.qrCodeDataModalVisibility" v-bind:qr-code-data="this.qrCodeData" @closeQrDataModal="this.qrCodeDataModalVisibility=false"></qr-data-modal>
  <SandwichMenu title="Home"/>
</template>

<script>
import AddButton from '@/components/AddButton.vue'
import QrButton from '@/components/QrButton.vue'
import SandwichMenu from "@/components/SandwichMenu.vue";
import ListContainer from '@/components/ListContainer.vue';
import AddModal from '@/modals/AddModal.vue';
import QrReaderModal from "@/modals/QrReaderModal.vue";
import QrDataModal from "@/modals/QrDataModal.vue";


import { DB_SB_getStarredProducts } from '@/db/supabase';

export default {
  name: 'App',
  components: {
    SandwichMenu,
    AddButton,
    QrButton,
    ListContainer,
    AddModal,
    QrReaderModal,
    QrDataModal
  },
  data() {
    return {
      showTitle: true,
      starred_products: [],
      addModalVisibility: false,
      qrReaderModalVisibility: false,
      qrCodeDataModalVisibility: false,
      qrCodeData: Object,
    }
  },
  methods: {
    openMenu() {
      console.log("open me")
    },
    closeQrModal()
    {
      this.qrReaderModalVisibility = false;
    },
    loadDetailView(qr_data)
    {
      console.log(qr_data);
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
a:visited {
  color: white;
}


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
