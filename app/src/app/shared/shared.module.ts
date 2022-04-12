import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HeaderComponent } from './components/header/header.component';
import { IonicModule } from '@ionic/angular';
import { UpdatesNotificationComponent } from './components/updates-notification/updates-notification.component';
import { DistancePipe } from './pipes/distance/distance.pipe';
import { MapComponent } from './components/map/map.component';
import { GoogleMapsModule } from '@angular/google-maps';
import { StepBarComponent } from './components/step-bar/step-bar.component';
import { ReviewListComponent } from './components/review-list/review-list.component';
import { ForecastListComponent } from './components/forecast-list/forecast-list.component';
import { SolutionResumeComponent } from './components/solution-resume/solution-resume.component';
import { DurationPipe } from './pipes/duration/duration.pipe';
import { CounterPipe } from './pipes/counter/counter.pipe';
import { PartnerListComponent } from './components/partner-list/partner-list.component';
import { ToDatePipe } from './pipes/to-date/to-date.pipe';



@NgModule({
  declarations: [
    HeaderComponent,
    UpdatesNotificationComponent,
    DistancePipe,
    StepBarComponent,
    MapComponent,
    ReviewListComponent,
    ForecastListComponent,
    SolutionResumeComponent,
    DurationPipe,
    CounterPipe,
    PartnerListComponent,
    ToDatePipe
  ],
  imports: [
    CommonModule,
    IonicModule,
    GoogleMapsModule
  ],
  exports: [
    HeaderComponent,
    UpdatesNotificationComponent,
    DistancePipe,
    StepBarComponent,
    MapComponent,
    ReviewListComponent,
    ForecastListComponent,
    SolutionResumeComponent,
    DurationPipe,
    CounterPipe,
    PartnerListComponent,
    ToDatePipe
  ]
})
export class SharedModule { }
