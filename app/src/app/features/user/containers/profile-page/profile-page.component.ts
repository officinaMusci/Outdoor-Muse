import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AlertController, ToastController } from '@ionic/angular';
import { ApiService } from 'src/app/services/api/api.service';
import { AuthService } from 'src/app/services/auth/auth.service';

@Component({
  selector: 'app-profile-page',
  templateUrl: './profile-page.component.html',
  styleUrls: ['./profile-page.component.scss']
})
export class ProfilePageComponent implements OnInit {

  constructor(
    private readonly _apiService: ApiService,
    private readonly _authService: AuthService,
    private readonly _toastController: ToastController,
    private readonly _alertController: AlertController,
    private readonly _router: Router
  ) { }

  ngOnInit(): void {
  }

  unauthenticate(): void {
    this._authService.unauthenticate();
  }

  async deleteAccount(): Promise<void> {
    const alert = await this._alertController.create({
      header: 'Êtes-vous super sûr ?',
      message: 'Vous perdrez toutes vos données.',
      inputs: [
        {
          name: 'confirmationText',
          placeholder: '"Oui, je suis super sûr"',
          type: 'text'
        }
      ],
      buttons: [
        {
          text: 'Annuler',
          role: 'cancel',
          handler: async () => {
            const toast = await this._toastController.create({
              message: 'Ouf ! On y croyait presque !',
              color: 'success',
              duration: 2000
            });
            toast.present();
          }
        }, {
          text: 'Confirmer',
          role: 'destructive',
          handler: async inputs => {
            const id = this._authService.getId();
            if (id && inputs.confirmationText === 'Oui, je suis super sûr') {
              const response = await this._apiService.delete('users', id);

              if (response.result) {
                const toast = await this._toastController.create({
                  message: 'Votre compte a bien été désintégré',
                  color: 'success',
                  duration: 2000
                });
                toast.present();
                this._authService.unauthenticate(false);
                this._router.navigate(['/']);
              
              } else {
                const toast = await this._toastController.create({
                  message: 'Notre serveur a des soucis...',
                  color: 'danger',
                  duration: 2000
                });
                toast.present();
              }
            
            } else {
              const toast = await this._toastController.create({
                message: 'Ah-ah-ah ! Vous n\'avez pas dit le mot magique !',
                color: 'warning',
                duration: 2000
              });
              toast.present();
            }
          }
        }
      ]
    });

    await alert.present();
    await alert.onDidDismiss();
  }
}
