import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SolutionResumeComponent } from './solution-resume.component';

describe('SolutionResumeComponent', () => {
  let component: SolutionResumeComponent;
  let fixture: ComponentFixture<SolutionResumeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SolutionResumeComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SolutionResumeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
