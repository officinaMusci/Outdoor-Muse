import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ProtectedGuard } from 'src/app/guards/protected/protected.guard';
import { UnauthenticatedGuard } from 'src/app/guards/unauthenticated/unauthenticated.guard';
import { LoginPageComponent } from './containers/login-page/login-page.component';
import { ProfilePageComponent } from './containers/profile-page/profile-page.component';
import { RegisterPageComponent } from './containers/register-page/register-page.component';

const routes: Routes = [
  {path: '', redirectTo: 'profile', pathMatch: 'full'},
  {path: 'register', component: RegisterPageComponent, canActivate: [UnauthenticatedGuard]},
  {path: 'login', component: LoginPageComponent, canActivate: [UnauthenticatedGuard]},
  {path: 'profile', component: ProfilePageComponent, canActivate: [ProtectedGuard]}
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class UserRoutingModule { }
