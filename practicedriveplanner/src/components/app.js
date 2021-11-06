let map;
let service;
let infowindow;
//var test = [];
var latitude = 40.306;
var longitude = -74.6197;

//this functions uses geocoder api to convert the address to lat and lng coords
function inputToCoord() {
  var geocoder = new google.maps.Geocoder();
  var address = currentAddress; //currentAddress is variable initialized in Form.vue, which is the current Address of the driver
  geocoder.geocode({ address: address }, function (results, status) {
    if (status == google.maps.GeocoderStatus.OK) {
      latitude = results[0].geometry.location.lat();
      longitude = results[0].geometry.location.lng();

      initMap();
    }
  });
}

function initMap() {
  const location = new google.maps.LatLng(latitude, longitude);

  infowindow = new google.maps.InfoWindow();
  map = new google.maps.Map(document.getElementById("map"), {
    center: location,
    zoom: 25,
  });

  const request = {
    query: "neighborhood",
    fields: ["types"],
  };

  service = new google.maps.places.PlacesService(map);
  service.textSearch(request, (results, status) => {
    if (status === google.maps.places.PlacesServiceStatus.OK && results) {
      for (let i = 0; i < results.length; i++) {
        createMarker(results[i]);
        test.push(results[i]);
      }

      //map.setCenter(results[0].geometry.location);
    }
  });
}

function createMarker(place) {
  if (!place.geometry || !place.geometry.location) return;

  const marker = new google.maps.Marker({
    map,
    position: place.geometry.location,
  });

  google.maps.event.addListener(marker, "click", () => {
    infowindow.setContent(place.name || "");
    infowindow.open(map);
  });
}

// const center = { lat: 40.306, lng: -74.6197 };
// // Create a bounding box with sides ~10km away from the center point
// const defaultBounds = {
//   north: center.lat + 0.1,
//   south: center.lat - 0.1,
//   east: center.lng + 0.1,
//   west: center.lng - 0.1,
// };

// const input = document.getElementById("pac-input");
// const options = {
//   bounds: defaultBounds,
//   componentRestrictions: { country: "us" },
//   fields: ["address_components", "geometry", "icon", "name"],
//   strictBounds: false,
//   types: ["establishment"],
// };
// const autocomplete = new google.maps.places.Autocomplete(input, options);

// var axios = require("axios");

// var config = {
//   method: "get",
//   url: "https://maps.googleapis.com/maps/api/distancematrix/json?origins=40.6655101%2C-73.89188969999998&destinations=40.659569%2C-73.933783%7C40.729029%2C-73.851524%7C40.6860072%2C-73.6334271%7C40.598566%2C-73.7527626&key=AIzaSyBdZ8GXm2rC-co5WIseA-9sQRtCZATT84I",
//   headers: {},
// };

// axios(config)
//   .then(function (response) {
//     console.log(JSON.stringify(response.data));
//   })
//   .catch(function (error) {
//     console.log(error);
//   });

// AIzaSyBdZ8GXm2rC-co5WIseA-9sQRtCZATT84I
// Distance Matri Api Key: