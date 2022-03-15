import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { UserRoutingModule } from './user-routing.module';
import { RegisterPageComponent } from './containers/register-page/register-page.component';
import { LoginPageComponent } from './containers/login-page/login-page.component';
import { ProfilePageComponent } from './containers/profile-page/profile-page.component';
import { PlacesPageComponent } from './containers/places-page/places-page.component';
import { ReviewsPageComponent } from './containers/reviews-page/reviews-page.component';
import { ReactiveFormsModule } from '@angular/forms';
import { SharedModule } from 'src/app/shared/shared.module';
import { IonicModule } from '@ionic/angular';
import { LoginFormComponent } from './components/login-form/login-form.component';
import { RegistrationFormComponent } from './components/registration-form/registration-form.component';
import { ProfileFormComponent } from './components/profile-form/profile-form.component';


@NgModule({
  declarations: [
    RegisterPageComponent,
    LoginPageComponent,
    ProfilePageComponent,
    PlacesPageComponent,
    ReviewsPageComponent,
    LoginFormComponent,
    RegistrationFormComponent,
    ProfileFormComponent
  ],
  imports: [
    CommonModule,
    ReactiveFormsModule,
    UserRoutingModule,
    SharedModule,
    IonicModule
  ]
})
export class UserModule { }
