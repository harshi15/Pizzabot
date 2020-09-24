import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { RestService } from '../rest.service';
import { UserIdleService } from 'angular-user-idle';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  constructor(private restService: RestService, private router: Router, private userIdle: UserIdleService) { }
  loginData: any = {};
  ngOnInit(): void {
    if (localStorage.getItem("chatId")){
      this.router.navigate(['chat']);

    }
    //Start watching for user inactivity.
    this.userIdle.startWatching();

    // Start watching when user idle is starting.
    this.userIdle.onTimerStart().subscribe(count => console.log(count));
    
    // Start watch when time is up.
    this.userIdle.onTimeout().subscribe(() => localStorage.clear());

  }

  login(data) {
    console.log("data",data)
    this.loginData = data;
    let successCallback = function (response) {
      console.log("response",response)
      this.isPageLoading = false;
      if (!response.success){
        this.loginError = true;
        alert("Incorrect Password")
      } else {
        
          // let tokenInfo = this.getDecodedAccessToken(response.token);
          //localStorage.setItem('userId',tokenInfo.id)
          localStorage.setItem('chatId',response.payload.chatId)
          // this.router.navigate(['dashboard']);
          this.router.navigate(['chat']);
      }
    }

    let errorCallback = function (response) {
      console.log("error response",response)
      this.loginError = true;
      if (response.status==404){
      alert("User does not Exist!")
      }
      else{alert("InCorrect Password")}

      // this.isPageLoading = false;
    }

    this.restService.postCall('/login', this.loginData, {"Content-Type": "application/json"}, successCallback.bind(this), errorCallback.bind(this));   
  }

}
