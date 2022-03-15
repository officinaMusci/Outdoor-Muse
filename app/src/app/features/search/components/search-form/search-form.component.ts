import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { SearchService } from '../../services/search/search.service';
import { format, parseISO } from 'date-fns';

@Component({
  selector: 'app-search-form',
  templateUrl: './search-form.component.html',
  styleUrls: ['./search-form.component.scss']
})
export class SearchFormComponent implements OnInit {
  public searchForm!: FormGroup;

  private _now = new Date();
  private _tomorrow = new Date(this._now.setDate(this._now.getDate() + 1));
  private _defaultStart = new Date(this._tomorrow.getFullYear(), this._tomorrow.getMonth(), this._tomorrow.getDate(), 8, 0, 0);
  private _defaultEnd = new Date(this._tomorrow.getFullYear(), this._tomorrow.getMonth(), this._tomorrow.getDate(), 18, 0, 0);

  constructor(
    private readonly _searchService: SearchService
  ) { }

  ngOnInit(): void {
    this.searchForm = new FormGroup({
      location: new FormGroup({
        lat: new FormControl(),
        lng: new FormControl()
      }),
      interval: new FormGroup({
        start: new FormControl(this.formatDate(this._defaultStart.toISOString())),
        end: new FormControl(this.formatDate(this._defaultEnd.toISOString()))
      }),
      radius: new FormControl(150),
      types: new FormControl(['hyke']),
      max_travel: new FormControl(300000),
      max_walk: new FormControl(300000),
      weather_ids: new FormGroup({
        clear: new FormControl(false),
        clouds: new FormControl(false),
        other: new FormControl(false),
        rain: new FormControl(false),
        snow: new FormControl(false),
        thunderstorm: new FormControl(false)
      }),
      max_results: new FormControl(10),
      language: new FormControl('fr')
    });
  }

  localize() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position: GeolocationPosition) => this.setLocation(position)
      );
    }
  }
  
  setLocation(position: GeolocationPosition) {
    this.searchForm.get('location')?.get('lat')?.setValue(
      position.coords.latitude
    );

    this.searchForm.get('location')?.get('lng')?.setValue(
      position.coords.longitude
    );
  }

  formatDate(value: string | null | undefined) {
    if (value)  {
      return format(parseISO(value), 'dd.MM.Y, HH:mm');
    } else {
      return value;
    }
  }

  onSubmit(): void {console.log(this.searchForm.value)
    //if (this.searchForm.valid) {
    //  this._searchService.getSolutions(this.searchForm.value);
    //}
  }
}
