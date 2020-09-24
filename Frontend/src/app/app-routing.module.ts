import {NgModule} from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {LoginComponent} from './login/login.component';
import {ChatWindowComponent} from './chat-window/chat-window.component';
import {SignupComponent} from './signup/signup.component';


const routes:Routes = [
  {path:'', pathMatch:'full', redirectTo:'login'},
  { path: 'login', component: LoginComponent },
  { path: 'signup', component: SignupComponent },
  {path:'chat', component: ChatWindowComponent},
  { path: 'static/login', component: LoginComponent },
  { path: 'static/signup', component: SignupComponent },
  {path:'static/chat', component: ChatWindowComponent},
  { path: '**', redirectTo: 'login' }
];

@NgModule({
  imports:[RouterModule.forRoot(routes,{ useHash: true })],
  exports:[RouterModule]
})
export class AppRoutingModule {};