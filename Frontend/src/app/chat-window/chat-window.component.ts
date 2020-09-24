import { Component, OnInit, ViewChild, ElementRef, IterableDiffers, DoCheck } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { NgModule } from '@angular/core';
import { Router } from '@angular/router';
import {RestService} from '../rest.service';

@Component({
  selector: 'app-chat-window',
  templateUrl: './chat-window.component.html',
  styleUrls: ['./chat-window.component.css']
})
export class ChatWindowComponent implements OnInit ,DoCheck{

  differ: any;
  change:any;
  refreshIntervalId:any;
  
  message:string;
  loading:boolean;
  messages = [];
  value: string ="";
  public pizzas =['margherita pizza', 'golden corn pizza', 'jalapeno & red paprika pizza', 'double cheese margherita pizza', 'crisp capsicum & fresh tomato pizza', 'farmhouse pizza', 'spicy triple tango', 'paneer special pizza', 'pepper barbecue chicken', 'pepper barbecue chicken i cheese', 'chicken sausage', 'chicken sausage i cheese', 'chicken golden delight', 'non veg supreme', 'chicken dominator', 'pepper barbecue & onion', 'chicken fiesta', 'indi chicken tikka']
  public crusts = ['classic hand tossed', 'wheat thin crust', 'cheese burst', 'fresh pan pizza', 'italian crust', 'double cheese crunch']
  public sizes=['regular','medium','large']
  public pizzaData=this.pizzas

  @ViewChild('msgContainer') private myScrollContainer: ElementRef;
  
  constructor(private restService:RestService, private router: Router,differs: IterableDiffers) { 
    this.differ = differs.find([]).create(null);
  }
  
  ngOnInit(): void {
    if (localStorage.getItem("chatId")==undefined){
      this.router.navigate(['login']);

    }
    this.getMessages();
    // setInterval(()=>{ this.getMessages(); 

    //       }, 2000);
  }

  ngDoCheck() {
    this.change = this.differ.diff(this.messages);
    if (this.change){
    setTimeout(()=>{ 
      this.myScrollContainer.nativeElement.scroll({
      top: this.myScrollContainer.nativeElement.scrollHeight,
      left: 0,
      behavior: "smooth"
      }); },2)
    }
    // console.log(this.change);
 
  }


  // constructor(public chatService: ChatService) { }

  // ngOnInit() {
  //     this.chatService.conversation.subscribe((val) => {
  //     this.messages = this.messages.concat(val);
  //   });
  // }

  getMessages(){
    let chatId =localStorage.getItem("chatId")
    // chatId= "2532542"
    if (chatId){
      if(this.loading){
          this.messages.push({"content":'loading',"author":"bot"})
      }
        let successCallback = function (response) {
          if (response.status==404){
            alert("Please login again !")
            this.logout();
            }
          // console.log("response",response)
          this.isPageLoading = false;
          if (!response.success){
            this.loginError = true;
            
          } else {
            // console.log(response)
            this.messages = response.data
            
            // this.messages=[]
          }
        }

        let errorCallback = function (response) {
          if (response.status==404){
            alert("Please login again !")
            this.logout();
            }
          // console.log("error response",response)
          this.messages = response.data
          this.loginError = true;
          // this.isPageLoading = false;
        }
        this.loading=false;
        this.restService.getcall('/chats?chatId=' +chatId ,  {"Content-Type": "application/json"}, errorCallback.bind(this), successCallback.bind(this));   
    }
    else{
      this.logout();
    }
  }


  sendMessage() {
    // this.chatService.getBotAnswer(this.value);
      if (this.message){
        if (this.message === "logout" || this.message === "Logout"){
          this.logout();
        }
        else{
              let msgData = {"content":this.message,"author":"user"};
              this.messages.push(msgData)
              this.loading=true;
              msgData["chatId"]=localStorage.getItem("chatId")
              let successCallback = function (response) {
                console.log("response",response)
                this.isPageLoading = false;
                if (!response.success){
                  this.loginError = true;
                  
                } else {
                  // setTimeout(function(){  this.getMessages(); }, 3000);
                  console.log("MSG posted")
                  if (this.message=="reset") {
                    this.pizzaData=this.pizzas;
                  }
                  if (this.pizzaData.indexOf(this.message) >= 0) {
                    this.pizzaData=this.sizes;
                  }
                  if (this.pizzaData.indexOf(this.message) >= 0) {
                    this.pizzaData=this.crusts;
                  }
                  this.message=""
                }
              }

              let errorCallback = function (response) {
                console.log("error response",response)
                this.loginError = true;
                if (response.status==404){
                  alert("Please login again !")
                  this.logout();
                  }
                // this.isPageLoading = false;
              }

              this.restService.postCall('/chats', msgData, {"Content-Type": "application/json"}, successCallback.bind(this), errorCallback.bind(this));  
              
              for(let i=0 ; i<10; i++){
                this.getMessages();
              }


            } 
        }
          }

      logout(){
        localStorage.clear()
        this.router.navigate(['login']);
      }

  

}
