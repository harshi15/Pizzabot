import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { ChatWindowComponent } from './chat-window/chat-window.component';
// import { LoginComponent } from './login/login.component';
import { FormsModule } from '@angular/forms';
import { LoginComponent } from './login/login.component';
import { SignupComponent } from './signup/signup.component';
import { HttpClientModule } from '@angular/common/http';
import { UserIdleModule } from 'angular-user-idle';
import { Ng2CompleterModule } from 'ng2-completer';

@NgModule({
  declarations: [
    AppComponent,
    ChatWindowComponent,
    LoginComponent,
    SignupComponent,
    // LoginComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    HttpClientModule,
    UserIdleModule.forRoot({idle: 300, timeout: 150, ping: 10}),
    Ng2CompleterModule 
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
