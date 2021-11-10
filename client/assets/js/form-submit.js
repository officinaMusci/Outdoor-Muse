function objectifyForm(formArray) {
  //serialize data function
  var returnArray = {};
  for (var i = 0; i < formArray.length; i++){
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
  var weatherIdGroups = {
    weatherClear: [800],
    weatherClouds: [801, 802, 803, 804],
    weatherOther: [300, 301, 302, 310, 311, 312, 313, 314, 321, 701, 711, 721, 731, 741, 751, 761, 762, 771, 781],
    weatherRain: [500, 501, 502, 503, 504, 511, 520, 521, 522, 531],
    weatherSnow: [600, 601, 602, 611, 612, 613, 615, 616, 620, 621, 622],
    weatherThunderstorm: [200, 201, 202, 210, 211, 212, 221, 230, 231, 232]
  };

  var filtered = Object.keys(data)
    .filter(key => key.startsWith('weather'))
    .reduce((obj, key) => {
      obj[key] = data[key];
      return obj;
    }, {});
  
  var weatherIds = [];
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
    var parts = time.split(':');
    return parts[0] * 3600 + parts[1] * 60 + parts[2];
  }
  return (100 * totalSeconds(duration) / totalSeconds(total)).toFixed(2);
}

function createResults(results) {
  $('#solutions-container .badge').text(results.length)
  $('#solutions > div:not(#toClone)').remove();

  results.forEach(result => {
    var clone = $('#toClone').clone();

    var title = result.destination.name;
    var outwardStart = new Date(result.outward_itinerary.interval.start);
    var outwardWalkDuration = result.outward_itinerary.walk_duration;
    var outwardTravelDuration = result.outward_itinerary.travel_duration;
    var outwardEnd = new Date(result.outward_itinerary.interval.end);
    var returnStart = new Date(result.return_itinerary.interval.start);
    var returnWalkDuration = result.return_itinerary.walk_duration;
    var returnTravelDuration = result.return_itinerary.travel_duration;
    var returnEnd = new Date(result.return_itinerary.interval.end);
    var totalTripDuration = result.info.total_trip_duration;
    var freeTimeDuration = result.info.free_time;
    var difficulty = result.destination.difficulty;
    var weather = capitalizeFirstLetter(result.forecasts[0].weather[0].description);
    
    clone.find('.outwardTravelDurationBar').css('width', getTimePercentage(outwardTravelDuration, totalTripDuration) + '%')
    clone.find('.outwardWalkDurationBar').css('width', getTimePercentage(outwardWalkDuration, totalTripDuration) + '%')
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
    clone.find('td.weather').text(weather);
    clone.find('td.difficulty').text(difficulty);
    clone.find('td.freeTimeDuration').text(freeTimeDuration);
    
    clone.removeAttr('id');
    clone.removeAttr('style');
    clone.appendTo('#solutions');
  });
}

$(document).ready(function () {
  var form = $('form');
  var inputs = form.find("input, button[type=submit]");

  inputs.on('input', function() {
    form.removeClass('was-validated');
  });

  $(document).on('submit', 'form', function(event) {
    event.preventDefault();
    event.stopPropagation();

    var data = objectifyForm(form.serializeArray())
    var json = {
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
      'max_results': 100
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
          console.log(error.responseJSON);
        }
      });
    }
  });
});
