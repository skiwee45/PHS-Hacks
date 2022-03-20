<template>
  <v-app>
    <v-main>
      <v-dialog v-model="dialog" width="700">
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            :color="formButtonColor"
            dark
            v-bind="attrs"
            v-on="on"
          >
            Generate New Route
          </v-btn>
        </template>
        <Form @submit-form="SubmitForm" />
      </v-dialog>
      <br/>
      <br/>
      <v-img v-show="start" src="./assets/shot.png" width=" 10000px" height="800px" />
    </v-main>
  </v-app>
</template>

<script>
import Form from './components/Form.vue'
// import MapRender from './components/MapRender.vue'

export default {
  name: 'App',

  components: {
    Form
    // MapRender
  },

  methods: {
    SubmitForm (form) {
      this.dialog = false
      this.inRoute = true
      this.start = form.currentAddress
    }
  },

  data: () => ({
    dialog: false,
    currentRoute: null,
    pastRoutes: [],
    start: '',
    end: ''
  }),

  computed: {
    inRoute () {
      return !!this.currentRoute
    },
    formButtonColor () {
      return this.inRoute ? 'error' : 'success'
    },
    origin () {
      if (!this.start) return null
      return { query: this.start }
    },
    destionation () {
      if (!this.end) return null
      return { query: this.end }
    }
  }
}
</script>

<style>
#app {
  background: url('https://www.xmple.com/wallpaper/black-green-gradient-linear-1920x1080-c2-000000-228b22-a-105-f-14.svg') center fixed !important;
  background-size: 700px;
}
</style>
