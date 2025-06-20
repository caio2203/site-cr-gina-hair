import { Component } from '@angular/core';

@Component({
  selector: 'app-container-chatbot',
  standalone: true,
  imports: [],
  templateUrl: './container-chatbot.component.html',
  styleUrl: './container-chatbot.component.css'
})
export class ContainerChatbotComponent {
  showChatbot = false;

  openChatbot() {
    this.showChatbot = true;
  }

  closeChatbot() {
    this.showChatbot = false;
  }
}
