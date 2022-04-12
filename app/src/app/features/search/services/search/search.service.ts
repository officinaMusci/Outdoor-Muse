import { Injectable } from '@angular/core';
import { LoadingController } from '@ionic/angular';
import { BehaviorSubject, Observable } from 'rxjs';
import { ApiResponseInterface, QueryInterface, SolutionInterface } from 'src/app/app.interfaces';
import { ApiService } from 'src/app/services/api/api.service';

@Injectable()
export class SearchService {
  private _solutions$: BehaviorSubject<SolutionInterface[]> = new BehaviorSubject([] as SolutionInterface[]);
  public readonly solutions$: Observable<SolutionInterface[]> = this._solutions$.asObservable();

  private _favoriteQueries$: BehaviorSubject<QueryInterface[]> = new BehaviorSubject([] as QueryInterface[]);
  public readonly favoriteQueries$: Observable<QueryInterface[]> = this._favoriteQueries$.asObservable();
  
  public isUsed: boolean = false;

  constructor(
    private readonly _loadingController: LoadingController,
    private readonly _apiService: ApiService
  ) { }

  async saveQuery(query: QueryInterface): Promise<ApiResponseInterface<boolean>> {
    return await this._apiService.post<boolean>(`search/save`, query).then(response => {
      return response;
    });
  }

  async getSolutions(query: QueryInterface): Promise<void> {
    this._solutions$.next([]);
    
    const loading = await this._loadingController.create();
    await loading.present();

    this._apiService.getSolutions(query)
    .then(response => {
      if (response.result) {
        this._solutions$.next(response.result);
      }
    }).finally(() => {
      this._loadingController.dismiss();
      this.isUsed = true;
    });
  }

  async getFavoriteQueries(): Promise<void> {
    this._solutions$.next([]);
    
    this._apiService.get<QueryInterface[]>('search/favorites')
    .then(response => {
      if (response.result) {
        this._favoriteQueries$.next(response.result);
      }
    });
  }

  async selectSolution(id: number): Promise<void> {
    await this._apiService.post<boolean>(`search/select/${id}`, {}).then(response => {
      return response.result;
    });
  }

  async unselectSolution(id: number): Promise<void> {
    await this._apiService.delete<boolean>(`search/select`, id).then(response => {
      return response.result;
    });
  }
}
