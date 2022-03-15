import { Component, OnInit } from '@angular/core';
import { SolutionInterface } from 'src/app/app.interfaces';
import { SearchService } from '../../services/search/search.service';

@Component({
  selector: 'app-search-results',
  templateUrl: './search-results.component.html',
  styleUrls: ['./search-results.component.scss']
})
export class SearchResultsComponent implements OnInit {
  public readonly solutions: SolutionInterface[] = this._searchService.solutions;

  constructor(
    private readonly _searchService: SearchService
  ) { }

  ngOnInit(): void {
  }

}
