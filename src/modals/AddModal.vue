<template>
    <div id="mainContainerAddModal">
        <svg @click="$emit('closeModal')" id="exitButton" xmlns="http://www.w3.org/2000/svg" height="48" viewBox="0 96 960 960" width="48"><path d="m249 849-42-42 231-231-231-231 42-42 231 231 231-231 42 42-231 231 231 231-42 42-231-231-231 231Z"/></svg>
        <div id="addWhat">
            <tag @click="categoryChange('product')" text="Product" :active="this.product_active"> </tag>
            <tag @click="categoryChange('box')" :active="this.box_active" text="Box"> </tag>
            <tag @click="categoryChange('location')" :active="this.location_active" text="Location"> </tag>
        </div>

        <div id="containerWhat" v-if="this.product_active == 'true'">
            <input-text-enhanced placeholder="name"/>
            <input-text-enhanced placeholder="box"/>
            <input-text-enhanced placeholder="room"/>
            <input-text-enhanced placeholder="amount"/>
            <input-text-enhanced placeholder="starred"/>
            <bigger-button-center text="Add Product" />
        </div>

        <div id="containerWhat" v-if="this.box_active == 'true'">
            <input-text-enhanced placeholder="name"/>
            <input-text-enhanced placeholder="room"/>
            <bigger-button-center text="Add Box" />
        </div>


        <div id="containerWhat" v-if="this.location_active == 'true'">
            <input-text-enhanced placeholder="name"/>
            <bigger-button-center text="Add Location" />
        </div>

    </div>
</template>

<script>
import Tag from '@/components/Tag.vue';
import InputTextEnhanced from '@/components/InputTextEnhanced.vue';
import BiggerButtonCenter from '@/components/BiggerButtonCenter.vue';

export default {
name: 'App',
components: {
    Tag,
    InputTextEnhanced,
    BiggerButtonCenter
}, 
data() {
    return {
      product_active: "true",
      box_active: "false",
      location_active: "false"
    }
},
  methods: {
    categoryChange(change_to) {
        if (change_to == "product") {
            this.product_active = "true"; this.box_active = "false"; this.location_active = "false";
        } else if (change_to == "box")  {
            this.product_active = "false"; this.box_active = "true"; this.location_active = "false";
        } else {
            this.product_active = "false"; this.box_active = "false"; this.location_active = "true";
        }
    }
}
}
</script>

<style scoped>
#mainContainerAddModal {
    position: absolute;
    top: 2.5vh;
    bottom : 2.5vh;
    left: 5vw;
    right: 5vw;
    background-color: rgba(0,0,0,0.5);
    backdrop-filter: blur(15px);
    border-radius: 10px;
    border: white solid 1px;
}

#exitButton {
    position: absolute;
    right: 10px;
    top: 10px;
    fill: white;
    border: 1px solid white;
    border-radius: 10px;
    cursor: pointer;
}

#addWhat {
    position: absolute;
    display: flex;
    top: 15vh;
    left: 50%;
    transform: translateX(-50%);
}

#containerWhat {
    position: absolute;
    top: 25vh;
    left: 5%;
    width: 90%;
}
</style>
  