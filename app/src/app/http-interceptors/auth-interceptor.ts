import { HttpErrorResponse, HttpHandler, HttpInterceptor, HttpRequest, HttpResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { finalize, tap } from 'rxjs';
import { AuthService } from '../services/auth/auth.service';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {

  constructor(
    private readonly _auth: AuthService
  ) { }

  intercept(req: HttpRequest<any>, next: HttpHandler) {
    const started = Date.now();
    let status: number;
    
    // Get the auth token from the service
    const authToken = this._auth.getToken();

    // Clone the request and replace the original headers with
    // cloned headers, updated with the authorization
    const authReq = req.clone(authToken ? {
      headers: req.headers.set(
        'Authorization',
        `Bearer ${authToken}`
      )
    } : {});

    // Send cloned request with header to the next handler
    // and extend server response observable with logging
    return next.handle(authReq).pipe(
      tap({
        // Succeeds when there is a response; ignore other events
        next: (event:any) => (status = event instanceof HttpResponse ? event.status : 500),
        // Operation failed; error is an HttpErrorResponse
        error: (error:HttpErrorResponse) => (status = error.status)
      }),

      // Log when response observable either completes or errors
      // then redirects to login if error is 401
      finalize(() => {
        const elapsed:number = (Date.now() - started) / 1000;
        const message = `${req.method} "${req.urlWithParams}", ${status} in ${elapsed} s`;
        console.debug(message);
        
        // If 401 error, unauthenticate
        if (status === 401) {
          this._auth.unauthenticate();
        }
      })
    );
  }
}