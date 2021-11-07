<template>
  <div id="map" ref="map"></div>
</template>

<script>
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
  created: this.initMap(),
  data () {
    return {
      directionsService: null,
      directionsRenderer: null,
      map: null,
      service: null,
      infowindow: null,
      latitude: 40.306,
      longitude: -74.6197,
      google: null
    }
  },
  props: {
    start: {
      type: String,
      require: true
    },
    end: {
      type: String,
      require: true
    }
  },
  methods: {
    initMap () {
      this.directionsService = new this.google.maps.DirectionsService()
      this.directionsRenderer = new this.google.maps.DirectionsRenderer()
      var chicago = new this.google.maps.LatLng(41.850033, -87.6500523)
      var mapOptions = {
        zoom: 7,
        center: chicago
      }
      var map = new this.google.maps.Map(this.$refs.map, mapOptions)
      this.directionsRenderer.setMap(map)
    },
    inputToCoord (address) {
      var geocoder = new this.google.maps.Geocoder()
      geocoder.geocode({ address: address }, function (results, status) {
        if (status === this.google.maps.GeocoderStatus.OK) {
          this.latitude = results[0].geometry.location.lat()
          this.longitude = results[0].geometry.location.lng()

          this.initMap()
        }
      })
    },
    createMarker (place) {
      if (!place.geometry || !place.geometry.location) return

      const marker = new this.google.maps.Marker({
        map: this.map,
        position: place.geometry.location
      })

      this.google.maps.event.addListener(marker, 'click', () => {
        this.infowindow.setContent(place.name || '')
        this.infowindow.open(this.map)
      })
    },
    // getReverseGeocodingData (lat, lng) {
    //   var latlng = new this.google.maps.LatLng(lat, lng)
    //   // This is making the Geocode request
    //   var geocoder = new this.google.maps.Geocoder()
    //   geocoder.geocode({ latLng: latlng }, function (results, status) {
    //     if (status !== this.google.maps.GeocoderStatus.OK) {
    //       alert(status)
    //     }
    //     // This is checking to see if the Geoeode Status is OK before proceeding
    //     if (status === this.google.maps.GeocoderStatus.OK) {
    //       console.log(results)
    //       var address = results[0].formatted_address
    //     }
    //   })
    // },
    calcRoute (reverse, sLat, sLong, eLat, eLong) {
      // if (!reverse) {
      //   var start = { lat: sLat, lng: sLong }
      //   var end = { lat: eLat, lng: eLong }
      // } else {
      //   var end = { lat: this.latitude, lng: this.longitude }
      //   var start = { lat: this.eLat, lng: this.eLong }
      // }

      var start = { lat: sLat, lng: sLong }
      var end = { lat: eLat, lng: eLong }

      var request = {
        origin: start,
        destination: end,
        travelMode: 'DRIVING'
      }
      this.directionsService.route(request, function (result, status) {
        if (status === 'OK') {
          this.directionsRenderer.setDirections(result)
        }
      })
    }
  }
}
</script>
