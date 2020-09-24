import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'Pizzabot';
  links = [
    {path:'/main',label:'main',active:'button-active'},
    {path:'/chat',label:'chat',active:'button-active'}
  ]
}
