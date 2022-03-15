import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, CanActivate, Router, RouterStateSnapshot, UrlTree } from '@angular/router';
import { Observable } from 'rxjs';
import { AuthService } from 'src/app/services/auth/auth.service';

@Injectable({
  providedIn: 'root'
})
export class ProtectedGuard implements CanActivate {
  constructor(
    private readonly _authService: AuthService,
    private readonly _router: Router
  ) { }

  canActivate(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ): Observable<boolean | UrlTree> | Promise<boolean | UrlTree> | boolean | UrlTree {
    
    const isAuthenticated = this._authService.checkAuth();

    if (!isAuthenticated) {
      this._router.navigate(['user', 'login']);
    }

    return isAuthenticated;
  }
}
