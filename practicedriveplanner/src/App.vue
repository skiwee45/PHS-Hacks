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
      <MapRender v-if="start" :start="start"/>
    </v-main>
  </v-app>
</template>

<script>
import Form from './components/Form.vue'
import MapRender from './components/MapRender.vue'

export default {
  name: 'App',

  components: {
    Form,
    MapRender
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
  background: url('https://onicodod.sirv.com/1920x1080-5408292-snow-road-forest-winter-tree-frozen-wood-cold-driving-curve-drone-view-aerial-view-mountain-ice-aerial-drone-car-oregon-mt-hood-national-forest-png-images.jpg') center fixed !important;
  background-size: 700px;
}
</style>
