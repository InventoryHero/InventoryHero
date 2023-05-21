<template>
    <SandwichMenu :title="this.title"/>
    <v-virtual-scroll
        class="virtual-scroll-bg"
        :height="80+'vh'"
        :items="rooms"
    >
        <template v-slot:default="{ item }">
            <RoomCard class="card" :id="item.id" :roomName="item.name" :numBoxes="item.box_cnt" :numProducts="item.product_cnt"/>
        </template>
    </v-virtual-scroll>
    <add-modal ::defaultAddView="this.defaultModalView" v-if="this.addModalVisibility" @closeModal="closeModal()"/>
    <add-button @click="this.addModalVisibility = true"/>
    <qr-button/>
</template>

<script>
import AddButton from '@/components/AddButton.vue'
  import QrButton from '@/components/QrButton.vue'
  import RoomCard from "@/components/RoomCard.vue";
import SandwichMenu from "@/components/SandwichMenu.vue";

import {DB_SB_get_rooms, DB_SB_getStarredProducts} from '@/db/supabase';
import {getUser} from "@/db/dexie";
import AddModal from "@/modals/AddModal.vue";
import { Constants } from "@/global/constants";

  
  export default {
    name: 'App',
    components: {
        AddModal,
        RoomCard,
        AddButton,
        QrButton,
        SandwichMenu
    },
    data() {
        return {
            rooms: [],
            currentUser: "",
            addModalVisibility: false,
            Constants,
            title: "Locations",
            defaultModalView: Constants.LocationsView,
        }
    },
    methods: {
        get_rooms() {
            DB_SB_get_rooms(this.currentUser.username).then((rooms) => {
                this.rooms = rooms;
            });
        },
        closeModal() {
            this.addModalVisibility = false;
            DB_SB_getStarredProducts().then((res) => {
                this.starred_products = res;
            })
        },
    },
    beforeMount() {

        getUser().then((user) => {
            if(user === undefined)
            {
                this.$router.push("/login");
            }
            this.currentUser = user;
            this.get_rooms();
        });
    }

  }
</script>
  
<style scoped>
    .card {
        padding-left: 2.5%;
        padding-right: 2.5%;
    }
    .v-virtual-scroll{
        background: var(--color-blue);
    }
    ::-webkit-scrollbar { width: 0px;  }
</style>
  