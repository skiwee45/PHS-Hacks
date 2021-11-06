<template>
  <v-container>
    <v-card>
      <v-card-title>
        Generate New Route
      </v-card-title>
        <v-card-text>
          <v-form class="px-3" ref="form">
            <v-text-field label="Current Address" :rules="rules" prepend-icon="mdi-home" v-model="currentAddress"></v-text-field>
            <v-row>
              <v-col cols="8">
                <v-slider label="Number Of Stops" :rules="rules" prepend-icon="mdi-map-marker" v-model.number="numberOfStops" max="10" min="2" thumb-label></v-slider>
              </v-col>
              <v-col cols="1"><v-span class="text-body-1">{{numberOfStops}}</v-span></v-col>
              <v-col cols="3">
                <v-select label="Driving Ability" dense :rules="rules" :items="drivingAbilityChoices" v-model="drivingAbility"></v-select>
              </v-col>
            </v-row>
            <v-btn flat class="success mx-0 mt-3" :disabled="!canSubmit">Generate Route</v-btn>
          </v-form>
        </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import '@mdi/font/css/materialdesignicons.css'

export default {
  data () {
    return {
      drivingAbilityChoices: ['Beginner', 'Intermediate', 'Proficient'],
      currentAddress: null,
      numberOfStops: null,
      drivingAbility: null
    }
  },
  computed: {
    rules () {
      const rules = []
      rules.push(v => !!v || 'Required field')
      return rules
    },
    canSubmit () {
      return this.$refs.form.validate()
    }
  }
}
</script>
