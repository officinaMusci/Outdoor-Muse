import { Component, OnInit } from '@angular/core';
import { AuthService } from './services/auth/auth.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  title = 'app';

  constructor(
    private readonly _authService: AuthService
  ) { }

  async ngOnInit(): Promise<void> {
    if (!this._authService.userSessionData) {
      await this._authService.setUserSessionData();
    }
  }
}
