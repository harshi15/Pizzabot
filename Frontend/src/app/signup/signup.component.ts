import { RestService } from '../rest.service';
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent implements OnInit {

  constructor(private restService: RestService, private router: Router) { }

  loginData: any = {};
  ngOnInit(): void {
  }

  login(data) {
    console.log("data 1121",data)
    this.loginData = data;
    let successCallback = function (response) {
      console.log("response",response)
      this.isPageLoading = false;
      if (!response.success){
        this.loginError = true;
      } else {
        this.router.navigate(['login']);
          // let tokenInfo = this.getDecodedAccessToken(response.token);
          //localStorage.setItem('userId',tokenInfo.id)
          // localStorage.setItem('userInfo',response.token)
          // this.router.navigate(['dashboard']);
      }
    }

    let errorCallback = function (response) {
      console.log("error response",response)
      this.loginError = true;
      // this.isPageLoading = false;
    }

    this.restService.postCall('/user', this.loginData, {"Content-Type": "application/json"}, successCallback.bind(this), errorCallback.bind(this));   
  }

}
