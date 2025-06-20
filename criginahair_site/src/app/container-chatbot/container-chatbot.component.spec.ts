import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ContainerChatbotComponent } from './container-chatbot.component';

describe('ContainerChatbotComponent', () => {
  let component: ContainerChatbotComponent;
  let fixture: ComponentFixture<ContainerChatbotComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ContainerChatbotComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ContainerChatbotComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
