import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ReviewInterface, SolutionInterface } from 'src/app/app.interfaces';
import { ApiService } from 'src/app/services/api/api.service';
import { AuthService } from 'src/app/services/auth/auth.service';

@Component({
  selector: 'app-home-page',
  templateUrl: './home-page.component.html',
  styleUrls: ['./home-page.component.scss']
})
export class HomePageComponent {
  public isLoggedIn: boolean = this._authService.checkAuth(false);

  public user = this._authService.userSessionData;
  public solutions: SolutionInterface[] = [];
  public userReviews: {[place_id: number]: ReviewInterface} = {};

  constructor(
    private readonly _authService: AuthService,
    private readonly _apiService: ApiService
  ) { }

  ionViewWillEnter(): void {
    if (this.isLoggedIn) {
      this._apiService.get<SolutionInterface[]>('search/fetch').then(response => {
        if (response.result) {
          this.solutions = response.result;

          this.solutions.forEach(solution => {
            if (solution.place_id) {
              let place_id = solution.place_id;
              this._apiService.get<ReviewInterface | undefined>('reviews/user_place', place_id)
                .then(response => {
                  if (response.result) {
                    this.userReviews[place_id] = response.result;
                  } 
                })
            }
          });
        }
      });
    }
  }

}
