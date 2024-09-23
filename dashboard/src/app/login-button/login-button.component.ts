import { Component } from '@angular/core';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { faDiscord } from '@fortawesome/free-brands-svg-icons';

@Component({
  selector: 'app-login-button',
  standalone: true,
  imports: [FontAwesomeModule],
  templateUrl: './login-button.component.html',
  styleUrl: './login-button.component.css'
})
export class LoginButtonComponent {
  faDiscord = faDiscord;
}
