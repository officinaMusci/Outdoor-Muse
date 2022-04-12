import { ChangeDetectionStrategy, ChangeDetectorRef, Component, Input } from '@angular/core';
import { SolutionInterface } from 'src/app/app.interfaces';
import { SearchService } from '../../services/search/search.service';

@Component({
  selector: 'app-search-results',
  templateUrl: './search-results.component.html',
  styleUrls: ['./search-results.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class SearchResultsComponent {
  @Input() public solutions: SolutionInterface[] = [];

  public length: number = 15;

  constructor(
    private readonly _searchService: SearchService,
    private readonly _cdr: ChangeDetectorRef
  ) { }

  loadData(event: any) {
    setTimeout(() => {
      event.target.complete();
      this.length += 5;

      if (this.length >= this.solutions.length) {
        event.target.disabled = true;
      }

      this._cdr.detectChanges();
    }, 500);
  }
}
