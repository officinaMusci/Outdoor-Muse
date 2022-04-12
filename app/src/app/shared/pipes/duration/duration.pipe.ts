import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'duration'
})
export class DurationPipe implements PipeTransform {

  transform(value: string | undefined, format: string, total?: string): string {
    if (value) {
      if (
        format === 'percentage'
        && total
      ) {
        return `${this.getTimePercentage(value, total)}%`;
      
      } else if (format === 'HH:MM') {
        let seconds = this.totalSeconds(value);
        let hours = Math.floor(seconds / 3600);
        let minutes = Math.floor((seconds % 3600) / 60);

        return [
          (format.includes('HH') && hours < 10 ? '0' : '') + hours,
          (format.includes('MM') && minutes < 10 ? '0' : '') + minutes
        ].join(':');
      }
    }

    return String(value);
  }

  totalSeconds(time: string): number {
    let parts = time.split(':');
    return Number(parts[0]) * 3600 + Number(parts[1]) * 60 + Number(parts[2]);
  }

  getTimePercentage(duration: string, total: string): number {
    return 100 * this.totalSeconds(duration) / this.totalSeconds(total);
  }

}
