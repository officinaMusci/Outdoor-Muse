import { ChangeDetectorRef, Component, Input, OnInit } from '@angular/core';
import { ReviewInterface, SolutionInterface } from 'src/app/app.interfaces';
import { ApiService } from 'src/app/services/api/api.service';

@Component({
  selector: 'app-home-solutions',
  templateUrl: './home-solutions.component.html',
  styleUrls: ['./home-solutions.component.scss']
})
export class HomeSolutionsComponent {
  @Input() public solutions: SolutionInterface[] = [];
  @Input() public userReviews: {[place_id: number]: ReviewInterface} = {};

  public now = new Date();
  public length: number = 15;


  constructor(
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
