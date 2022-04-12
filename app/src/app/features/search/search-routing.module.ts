import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SearchDetailComponent } from './containers/search-detail/search-detail.component';
import { SearchPageComponent } from './containers/search-page/search-page.component';

const routes: Routes = [
  {path: '', component: SearchPageComponent},
  {path: ':id', component: SearchDetailComponent}
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class SearchRoutingModule { }
