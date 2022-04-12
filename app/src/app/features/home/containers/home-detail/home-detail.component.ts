import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { AlertController, ToastController } from '@ionic/angular';
import { PartnerInterface, ReviewInterface, SolutionInterface } from 'src/app/app.interfaces';
import { ApiService } from 'src/app/services/api/api.service';
import { AuthService } from 'src/app/services/auth/auth.service';

@Component({
  selector: 'app-home-detail',
  templateUrl: './home-detail.component.html',
  styleUrls: ['./home-detail.component.scss']
})
export class HomeDetailComponent implements OnInit {
  private readonly id: number = Number(this._activatedRoute.snapshot.params['id']);

  public solution?: SolutionInterface;

  public now = new Date();
  public accordionGroupValues: string[] = [];
  public reviews: ReviewInterface[] = [];
  public hasRewiew: boolean = false;
  public partners: PartnerInterface[] = [];
  
  public reviewForm!: FormGroup;

  constructor(
    private readonly _activatedRoute: ActivatedRoute,
    private readonly _router: Router,
    private readonly _toastController: ToastController,
    private readonly _alertCtrl: AlertController,
    private readonly _apiService: ApiService,
    private readonly _authService: AuthService
  ) { }

  ngOnInit(): void {
    this.reviewForm = new FormGroup({
      comment: new FormControl(''),
      rating: new FormControl(5),
      place_id: new FormControl(this.solution?.place_id)
    });
  }

  ionViewWillEnter(): void {
    this._apiService.get<SolutionInterface>('solutions', this.id).then(response => {
      this.solution = response.result;
      this.reviewForm.get('place_id')?.setValue(response.result?.place_id);

      if (!this.solution) {
        this._router.navigate(['/']);
      } else {
        this._apiService.get<ReviewInterface[]>('reviews/place', this.solution.place_id).then(response => {
          if (response.result) {
            this.reviews = response.result;

            if (this.reviews.filter(review => review.user_id === this._authService.userSessionData?.id).length > 0) {
              this.hasRewiew = true;
              this.reviewForm.disable();
            }
          }
        });
        this._apiService.get<PartnerInterface[]>('partners/solution', this.solution.id).then(response => {
          if (response.result) {
            this.partners = response.result;
          }
        });
      }
    });
  }

  setAccordionGroupValue($event: any) {
    this.accordionGroupValues.push($event.detail.value);
  }

  async openReviewModal(): Promise<void> {
    await this.reviewModal();

    if (this.reviewForm.get('comment')?.value !== '') {
      const formData = this.reviewForm.value;

      await this._apiService.post('reviews', formData);
      const toast = await this._toastController.create({
        message: 'Votre avis a été enregistré',
        color: 'success',
        duration: 2000
      });
      toast.present();
  
      this.hasRewiew = true;
      this.reviewForm.reset();

      if (this.solution) {
        this._apiService.get<ReviewInterface[]>('reviews/place', this.solution.place_id).then(response => {
          if (response.result) {
            this.reviews = response.result;
          }
        });
      }
    
    } else {
      const toast = await this._toastController.create({
        message: 'Votre avis n\'etait pas valide',
        color: 'warning',
        duration: 2000
      });
      toast.present();
    }
  }

  async reviewModal() {
    const alert = await this._alertCtrl.create({
      header: 'Écrire un avis',
      inputs: [
        {
          label: 'Commentaire',
          name: 'comment',
          value: this.reviewForm.get('comment')?.value,
          type: 'textarea'
        },
        {
          label: 'Note',
          name: 'rating',
          value: this.reviewForm.get('rating')?.value,
          type: 'number',
          min: 1,
          max: 5
        }
      ],
      buttons: [
        {
          text: 'Annuler',
          role: 'cancel',
          cssClass: 'secondary',
          handler: () => {}
        }, {
          text: 'Confirmer',
          handler: inputs => {
            this.reviewForm.get('comment')?.setValue(inputs.comment);
            this.reviewForm.get('rating')?.setValue(inputs.rating);
          }
        }
      ]
    });

    await alert.present();
    await alert.onDidDismiss();
  }

  removeSolution(id: number): void {
    this._apiService.delete<boolean>('search/select', id).then(() => {
      this._router.navigate(['/']);
    });
  }
}
