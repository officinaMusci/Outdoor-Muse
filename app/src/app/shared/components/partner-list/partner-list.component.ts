import { Component, Input, OnInit } from '@angular/core';
import { PartnerInterface } from 'src/app/app.interfaces';

@Component({
  selector: 'app-partner-list',
  templateUrl: './partner-list.component.html',
  styleUrls: ['./partner-list.component.scss']
})
export class PartnerListComponent implements OnInit {
  @Input() public partners: PartnerInterface[] = [];

  constructor() { }

  ngOnInit(): void {
  }

}
