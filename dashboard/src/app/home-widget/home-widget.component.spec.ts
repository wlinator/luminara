import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HomeWidgetComponent } from './home-widget.component';

describe('HomeWidgetComponent', () => {
  let component: HomeWidgetComponent;
  let fixture: ComponentFixture<HomeWidgetComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [HomeWidgetComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(HomeWidgetComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
