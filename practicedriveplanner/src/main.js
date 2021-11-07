import Vue from 'vue'
import App from './App.vue'
import store from './store'
import vuetify from './plugins/vuetify'

import * as VueGoogleMaps from 'vue2-google-maps'

Vue.config.productionTip = false

Vue.use(VueGoogleMaps, {
  load: {
    key: 'AIzaSyBdZ8GXm2rC-co5WIseA-9sQRtCZATT84I',
    libraries: ['places', 'routes']
  }
})

new Vue({
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
