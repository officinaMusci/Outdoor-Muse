import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

const routes: Routes = [
  {path: '', redirectTo: 'home', pathMatch: 'full'},
  {
    path: 'home',
    loadChildren: () => 
      import('./features/home/home.module')
      .then(m => m.HomeModule)
  },
  {
    path: 'search',
    loadChildren: () => 
      import('./features/search/search.module')
      .then(m => m.SearchModule)
  },
  {
    path: 'user',
    loadChildren: () => 
      import('./features/user/user.module')
      .then(m => m.UserModule)
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
