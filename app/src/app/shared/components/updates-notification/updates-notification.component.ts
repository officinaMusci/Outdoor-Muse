import { Component } from '@angular/core';
import { SwUpdate } from '@angular/service-worker';
import { merge, Observable, of, Subject } from 'rxjs';
import { map } from 'rxjs/operators';
import { ToastOptions } from '@ionic/core';
import { ToastController } from '@ionic/angular';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-updates-notification',
  template: `
    <div *ngIf="updateAvailable$|async"></div>
  `,
})
export class UpdatesNotificationComponent {
  updateAvailable$: Observable<boolean | {}>;
  closed$ = new Subject<void>();

  constructor(
    private updates: SwUpdate,
    private _toast: ToastController
  ) {
    this.updateAvailable$ = merge(
      of(false),
      this.updates.available.pipe(
        map(async _ => await this._displayNotif()),
        map(() => true)
      ),
      this.closed$.pipe(map(() => false)),
    );
  }

  activateUpdate() {
    if (environment.production) {
      this.updates.activateUpdate().then(() => {
        location.reload();
      });
    }
  }

  private async _displayNotif() {
    const data = <ToastOptions>{
      message: 'Nouvelle mise à jour !',
      position: 'bottom',
      buttons: [
        {
          side: 'end',
          icon: 'refresh'
        }
      ]
    };

    const toast = await this._toast.create(data);
    await toast.present();
    toast.onDidDismiss()
      .then(_ => this.activateUpdate());
  }
}