import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { HomeRoutingModule } from './home-routing.module';
import { SharedModule } from 'src/app/shared/shared.module';
import { IonicModule } from '@ionic/angular';
import { HomePageComponent } from './containers/home-page/home-page.component';
import { HomeDetailComponent } from './containers/home-detail/home-detail.component';
import { HomeSolutionsComponent } from './components/home-solutions/home-solutions.component';


@NgModule({
  declarations: [
    HomePageComponent,
    HomeDetailComponent,
    HomeSolutionsComponent
  ],
  imports: [
    CommonModule,
    HomeRoutingModule,
    SharedModule,
    IonicModule
  ]
})
export class HomeModule { }
