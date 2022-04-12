import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { SearchService } from '../../services/search/search.service';
import { format, utcToZonedTime } from 'date-fns-tz';
import { ToastController } from '@ionic/angular';
import { Geolocation, Position } from '@capacitor/geolocation';
import { AuthService } from 'src/app/services/auth/auth.service';
import { QueryInterface } from 'src/app/app.interfaces';

@Component({
  selector: 'app-search-form',
  templateUrl: './search-form.component.html',
  styleUrls: ['./search-form.component.scss']
})
export class SearchFormComponent implements OnInit {
  @Input() set favoriteQueries(queries: QueryInterface[]) {
    if (queries?.length) {
      this._favoriteQueries = queries;

      const lastFavoriteQuery = this._favoriteQueries.length > 0 ? this._favoriteQueries[this._favoriteQueries.length - 1] : null;
      const weather_booleans = lastFavoriteQuery ? this.getWeatherValues(lastFavoriteQuery.weather_ids) : {};

      this.searchForm.patchValue({
        location: {
          lat: lastFavoriteQuery?.location?.lat,
          lng: lastFavoriteQuery?.location?.lng
        },
        interval: {
          start: this.defaultStart,
          end: this.defaultEnd
        },
        radius: lastFavoriteQuery ? lastFavoriteQuery.radius / 1000 : 150,
        types: ['hyke'],
        max_travel: lastFavoriteQuery ? Date.parse(`1970.01.01 ${lastFavoriteQuery.max_travel as string}Z`) : 14400000,
        max_walk: lastFavoriteQuery ? Date.parse(`1970.01.01 ${lastFavoriteQuery.max_walk as string}Z`) : 7200000,
        weather_ids: {
          clear: lastFavoriteQuery ? weather_booleans['clear'] : true,
          clouds: lastFavoriteQuery ? weather_booleans['clouds'] : false,
          other: lastFavoriteQuery ? weather_booleans['other'] : false,
          rain: lastFavoriteQuery ? weather_booleans['rain'] : false,
          snow: lastFavoriteQuery ? weather_booleans['snow'] : false,
          thunderstorm: lastFavoriteQuery ? weather_booleans['thunderstorm'] : false
        },
        max_results: lastFavoriteQuery?.max_results || 10,
        language: lastFavoriteQuery?.language || 'fr'
      }, { emitEvent: false });

      this.searchForm.markAsPristine();
    }
  }

  @Output() public submitted: EventEmitter<boolean> = new EventEmitter();

  public searchForm!: FormGroup;

  public weatherList: Array<{label: string, value: string}> = [
    {label: 'Ciel dégagé', value: 'clear'},
    {label: 'Nuageux', value: 'clouds'},
    {label: 'Pluie', value: 'other'},
    {label: 'Neige', value: 'rain'},
    {label: 'Orage', value: 'snow'},
    {label: 'Autre', value: 'thunderstorm'}
  ]

  public get favoriteQueriesLength(): number {
    return this._favoriteQueries.length;
  }

  private _favoriteQueries: QueryInterface[] = [];

  private _weatherIdGroups:{[key:string]: Array<number>} = {
    'clear': [800],
    'clouds': [801, 802, 803, 804],
    'other': [300, 301, 302, 310, 311, 312, 313, 314, 321, 701, 711, 721, 731, 741, 751, 761, 762, 771, 781],
    'rain': [500, 501, 502, 503, 504, 511, 520, 521, 522, 531],
    'snow': [600, 601, 602, 611, 612, 613, 615, 616, 620, 621, 622],
    'thunderstorm': [200, 201, 202, 210, 211, 212, 221, 230, 231, 232]
  };

  private _now:Date = new Date();
  private _tomorrow:Date = new Date(this._now.setDate(this._now.getDate() + 1));

  public isLoggedIn: boolean = this._authService.checkAuth(false);
  
  public defaultStart:string = new Date(
    this._tomorrow.getFullYear(),
    this._tomorrow.getMonth(),
    this._tomorrow.getDate(),
    8, 0, 0
  ).toISOString();
  
  public defaultEnd:string = new Date(
    this._tomorrow.getFullYear(),
    this._tomorrow.getMonth(),
    this._tomorrow.getDate(),
    18, 0, 0
  ).toISOString();
  
  public minStart:string = this.defaultStart;
  public maxStart:string = new Date(this._now.setDate(this._now.getDate() + 6)).toISOString();

  public minEnd:string = this.defaultEnd;
  public maxEnd:string = new Date(this._now.setDate(this._now.getDate() + 6)).toISOString();

  constructor(
    private readonly _toastController: ToastController,
    private readonly _authService: AuthService,
    private readonly _searchService: SearchService
  ) { }

