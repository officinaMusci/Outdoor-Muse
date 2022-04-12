import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { SearchRoutingModule } from './search-routing.module';
import { SearchPageComponent } from './containers/search-page/search-page.component';
import { SearchFormComponent } from './components/search-form/search-form.component';
import { SearchResultsComponent } from './components/search-results/search-results.component';
import { ReactiveFormsModule } from '@angular/forms';
import { SearchService } from './services/search/search.service';
import { SharedModule } from 'src/app/shared/shared.module';
import { IonicModule } from '@ionic/angular';
import { SearchDetailComponent } from './containers/search-detail/search-detail.component';


@NgModule({
  declarations: [
    SearchPageComponent,
    SearchFormComponent,
    SearchResultsComponent,
    SearchDetailComponent
  ],
  imports: [
    CommonModule,
    ReactiveFormsModule,
    SearchRoutingModule,
    SharedModule,
    IonicModule
  ],
  providers: [
    SearchService
  ]
})
export class SearchModule { }
