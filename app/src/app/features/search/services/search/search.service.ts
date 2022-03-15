import { Injectable } from '@angular/core';
import { QueryInterface, SolutionInterface } from 'src/app/app.interfaces';
import { ApiService } from 'src/app/services/api/api.service';

@Injectable()
export class SearchService {
  public solutions: SolutionInterface[] = [];

  constructor(
    private readonly _apiService: ApiService
  ) { }

  getSolutions(query: QueryInterface):void {
    this._apiService.getSolutions(query).then(response => {
      if (response.result) {
        this.solutions = response.result
      }
    });
  }
}
