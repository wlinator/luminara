import { Component } from '@angular/core';
import { LoginButtonComponent } from '../login-button/login-button.component';
import { HomeWidgetComponent } from '../home-widget/home-widget.component';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [LoginButtonComponent, HomeWidgetComponent],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent {
  title = 'Luminara';
}
