import { Component, Input, OnInit } from '@angular/core';
import { LocationInterface } from 'src/app/app.interfaces';

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.scss']
})
export class MapComponent implements OnInit {
  @Input() set center(value: LocationInterface | undefined) {
    if (value) {
    
      this.options = {
        ...this.options,
        center: value
      }
    }
  };

  @Input() set itinerary(value: any) {
    if (value) {
    
      this.directions = this.addGoogleServiceSDKFields({
        routes: [value],
        request: {
          destination: value.start_location,
          origin: value.end_location,
          travelMode: "TRANSIT"
        }
      })
    }
  };

  public options?: google.maps.MapOptions;
  public directions?: google.maps.DirectionsResult;

  constructor() { }

  ngOnInit(): void {
  }

  addGoogleServiceSDKFields(serverResponse: any) {
    serverResponse.routes = serverResponse.routes.map((response: any) => {
      const bounds = new google.maps.LatLngBounds(
        response.bounds.southwest,
        response.bounds.northeast,
      );
      response.bounds = bounds;
      response.overview_path = google.maps.geometry.encoding.decodePath(response.overview_polyline.points);

      response.legs = response.legs.map((leg: any) => {
        leg.start_location =
          new google.maps.LatLng(leg.start_location.lat, leg.start_location.lng);
        leg.end_location =
          new google.maps.LatLng(leg.end_location.lat, leg.end_location.lng);
        leg.steps = leg.steps.map((step: any) => {
          step.path = google.maps.geometry.encoding.decodePath(step.polyline.points);
          step.start_location = new google.maps.LatLng(
            step.start_location.lat,
            step.start_location.lng,
          );
          step.end_location = new google.maps.LatLng(
            step.end_location.lat,
            step.end_location.lng,
          );
          return step;
        });
        return leg;
      });

      return response;
    });

    return serverResponse;
  }

}
