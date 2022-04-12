import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { firstValueFrom, map, Observable } from 'rxjs';
import { PartnerInterface, ReviewInterface, SolutionInterface } from 'src/app/app.interfaces';
import { ApiService } from 'src/app/services/api/api.service';
import { AuthService } from 'src/app/services/auth/auth.service';
import { SearchService } from '../../services/search/search.service';

@Component({
  selector: 'app-search-detail',
  templateUrl: './search-detail.component.html',
  styleUrls: ['./search-detail.component.scss']
})
export class SearchDetailComponent {
  private readonly id: number = Number(this._activatedRoute.snapshot.params['id']);

  public solution$: Observable<SolutionInterface | undefined> = this._searchService.solutions$.pipe(
    map(solutions => solutions.find(solution => solution.id === this.id))
  );

  public isLoggedIn: boolean = this._authService.checkAuth(false);

  public accordionGroupValues: string[] = [];
  public partners: PartnerInterface[] = [];
  public reviews: ReviewInterface[] = [];

  constructor(
    private readonly _activatedRoute: ActivatedRoute,
    private readonly _router: Router,
    private readonly _authService: AuthService,
    private readonly _searchService: SearchService,
    private readonly _apiService: ApiService
  ) { }

  ionViewWillEnter(): void {
    if (!this._searchService.isUsed) {
      this._router.navigate(['/search']);
    } else {
      firstValueFrom(this.solution$).then(solution => {
        this._apiService.get<ReviewInterface[]>('reviews/place', solution?.place_id).then(response => {
          if (response.result) {
            this.reviews = response.result;
          }
        });
        this._apiService.get<PartnerInterface[]>('partners/solution', solution?.id).then(response => {
          if (response.result) {
            this.partners = response.result;
          }
        });
      });
    }
  }

  setAccordionGroupValue($event: any) {
    this.accordionGroupValues.push($event.detail.value);
  }

  selectSolution(id: number): void {
    this._searchService.selectSolution(id).then(() => {
      this._router.navigate(['/']);
    });
  }
  
  unselectSolution(id: number): void {
    this._searchService.unselectSolution(id).then(() => {
      this._router.navigate(['/']);
    });
  }
}
