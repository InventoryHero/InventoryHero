<template>
  <div class="containerInputText">
    <input v-if="this.is_pssw == false" :placeholder=this.place_holder type="text" v-model="this.my_value" @input="$emit('valueUpdated', this.my_value)">
    <input v-else :placeholder=this.place_holder type="password" v-model="this.my_value" @input="$emit('valueUpdated', this.my_value)">
  </div>
</template>

<script>
export default {
  name: 'InputText',
  props: ["place_holder", "is_pssw"],
  data() {
    return {
      my_value: ""
    }
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
input {
  background-color: var(--color-cyan);
  color: black;
  width: 60%;
  font-size: 1.5em;
  padding: 20px;
  border: none;
  border-radius: 15px;
}

input:focus {
  outline: none;
}
</style>
