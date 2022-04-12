import { Component, Input, OnInit } from '@angular/core';
import { ReviewInterface } from 'src/app/app.interfaces';

@Component({
  selector: 'app-review-list',
  templateUrl: './review-list.component.html',
  styleUrls: ['./review-list.component.scss']
})
export class ReviewListComponent implements OnInit {
  @Input() public reviews: ReviewInterface[] = [];

  constructor() { }

  ngOnInit(): void {
  }
}
