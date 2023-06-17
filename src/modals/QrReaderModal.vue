<template>


    <v-dialog
        transition="dialog-bottom-transition"
        width="auto"
        persistent
        no-click-animation
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
import { useToast } from "vue-toastification";

export default {

    name: 'App',
    setup(){
      const toast = useToast();
      return {toast};
    },
    props: {
        model: Boolean

    },
    components: {
        QrcodeStream,


    },
    data() {
        return {
            barcodeInvalid: false,
        }
    },
    methods: {
        async onDecode(decodedString)
        {
            try{
                let data = JSON.parse(decodedString);

                if(!data.hasOwnProperty("id") || ! data.hasOwnProperty("is_room") || !data.hasOwnProperty("is_box") || !data.hasOwnProperty("username"))
                {
                    this.toast.error("Please scan a valid IH qr code!");
                    return;
                }

                this.$emit('loadDetailView', data);
            }catch(e)
            {
                console.log(e);
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
  