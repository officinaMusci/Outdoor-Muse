import { InjectionToken, NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { httpInterceptorProviders } from './http-interceptors';
import { environment } from 'src/environments/environment';
import { IonicModule } from '@ionic/angular';

const TOKEN_NAME = 'TOKEN_NAME'; // new InjectionToken('TOKEN_NAME');
const ID_NAME = 'ID_NAME'; // new InjectionToken('ID_NAME');
const API_URL = 'API_URL'; // new InjectionToken('API_URL');

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    IonicModule.forRoot({
      mode: 'md'
    }),
  ],
  providers: [
    {
      provide: TOKEN_NAME,
      useValue: environment.tokenName
    },
    {
      provide: ID_NAME,
      useValue: environment.idName
    },
    {
      provide: API_URL,
      useValue: environment.apiUrl
    },
    httpInterceptorProviders
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
