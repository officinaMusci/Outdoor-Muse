import { Component, Input, OnInit } from '@angular/core';
import { SolutionInterface } from 'src/app/app.interfaces';

@Component({
  selector: 'app-solution-resume',
  templateUrl: './solution-resume.component.html',
  styleUrls: ['./solution-resume.component.scss']
})
export class SolutionResumeComponent implements OnInit {
  @Input() solution?: SolutionInterface;

  constructor() { }

  ngOnInit(): void {
  }

}
