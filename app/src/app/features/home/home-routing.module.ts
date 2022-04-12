import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeDetailComponent } from './containers/home-detail/home-detail.component';
import { HomePageComponent } from './containers/home-page/home-page.component';

const routes: Routes = [
  {path: '', component: HomePageComponent},
  {path: ':id', component: HomeDetailComponent}
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class HomeRoutingModule { }
