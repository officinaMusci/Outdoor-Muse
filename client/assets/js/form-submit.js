function objectifyForm(formArray) {
  //serialize data function
  let returnArray = {};
  for (let i = 0; i < formArray.length; i++){
      returnArray[formArray[i]['name']] = formArray[i]['value'];
  }
  return returnArray;
}

function formatDatetime(date, time) {
  return date + ' ' + time + ':00.00';
}

function formatTimedelta(time) {
  return time.replace(/^0/, '') + ':00';
}

function createWeatherIds(data) {
  let weatherIdGroups = {
    weatherClear: [800],
    weatherClouds: [801, 802, 803, 804],
    weatherOther: [300, 301, 302, 310, 311, 312, 313, 314, 321, 701, 711, 721, 731, 741, 751, 761, 762, 771, 781],
    weatherRain: [500, 501, 502, 503, 504, 511, 520, 521, 522, 531],
    weatherSnow: [600, 601, 602, 611, 612, 613, 615, 616, 620, 621, 622],
    weatherThunderstorm: [200, 201, 202, 210, 211, 212, 221, 230, 231, 232]
  };

  let filtered = Object.keys(data)
    .filter(key => key.startsWith('weather'))
    .reduce((obj, key) => {
      obj[key] = data[key];
      return obj;
    }, {});
  
  let weatherIds = [];
  Object.keys(filtered).map(function(key, index) {
    weatherIds = weatherIds.concat(weatherIdGroups[key]);
  });

  return weatherIds;
}

function capitalizeFirstLetter(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}

function getTime(datetime) {
  // TODO: Get offset dynamically
  function addLeadingZero(str) {
    return ('0' + str).slice(-2);
  }
  return addLeadingZero(datetime.getHours() - 1) + ':' + addLeadingZero(datetime.getMinutes()) + ':' + addLeadingZero(datetime.getSeconds())
}

function getTimePercentage(duration, total) {
  function totalSeconds(time){
    let parts = time.split(':');
    return parts[0] * 3600 + parts[1] * 60 + parts[2];
  }
  return (100 * totalSeconds(duration) / totalSeconds(total)).toFixed(2);
}

function makeMap(container, data) {
  let id = container.attr('id');
  let map = L.map(id).setView([data.destination.location.lat, data.destination.location.lng], 7);

  L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: 'pk.eyJ1IjoiZGFuaWxvbXVzY2kiLCJhIjoiY2t2djdzcGhvMDgwbzJvcGhpeXdpMnprbyJ9.SuYbPwo5khMJgmfmRsp47g'
  }).addTo(map);

  let startIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-grey.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
  });
  L.marker([data.start_location.lat, data.start_location.lng], {icon: startIcon}).addTo(map);
  
  let endIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
  });
  L.marker([data.destination.location.lat, data.destination.location.lng], {icon: endIcon}).addTo(map);
}

