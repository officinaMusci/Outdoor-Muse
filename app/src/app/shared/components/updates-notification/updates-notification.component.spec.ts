import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UpdatesNotificationComponent } from './updates-notification.component';

describe('UpdatesNotificationComponent', () => {
  let component: UpdatesNotificationComponent;
  let fixture: ComponentFixture<UpdatesNotificationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ UpdatesNotificationComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(UpdatesNotificationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
