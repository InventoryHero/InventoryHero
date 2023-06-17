<template>
    <v-dialog
        transition="dialog-bottom-transition"
        width="auto"
        v-model="this.model"
    >
        <v-card
            height="100%"
            class="d-flex-column modal-container"
        >
            <v-toolbar
                title="Scan IH QR-Code"
                class="toolbar"
            >
                <v-icon class="me-5" icon="fa:fas fa-times" @click="closeModal()"></v-icon>
            </v-toolbar>
            <v-card-text>
                <qrcode-stream  @decode="onDecode"  @init="logErrors"></qrcode-stream>
            </v-card-text>
        </v-card>

    </v-dialog>
</template>

<script>
import {QrcodeStream} from "vue-qrcode-reader/src";

export default {
    name: 'App',
    props: {
        model: Boolean

    },
    components: {
        QrcodeStream

    },
    data() {

    },
    methods: {
        async onDecode(decodedString)
        {
            console.log("HALLO");
            try{
                let data = JSON.parse(decodedString);
                this.$emit('loadDetailView', data);
            }catch(e)
            {
                console.log("error while reading qr code");
            }

        },
        closeModal()
        {
            this.$emit('closeQrModal')
        },
        logErrors (promise) {
            promise.catch(console.error)
        }

    },
    beforeMount() {

    }
}
</script>

<style scoped>
.modal-container{
    background-color: rgba(0,0,0,0.5);
    backdrop-filter: blur(15px);
    border-radius: 10px;
    border: white solid 1px;
    height: 60vh;
    color: white;
}
.toolbar{
    background-color: transparent;
    border-bottom: white solid 1px;
    color: white;
}
</style>
  