  ngOnInit(): void {
    const lastFavoriteQuery = this._favoriteQueries.length > 0 ? this._favoriteQueries[this._favoriteQueries.length - 1] : null;
    const weather_booleans = lastFavoriteQuery ? this.getWeatherValues(lastFavoriteQuery.weather_ids) : {};

    this.searchForm = new FormGroup({
      location: new FormGroup({
        lat: new FormControl(lastFavoriteQuery?.location?.lat),
        lng: new FormControl(lastFavoriteQuery?.location?.lng)
      }),
      interval: new FormGroup({
        start: new FormControl(this.defaultStart),
        end: new FormControl(this.defaultEnd)
      }),
      radius: new FormControl(lastFavoriteQuery ? lastFavoriteQuery.radius / 1000 : 150),
      types: new FormControl(['hyke']),
      max_travel: new FormControl(lastFavoriteQuery ? Date.parse(`1970.01.01 ${lastFavoriteQuery.max_travel as string}Z`) : 14400000),
      max_walk: new FormControl(lastFavoriteQuery ? Date.parse(`1970.01.01 ${lastFavoriteQuery.max_walk as string}Z`) : 7200000),
      weather_ids: new FormGroup({
        clear: new FormControl(lastFavoriteQuery ? weather_booleans['clear'] : true),
        clouds: new FormControl(lastFavoriteQuery ? weather_booleans['clouds'] : false),
        other: new FormControl(lastFavoriteQuery ? weather_booleans['other'] : false),
        rain: new FormControl(lastFavoriteQuery ? weather_booleans['rain'] : false),
        snow: new FormControl(lastFavoriteQuery ? weather_booleans['snow'] : false),
        thunderstorm: new FormControl(lastFavoriteQuery ? weather_booleans['thunderstorm'] : false)
      }),
      max_results: new FormControl(lastFavoriteQuery?.max_results || 10),
      language: new FormControl(lastFavoriteQuery?.language || 'fr')
    });
  }

  async localize(): Promise<void> {
    const currentPosition = await Geolocation.getCurrentPosition()
      .catch(() => { return; });
    
    if (currentPosition) {
      this.setLocation(currentPosition);
    
    } else {
      return;
    }
  }
  
  setLocation(position: Position): void {
    this.searchForm.get('location')?.get('lat')?.setValue(
      position.coords.latitude
    );

    this.searchForm.get('location')?.get('lng')?.setValue(
      position.coords.longitude
    );
  }

  formatDateTime(value: string): string {
    return format(
      utcToZonedTime(new Date(value), 'Europe/Zurich'),
      'Y-MM-dd HH:mm:ss.SSS'
    );
  }

  formatTimeInterval(value: string): string {
    return format(
      utcToZonedTime(new Date(value), 'UTC'),
      'H:mm:ss'
    );
  }

  createWeatherIds(list: {[key:string]: string}) {
    let weatherIds: Array<number> = [];
    Object.keys(list).forEach(key => {
      if (list[key]) {
        weatherIds = weatherIds.concat(this._weatherIdGroups[key]);
      }
    });
  
    return weatherIds;
  }

  getWeatherValues(weatherIds: number[]): {[key: string]: boolean} {
    const weatherValues: {[key: string]: boolean} = {};

    weatherIds.forEach(weatherId => {
      Object.keys(this._weatherIdGroups).forEach(key => {
        if (!weatherValues[key]) {
          weatherValues[key] = this._weatherIdGroups[key].includes(weatherId);
        }
      });
    });
    
    return weatherValues;
  }

  async saveSearchForm(): Promise<void> {
    let formValue = this.searchForm.getRawValue();

    formValue.radius = formValue.radius * 1000

    formValue.interval.start = this.formatDateTime(formValue.interval.start)
    formValue.interval.end = this.formatDateTime(formValue.interval.end)

    formValue.max_travel = this.formatTimeInterval(formValue.max_travel);
    formValue.max_walk = this.formatTimeInterval(formValue.max_walk);

    formValue.weather_ids = this.createWeatherIds(formValue.weather_ids);

    await this._searchService.saveQuery(formValue).then(async response => {
      if (response.result) {
        const toast = await this._toastController.create({
          message: 'Le formulaire de recherche a été enregistré',
          color: 'warning',
          duration: 2000
        });
        toast.present();
      }
    });
  }

  async onSubmit(): Promise<void> {
    if (this.searchForm.valid) {
      let formValue = this.searchForm.getRawValue();

      formValue.radius = formValue.radius * 1000

      formValue.interval.start = this.formatDateTime(formValue.interval.start)
      formValue.interval.end = this.formatDateTime(formValue.interval.end)

      formValue.max_travel = this.formatTimeInterval(formValue.max_travel);
      formValue.max_walk = this.formatTimeInterval(formValue.max_walk);

      formValue.weather_ids = this.createWeatherIds(formValue.weather_ids);

      this.submitted.emit(true);
      this._searchService.getSolutions(formValue);
    
    } else {
      const toast = await this._toastController.create({
        message: 'Les formulaire de recherche n\'est pas valide',
        color: 'warning',
        duration: 2000
      });
      toast.present();
    }
  }
}
