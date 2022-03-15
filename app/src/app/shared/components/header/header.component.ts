import { DOCUMENT } from '@angular/common';
import { Component, Inject, Input, OnInit } from '@angular/core';
import { IonButton } from '@ionic/angular';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent implements OnInit {
  @Input() public hasBackButton: boolean = false;
  @Input() public defaultHref: string = '';
  @Input() public title: string = '';
  @Input() public buttons:IonButton[] = []

  constructor(
    @Inject(DOCUMENT) private readonly _document: Document
  ) { }

  ngOnInit(): void {
  }
}
