import { InjectionToken, NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { httpInterceptorProviders } from './http-interceptors';
import { environment } from 'src/environments/environment';
import { IonicModule } from '@ionic/angular';
import { ServiceWorkerModule } from '@angular/service-worker';
import { SharedModule } from './shared/shared.module';

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
    SharedModule,
    IonicModule.forRoot({
      mode: 'md'
    }),
    ServiceWorkerModule.register('ngsw-worker.js', {
      enabled: environment.production,
      // Register the ServiceWorker as soon as the application is stable
      // or after 30 seconds (whichever comes first).
      registrationStrategy: 'registerWhenStable:30000'
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
