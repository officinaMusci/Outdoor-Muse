import { Inject, Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { firstValueFrom } from 'rxjs';
import { ApiResponseInterface, QueryInterface, SolutionInterface, UserSessionDataInterface } from 'src/app/app.interfaces';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  constructor(
    private readonly _http: HttpClient,
    @Inject('API_URL') private readonly _apiUrl: string
  ) { }

  composeHeaders():HttpHeaders {
    const headers = new HttpHeaders({
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    });

    return headers;
  }

  async post<T>(
    entity:string,
    body:object
  ): Promise<ApiResponseInterface<T>> {
    const request = this._http.post<ApiResponseInterface<T>>(
      `${this._apiUrl}/${entity}`,
      body,
      {headers: this.composeHeaders()}
    );
    const response = await firstValueFrom(request);
    
    return response;
  }

  async get<T>(
    entity:string,
    id?:number
  ): Promise<ApiResponseInterface<T>> {
    const request = this._http.get<ApiResponseInterface<T>>(
      `${this._apiUrl}/${entity}` + (id ? `/${id}` : ''),
      {headers: this.composeHeaders()}
    );
    const response = await firstValueFrom(request);
    
    return response;
  }

  async put<T>(
    entity:string,
    id:number,
    body:object
  ): Promise<ApiResponseInterface<T>> {
    const request = this._http.put<ApiResponseInterface<T>>(
      `${this._apiUrl}/${entity}/${id}`,
      body,
      {headers: this.composeHeaders()}
    );
    const response = await firstValueFrom(request);
    
    return response;
  }

  async delete<T>(
    entity:string,
    id:number
  ): Promise<ApiResponseInterface<T>> {
    const request = this._http.delete<ApiResponseInterface<T>>(
      `${this._apiUrl}/${entity}/${id}`,
      {headers: this.composeHeaders()}
    );
    const response = await firstValueFrom(request);
    
    return response;
  }

  async register(
    email:string,
    password:string,
    name:string
  ): Promise<ApiResponseInterface<UserSessionDataInterface>> {
    const request = this._http.post<ApiResponseInterface<UserSessionDataInterface>>(
      `${this._apiUrl}/auth/register`,
      {email, password, name},
      {headers: this.composeHeaders()}
    );
    const response = await firstValueFrom(request);
    
    return response;
  }

  async authenticate(
    email:string,
    password:string
  ): Promise<ApiResponseInterface<UserSessionDataInterface>> {
    const request = this._http.post<ApiResponseInterface<UserSessionDataInterface>>(
      `${this._apiUrl}/auth/login`,
      {email, password},
      {headers: this.composeHeaders()}
    );
    const response = await firstValueFrom(request);
    
    return response;
  }

  async getSolutions(
    query: QueryInterface
  ): Promise<ApiResponseInterface<SolutionInterface[]>> {
    const request = this._http.post<ApiResponseInterface<SolutionInterface[]>>(
      `${this._apiUrl}/search`,
      query,
      {headers: this.composeHeaders()}
    );
    const response = await firstValueFrom(request);
    
    return response;
  }
}
