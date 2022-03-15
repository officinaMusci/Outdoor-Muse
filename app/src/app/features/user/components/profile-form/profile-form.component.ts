import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { ToastController } from '@ionic/angular';
import { UserInterface, UserSessionDataInterface } from 'src/app/app.interfaces';
import { ApiService } from 'src/app/services/api/api.service';
import { AuthService } from 'src/app/services/auth/auth.service';

@Component({
  selector: 'app-profile-form',
  templateUrl: './profile-form.component.html',
  styleUrls: ['./profile-form.component.scss']
})
export class ProfileFormComponent implements OnInit {
  public profileForm!: FormGroup;

  constructor(
    public readonly authService: AuthService,
    private readonly _toastController: ToastController,
    private readonly _apiService: ApiService
  ) { }

  ngOnInit(): void {
    this.profileForm = new FormGroup({
      email: new FormControl(this.authService.userSessionData?.email || ''),
      emailRepeat: new FormControl(''),
      password: new FormControl(''),
      passwordRepeat: new FormControl(''),
      name: new FormControl(this.authService.userSessionData?.name || ''),
    });
  }

  async onSubmit(): Promise<void> {
    if (this.profileForm.valid) {
      const email = this.profileForm.get('email')?.value;
      const emailRepeat = this.profileForm.get('emailRepeat')?.value;
      const password = this.profileForm.get('password')?.value;
      const passwordRepeat = this.profileForm.get('passwordRepeat')?.value;
      const name = this.profileForm.get('name')?.value;

      if (email && email != emailRepeat) {
        const toast = await this._toastController.create({
          message: 'Les deux e-mails doivent être identiques.',
          color: 'danger',
          duration: 2000
        });
        toast.present();
      }

      if (password && password != passwordRepeat) {
        const toast = await this._toastController.create({
          message: 'Les deux mots de passe doivent être identiques.',
          color: 'danger',
          duration: 2000
        });
        toast.present();
      }

      if (
        this.authService.userSessionData
        && (email || password || name)
      ) {
        const response = await this._apiService.put<UserInterface>(
          'users',
          this.authService.userSessionData.id,
          {email, password, name}
        );

        if (response.result) {
          this.authService.userSessionData.email = response.result.email;
          this.authService.userSessionData.name = response.result.name;

          const toast = await this._toastController.create({
            message: 'Modifications sauvegardées.',
            color: 'success',
            duration: 2000
          });
          toast.present();
        }
      }
    }
  }
}
