import { Component, OnInit } from '@angular/core';
import { ToastController } from '@ionic/angular';
import { AuthService } from './services/auth/auth.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  title = 'app';

  constructor(
    private readonly _authService: AuthService,
    private readonly _toastController: ToastController
  ) { }

  async ngOnInit(): Promise<void> {
    //this.showInstallToast();

    if (!this._authService.userSessionData) {
      await this._authService.setUserSessionData();
    }
  }

  async showInstallToast(platform = null): Promise<void> {
    // Detects if device is on iOS 
    const isIos = () => {
      const userAgent = platform || window.navigator.userAgent.toLowerCase();
      return /iphone|ipad|ipod/.test(userAgent);
    }

    // Detects if device is in standalone mode
    const isInStandaloneMode = () => (
      'standalone' in (window as any).navigator)
      && ((window as any).navigator.standalone
    );
    
    // Checks if should display install popup notification
    if (isIos() && !isInStandaloneMode()) {
      const toast = await this._toastController.create({
        message: 'AdditiveFinder is not installed. Please install it by click to ....',
      });

      await toast.present();
    }
  }
}
