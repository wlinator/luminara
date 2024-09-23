import { Component, Input } from '@angular/core';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { faGavel, faSlidersH, faCode, faLevelUpAlt, faCoins, faSmile } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-home-widget',
  standalone: true,
  imports: [FontAwesomeModule],
  templateUrl: './home-widget.component.html',
  styleUrl: './home-widget.component.css'
})
export class HomeWidgetComponent {
  @Input() icon!: 'faGavel' | 'faSlidersH' | 'faCode' | 'faLevelUpAlt' | 'faCoins' | 'faSmile';
  @Input() title!: string;
  @Input() description!: string;
  @Input() link!: string;

  faGavel = faGavel;
  faSlidersH = faSlidersH;
  faCode = faCode;
  faLevelUpAlt = faLevelUpAlt;
  faCoins = faCoins;
  faSmile = faSmile;

  getIcon() {
    switch (this.icon) {
      case 'faGavel':
        return this.faGavel;
      case 'faSlidersH':
        return this.faSlidersH;
      case 'faCode':
        return this.faCode;
      case 'faLevelUpAlt':
        return this.faLevelUpAlt;
      case 'faCoins':
        return this.faCoins;
      case 'faSmile':
        return this.faSmile;
      default:
        return this.faGavel; // fallback to default icon
    }
  }
}
