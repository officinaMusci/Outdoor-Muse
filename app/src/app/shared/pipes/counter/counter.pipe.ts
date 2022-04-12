import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'counter'
})
export class CounterPipe implements PipeTransform {

  transform(value?: number): number[] {
    if (value) {
      return new Array(Math.round(value));
    } else {
      return [];
    }
  }

}
