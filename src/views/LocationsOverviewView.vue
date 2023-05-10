<template>
    <SandwichMenu/>
    <v-virtual-scroll
        class="virtual-scroll-bg"
        :height="80+'vh'"
        :items="rooms"
    >
        <template v-slot:default="{ item }">
            <RoomCard class="card" :id="item.id" :roomName="item.name" :numBoxes="item.box_cnt" :numProducts="item.product_cnt"/>
        </template>
    </v-virtual-scroll>
    <add-button/>
    <qr-button/>
</template>

<script>
import AddButton from '@/components/AddButton.vue'
  import QrButton from '@/components/QrButton.vue'
  import RoomCard from "@/components/RoomCard.vue";
import SandwichMenu from "@/components/SandwichMenu.vue";

  import { DB_SB_get_rooms } from '@/db/supabase';
import {getUser} from "@/db/dexie";

  
  export default {
    name: 'App',
    components: {
        RoomCard,
        AddButton,
        QrButton,
        SandwichMenu
    },
    data() {
        return {
            rooms: [],
            currentUser: "",
        }
    },
    methods: {
        get_rooms() {
            DB_SB_get_rooms(this.currentUser.username).then((rooms) => {
                this.rooms = rooms.concat(rooms).concat(rooms).concat(rooms).concat(rooms).concat(rooms).concat(rooms).concat(rooms).concat(rooms);
            });
        }
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
  