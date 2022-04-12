import { Component, ViewChild } from '@angular/core';
import { IonAccordionGroup } from '@ionic/angular';
import { firstValueFrom, Observable } from 'rxjs';
import { QueryInterface, SolutionInterface } from 'src/app/app.interfaces';
import { AuthService } from 'src/app/services/auth/auth.service';
import { SearchService } from '../../services/search/search.service';

@Component({
  selector: 'app-search-page',
  templateUrl: './search-page.component.html',
  styleUrls: ['./search-page.component.scss']
})
export class SearchPageComponent {
  @ViewChild(IonAccordionGroup, { static: true }) accordionGroup!: IonAccordionGroup;
  
  public solutions$: Observable<SolutionInterface[]> = this._searchService.solutions$;
  public favoriteQueries$: Observable<QueryInterface[]> = this._searchService.favoriteQueries$;

  constructor(
    private readonly _authService: AuthService,
    private readonly _searchService: SearchService
  ) { }

  ionViewWillEnter(): void {
    if (this._authService.checkAuth(false)) {
      this._searchService.getFavoriteQueries();
    }

    firstValueFrom(this.solutions$).then(solutions => {
      if (solutions.length > 0) {
        this.accordionGroup.value = 'results';
      }
    });
  }

  toggleAccordion() {
    if (this.accordionGroup.value === 'form') {
      this.accordionGroup.value = 'results';
      
    } else {
      this.accordionGroup.value = 'form';

    }
  }
}
