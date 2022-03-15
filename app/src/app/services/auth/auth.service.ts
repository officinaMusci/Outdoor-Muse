import { Inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { firstValueFrom } from 'rxjs';
import { ApiResponseInterface, UserSessionDataInterface } from 'src/app/app.interfaces';
import { ApiService } from '../api/api.service';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  public userSessionData?: UserSessionDataInterface;

  constructor(
    private readonly _apiService: ApiService,
    private readonly _router: Router,
    @Inject('TOKEN_NAME') private readonly _tokenName: string,
    @Inject('ID_NAME') private readonly _idName: string
  ) { }

  async register(
    email:string,
    password:string,
    name:string
  ): Promise<boolean> {
    const response = await this._apiService.register(email, password, name);

    if (response.result && response.result.token) {
      sessionStorage.setItem(
        this._tokenName,
        response.result.token
      );

      sessionStorage.setItem(
        this._idName,
        String(response.result.id)
      );

      await this.setUserSessionData(response.result);

      return true;
    }

    return false;
  }

  getToken(): string | null {
    return sessionStorage.getItem(this._tokenName);
  }

  getId(): number | null {
    return Number(sessionStorage.getItem(this._idName));
  }

  async setUserSessionData(result?: UserSessionDataInterface): Promise<void> {
    if (result) {
      this.userSessionData = {
        id: result.id,
        email: result.email,
        name: result.name,
        points: result.points
      };
    
    } else if (this.checkAuth()) {
      const id = this.getId();

      if (id) {
        const response = await this._apiService.get<UserSessionDataInterface>('users', id);
        
        if (response.result) {
          this.userSessionData = {
            id: response.result.id,
            email: response.result.email,
            name: response.result.name,
            points: response.result.points
          };
        }
      }
    }
  }

  checkAuth(): boolean  {
    const token = this.getToken();
    const id = this.getId();

    if (token && id) {
      return true;
    
    } else {
      this.unauthenticate(false);
      return false
    }
  }

  async authenticate(
    email:string,
    password:string
  ): Promise<boolean> {
    const response = await this._apiService.authenticate(email, password);

    if (response.result && response.result.token) {
      sessionStorage.setItem(
        this._tokenName,
        response.result.token
      );

      sessionStorage.setItem(
        this._idName,
        String(response.result.id)
      );

      await this.setUserSessionData(response.result);

      return true;
    }

    return false;
  }

  unauthenticate(navigate: boolean = true): void {
    sessionStorage.removeItem(this._tokenName);
    sessionStorage.removeItem(this._idName);
    this.userSessionData = undefined;

    if (navigate) {
      this._router.navigate(['user', 'login']);
    }
  }
}
