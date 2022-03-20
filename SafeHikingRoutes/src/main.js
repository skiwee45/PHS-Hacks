import Vue from 'vue'
import App from './App.vue'
import store from './store'
import vuetify from './plugins/vuetify'

import * as VueGoogleMaps from 'vue2-google-maps'

Vue.config.productionTip = false

Vue.use(VueGoogleMaps, {
  load: {
    key: 'AIzaSyC1COUUe3Uhkj06qQo-_Ha2HwABlyB7qq4',
    libraries: ['places', 'routes']
  }
})

new Vue({
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
