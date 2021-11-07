let map
let service
let infowindow
var test = []
var latitude = 40.306
var longitude = -74.6197
var directionsService
var directionsRenderer

function inputToCoord () {
  var geocoder = new google.maps.Geocoder()
  var address = document.getElementById('loc').value
  geocoder.geocode({ address: address }, function (results, status) {
    if (status == google.maps.GeocoderStatus.OK) {
      latitude = results[0].geometry.location.lat()
      longitude = results[0].geometry.location.lng()

      initMap()
    }
  })
}

function initMap () {
  directionsService = new google.maps.DirectionsService()
  directionsRenderer = new google.maps.DirectionsRenderer()
  const location = new google.maps.LatLng(latitude, longitude)

  infowindow = new google.maps.InfoWindow()
  map = new google.maps.Map(document.getElementById('map'), {
    center: location,
    zoom: 25
  })

  const request = {
    query: 'neighborhood',
    fields: ['types']
  }

  service = new google.maps.places.PlacesService(map)
  service.textSearch(request, (results, status) => {
    if (status === google.maps.places.PlacesServiceStatus.OK && results) {
      for (let i = 0; i < results.length; i++) {
        createMarker(results[i])
        test.push(results[i])
      }

      // map.setCenter(results[0].geometry.location);
    }
  })

  const center = { lat: latitude, lng: longitude }
  // Create a bounding box with sides ~10km away from the center point
  const defaultBounds = {
    north: center.lat + 0.1,
    south: center.lat - 0.1,
    east: center.lng + 0.1,
    west: center.lng - 0.1
  }

  const input = document.getElementById('loc')
  const options = {
    bounds: defaultBounds,
    componentRestrictions: { country: 'us' },
    fields: ['address_components', 'geometry', 'icon', 'name'],
    strictBounds: false,
    types: ['establishment']
  }
  const autocomplete = new google.maps.places.Autocomplete(input, options)

  calcRoute(true, latitude, longitude, 35.9605454, -80.0020807)
  directionsRenderer.setMap(map)
}

function createMarker (place) {
  if (!place.geometry || !place.geometry.location) return

  const marker = new google.maps.Marker({
    map,
    position: place.geometry.location
  })

  google.maps.event.addListener(marker, 'click', () => {
    infowindow.setContent(place.name || '')
    infowindow.open(map)
  })
}

function getReverseGeocodingData (lat, lng) {
  var latlng = new google.maps.LatLng(lat, lng)
  // This is making the Geocode request
  var geocoder = new google.maps.Geocoder()
  geocoder.geocode({ latLng: latlng }, function (results, status) {
    if (status !== google.maps.GeocoderStatus.OK) {
      alert(status)
    }
    // This is checking to see if the Geoeode Status is OK before proceeding
    if (status == google.maps.GeocoderStatus.OK) {
      console.log(results)
      var address = results[0].formatted_address
    }
  })
}

function calcRoute (reverse, sLat, sLong, eLat, eLong) {
  if (!reverse) {
    var start = { lat: sLat, lng: sLong }
    var end = { lat: eLat, lng: eLong }
  } else {
    var end = { lat: latitude, lng: longitude }
    var start = { lat: eLat, lng: eLong }
  }
  var request = {
    origin: start,
    destination: end,
    travelMode: 'DRIVING'
  }
  directionsService.route(request, function (result, status) {
    if (status == 'OK') {
      directionsRenderer.setDirections(result)
    }
  })
}
