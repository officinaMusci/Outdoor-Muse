import { Component, Input, OnInit } from '@angular/core';
import { ForecastInterface } from 'src/app/app.interfaces';

@Component({
  selector: 'app-forecast-list',
  templateUrl: './forecast-list.component.html',
  styleUrls: ['./forecast-list.component.scss']
})
export class ForecastListComponent implements OnInit {
  @Input() forecasts: ForecastInterface[] = [];

  constructor() { }

  ngOnInit(): void {
  }

}
