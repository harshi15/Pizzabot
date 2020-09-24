import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ApplicationSettings } from './appSettings';


@Injectable({
  providedIn: 'root'
})
export class RestService {

  constructor(private http: HttpClient) { }

  // restAPIURL: string = ApplicationSettings.servericeurl;   //for dev
  restAPIURL: string = window.location.origin;   //for prod

  // public getNews(){
  //   return this.http.get(`https://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=${this.API_KEY}`);
  // }

  postCall(serviceURI, formData, headers = {}, successCallback, errorCallback) {
    this.http.post(this.restAPIURL + serviceURI, formData, { observe: 'response' }).subscribe(
      res => {
        successCallback(res.body);
      },
      err => {
        errorCallback(err);
      }
    );
  }

  getcall(serviceURI,  headers = {}, successCallback, errorCallback) {
    this.http.get(this.restAPIURL + serviceURI).subscribe(
      res => {
        successCallback(res);
      },
      err => {
        errorCallback(err);
      }
    );
  }
}

