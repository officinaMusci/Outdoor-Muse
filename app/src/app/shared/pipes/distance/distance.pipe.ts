import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'distance'
})
export class DistancePipe implements PipeTransform {

  transform(value: number, unit: string): string {
    switch(unit) {
      case 'km':
        return `${value / 1000} km`;
      
      case 'm':
      default:
        return `${value} m`;
    }
  }

}
