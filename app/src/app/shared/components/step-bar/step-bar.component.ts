import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-step-bar',
  templateUrl: './step-bar.component.html',
  styleUrls: ['./step-bar.component.scss']
})
export class StepBarComponent implements OnInit {
  @Input() public outwardTravelDuration:string = '00:00:00';
  @Input() public outwardWalkDuration:string = '00:00:00';
  @Input() public destinationDuration:string = '00:00:00';
  @Input() public freeTimeDuration:string = '00:00:00';
  @Input() public returnWalkDuration:string = '00:00:00';
  @Input() public returnTravelDuration:string = '00:00:00';
  @Input() public totalTripDuration:string = '00:00:00';

  constructor() { }

  ngOnInit(): void {
  }
}