<template>
    <v-card>
      <v-card-title>
        Locate Safe Hiking Track
      </v-card-title>
        <v-card-text>
          <v-form class="px-3" ref="form">
            <v-text-field label="Current Address" :rules="rules" prepend-icon="mdi-home" v-model="currentAddress"></v-text-field>
            <v-row>
              <v-col cols="8">
                <v-slider label="Mile Radius" :rules="rules" prepend-icon="mdi-map-marker" v-model.number="radiusloc" max="500" min="2" thumb-label></v-slider>
              </v-col>
              <v-col cols="1"><span class="text-body-1">{{radiusloc}}</span></v-col>
              <v-col cols="8">
                <v-slider label="Number Of Breaks" :rules="rules" prepend-icon="mdi-map-marker" v-model.number="numberOfStops" max="10" min="2" thumb-label></v-slider>
              </v-col>
              <v-col cols="1"><span class="text-body-1">{{numberOfStops}}</span></v-col>
              <v-col cols="3">
                <v-select label="Hiking Ability" dense :rules="rules" :items="drivingAbilityChoices" v-model="drivingAbility"></v-select>
              </v-col>
            </v-row>
            <v-btn class="success mx-0 mt-3" @click="submitForm()">Find Me A Hiking Track</v-btn>
          </v-form>
        </v-card-text>
    </v-card>
</template>

<script>
import '@mdi/font/css/materialdesignicons.css'
import { Loader } from '@googlemaps/js-api-loader'

const loader = new Loader({
  apiKey: '',
  version: 'weekly',
  libraries: ['places']
})

loader
  .load()
  .then((google) => {
    this.google = google
  })
  .catch(e => {
    console.log(e)
  })

export default {
  data () {
    return {
      drivingAbilityChoices: ['Beginner', 'Intermediate', 'Proficient'],
      currentAddress: null,
      radiusloc: null,
      numberOfStops: null,
      drivingAbility: null,
      google: null
    }
  },
  methods: {
    submitForm () {
      if (!this.$refs.form.validate()) {
        return
      }
      this.$emit('submit-form', {
        currentAddress: this.currentAddress,
        radiusloc: this.radiusloc,
        numberOfSteps: this.numberOfStops,
        drivingAbility: this.drivingAbility
      })
      this.currentAddress = null
      this.radiusloc = null
      this.numberOfStops = null
      this.drivingAbility = null
    }
  },
  computed: {
    rules () {
      const rules = []
      rules.push(v => !!v || 'Required field')
      return rules
    }
  }
}
</script>
