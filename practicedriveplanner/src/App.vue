<template>
  <v-app>
    <v-main>
      <Form/>
    </v-main>
  </v-app>
</template>

<script>
import Form from './components/Form.vue'

export default {
  name: 'App',

  components: {
    Form
  },

  data: () => ({
    //
  })
}
</script>
