import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { Router } from '@angular/router';
import { ToastController } from '@ionic/angular';
import { AuthService } from 'src/app/services/auth/auth.service';

@Component({
  selector: 'app-registration-form',
  templateUrl: './registration-form.component.html',
  styleUrls: ['./registration-form.component.scss']
})
export class RegistrationFormComponent implements OnInit {
  public registrationForm!: FormGroup;

  constructor(
    private readonly _authService: AuthService,
    private readonly _toastController: ToastController,
    private readonly _router: Router
  ) { }

  ngOnInit(): void {
    this.registrationForm = new FormGroup({
      email: new FormControl(''),
      password: new FormControl(''),
      name: new FormControl(''),
    });
  }

  async onSubmit(): Promise<void> {
    if (this.registrationForm.valid) {
      const email = this.registrationForm.get('email')?.value;
      const password = this.registrationForm.get('password')?.value;
      const name = this.registrationForm.get('name')?.value;

      if (email && password && name) {
        const isAuthenticated = await this._authService.register(email, password, name);

        if (isAuthenticated) {
          this._router.navigate(['/']);

          const toast = await this._toastController.create({
            message: 'Bienvenue chez Outdoor Muse !',
            color: 'success',
            duration: 2000
          });
          toast.present();
        
        } else {
          const toast = await this._toastController.create({
            message: 'Identifiants non valides.',
            color: 'danger',
            duration: 2000
          });
          toast.present();
        } 
      }
    
    } else {
      const toast = await this._toastController.create({
        message: 'Veuillez renseigner toutes les données.',
        color: 'warning',
        duration: 2000
      });
      toast.present();
    }
  }
}
