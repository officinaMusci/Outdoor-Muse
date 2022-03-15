import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { Router } from '@angular/router';
import { ToastController } from '@ionic/angular';
import { AuthService } from 'src/app/services/auth/auth.service';

@Component({
  selector: 'app-login-form',
  templateUrl: './login-form.component.html',
  styleUrls: ['./login-form.component.scss']
})
export class LoginFormComponent implements OnInit {
  public loginForm!: FormGroup;

  constructor(
    private readonly _authService: AuthService,
    private readonly _toastController: ToastController,
    private readonly _router: Router
  ) { }

  ngOnInit(): void {
    this.loginForm = new FormGroup({
      email: new FormControl(''),
      password: new FormControl('')
    });
  }

  async onSubmit(): Promise<void> {
    if (this.loginForm.valid) {
      const email = this.loginForm.get('email')?.value;
      const password = this.loginForm.get('password')?.value;

      if (email && password) {
        try {
          const isAuthenticated = await this._authService.authenticate(email, password);

          if (isAuthenticated) {
            this._router.navigate(['/']);
            
            const toast = await this._toastController.create({
              message: 'Bon retour chez Outdoor Muse !',
              color: 'success',
              duration: 2000
            });
            toast.present();
          }
        
        } catch (e) {
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
        message: 'Veuillez renseigner vos identifiants.',
        color: 'warning',
        duration: 2000
      });
      toast.present();
    }
  }
}