function createResults(results) {
  $('#solutions-container .badge').text(results.length);

  if (results.length) {
    results.forEach((result, index) => {
      let clone = $('#toClone').clone();
  
      let title = result.destination.name;

      // TEMP
      if (title.split(' - ')[0] === title.split(' - ')[1]) {
        title = title.split(' - ')[0];
      }
  
      let outwardStart = new Date(result.outward_itinerary.interval.start);
      let outwardWalkDuration = result.outward_itinerary.walk_duration;
      let outwardTravelDuration = result.outward_itinerary.travel_duration;
      let outwardEnd = new Date(result.outward_itinerary.interval.end);
      let returnStart = new Date(result.return_itinerary.interval.start);
      let returnWalkDuration = result.return_itinerary.walk_duration;
      let returnTravelDuration = result.return_itinerary.travel_duration;
      let returnEnd = new Date(result.return_itinerary.interval.end);
      let totalTripDuration = result.info.total_trip_duration;
  
      let difficulty = result.destination.difficulty;
      let weather = capitalizeFirstLetter(result.forecasts[0].weather[0].description);
      let weatherIcon = 'http://openweathermap.org/img/wn/' + result.forecasts[0].weather[0].icon + '@2x.png';
      let destinationDuration = result.destination.duration;
      let freeTimeDuration = result.info.free_time;
      
      clone.find('.outwardTravelDurationBar').css('width', getTimePercentage(outwardTravelDuration, totalTripDuration) + '%')
      clone.find('.outwardWalkDurationBar').css('width', getTimePercentage(outwardWalkDuration, totalTripDuration) + '%')
      clone.find('.destinationDurationBar').css('width', getTimePercentage(destinationDuration, totalTripDuration) + '%')
      clone.find('.freeTimeDurationBar').css('width', getTimePercentage(freeTimeDuration, totalTripDuration) + '%')
      clone.find('.returnWalkDurationBar').css('width', getTimePercentage(returnWalkDuration, totalTripDuration) + '%')
      clone.find('.returnTravelDurationBar').css('width', getTimePercentage(returnTravelDuration, totalTripDuration) + '%')
  
      clone.find('.card-title').text(title);
  
      clone.find('td.outwardStart').text(getTime(outwardStart));
      clone.find('td.outwardWalkDuration').text(outwardWalkDuration);
      clone.find('td.outwardTravelDuration').text(outwardTravelDuration);
      clone.find('td.outwardEnd').text(getTime(outwardEnd));
      clone.find('td.returnStart').text(getTime(returnStart));
      clone.find('td.returnWalkDuration').text(returnWalkDuration);
      clone.find('td.returnTravelDuration').text(returnTravelDuration);
      clone.find('td.returnEnd').text(getTime(returnEnd));
  
      clone.find('td.weather span').text(weather);
      clone.find('td.weather img').attr('src', weatherIcon);
      clone.find('td.difficulty').text(difficulty);
      clone.find('td.destinationDuration').text(destinationDuration);
      clone.find('td.freeTimeDuration').text(freeTimeDuration);
      
      clone.removeAttr('id');
      clone.removeAttr('style');
      clone.appendTo('#solutions');

      let mapContainer = clone.find('.map');
      mapContainer.attr('id', 'map-' + index);
      makeMap(mapContainer, result);
    });
  
  } else {
    $('#solutions .noResults').show();
  }
}

$(document).ready(function () {
  let form = $('form');
  let inputs = form.find("input, button[type=submit]");

  inputs.on('input', function() {
    form.removeClass('was-validated');
  });

  $(document).on('submit', 'form', function(event) {
    event.preventDefault();
    event.stopPropagation();

    $('#solutions-container .badge').text(0);
    $('#solutions > .card:not(#toClone)').remove();
    $('#solutions .alert').hide();

    let data = objectifyForm(form.serializeArray())
    let json = {
      'location': {
        'lat': parseFloat(data.lat),
        'lng': parseFloat(data.lng)
      },
      'interval': {
          'start': formatDatetime(data.date, data.timeFrom),
          'end': formatDatetime(data.date, data.timeTo)
      },
      'radius': parseInt(data.radius) * 1000,
      'type': 'hike',
      'max_travel': formatTimedelta(data.maxTravel),
      'max_walk': formatTimedelta(data.maxWalk),
      'weather_ids': createWeatherIds(data),
      'max_results': 25
    }
    
    if (form[0].checkValidity() !== false) {
      inputs.prop("disabled", true);
      $(".loading").show();
      $(".notLoading").hide();
      $.ajax({
        url: 'http://127.0.0.1:5000/api/v1/execute-query',
        type: "POST",
        contentType: 'application/json',
        data: JSON.stringify(json),
        dataType: 'json',

        success: function(result) {
          if (!result.error) {
            form.addClass('was-validated');
            inputs.prop("disabled", false);
            $(".loading").hide();
            $(".notLoading").show();
            createResults(result.results);
          }
          console.log(result);
        },

        error: function(error) {
          inputs.prop("disabled", false);
          $(".loading").hide();
          $(".notLoading").show();
          $('#solutions .errorMessage').show();
          console.log(error.responseJSON);
        }
      });
    }
  });
});
