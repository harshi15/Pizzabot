import pymongo
from flask import Flask, jsonify,make_response,render_template
from flask_restful import Resource, Api, request
import json
import traceback
import re 
import hashlib
import jwt
import datetime
import os
import time
from logging.handlers import TimedRotatingFileHandler
import logging.config
import logging
import copy
import requests
import random
import string
from flask_cors import CORS, cross_origin
import functools
import threading
import copy
from collections import defaultdict


    
base_path = os.path.abspath(os.path.dirname(__file__))
# log_file_path = os.path.join(base_path,'vaas.log')
logs_storage = os.path.join(base_path,'logs','pizza.log')
# logger = logging.getLogger()

myclient = pymongo.MongoClient("mongodb+srv://mypc:Y9uHv9Hpy2QaNDrJ@cluster0.8jjuk.mongodb.net/<dbname>?retryWrites=true&w=majority")
mydb = myclient["CHATBOT"]

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'thisissecret'
# base_path = os.path.abspath(os.path.dirname(__file__))
# app.config['UPLOAD_FOLDER'] = os.path.join(base_path,"Uploads")
# app.config['MAX_CONTENT_PATH'] = 
api = Api(app)


class Users(Resource):
    def __init__(self):
        pass
    # @app.route('/user', methods=['POST'])
    def post(self):
        try:
            response = {'success' : False, 'message' : 'Failure', "payload" : ''}
            mycol = mydb["users"]
            users = request.json
            letters = string.ascii_lowercase + string.digits
            ordersId = ''.join(random.choice(letters) for i in range(10))
            # tempId = ''.join(random.choice(letters) for i in range(8))
            chatId = ''.join(random.choice(letters) for i in range(15))
            users["chatId"]= chatId
            users["ordersId"]= ordersId
            if(list(mycol.find({"email":f"{users['email']}"}))):
                response['message'] = 'User Already Exist'
                status = 400
            else:
                temp = hashlib.md5(users['password'].lower().encode())
                encoded_password = temp.hexdigest()
                users['password'] = encoded_password
                mycol.insert_one(users)
                response['message'] = 'User Added Successfully'
                response['success'] = True
                response['payload'] = 'User Added Successfully'
                status = 200
        
        except:
            print(traceback.format_exc())
            # logger.error(traceback.format_exc())
            response['message'] = "Error"
            status = 400
        finally:
            return(make_response(response, status))
        

    # @app.route('/user', methods=['DELETE'])
    def delete(self):
        try:
            mycol = mydb["users"]
            email = request.args.get('email')
            if(list(mycol.find({"email":f"{email}"}))):
                myquery = { "email": f"{email}" }
                mycol.delete_one(myquery)
                res = jsonify({'result' : " user has been deleted"})
                status = 200
            else:
                res = jsonify({'result' : "this  user doesn't exists"})
                status = 200
        except:
            print(traceback.format_exc())
            # logger.error(traceback.format_exc())
            res = jsonify({'result' : "not updated"})
            status = 400
        finally:
            return(make_response(res, status))

    # @app.route('/view_user')
    def get(self):
        try:
            mycol = mydb["users"]
            output=[]
            for q in mycol.find():
                output.append({'name' : q['name'], 'email' : q['email']})
            res={'data' : output}
            # print(res)
            # print(type(res))
            # print('response is ',jsonify(res))
            status = 200
        except:
            print(traceback.format_exc())
            # logger.error(traceback.format_exc())
            res['message'] = "Error"
            status = 400
        finally:
            return(make_response(jsonify(res), status))
    
    def put(self):
        try:
            response = {'success' : False, 'message' : 'Failure', "payload" : ''}
            mycol = mydb["users"]
            user_update = request.json
            user_data = mycol.find_one({"email":f"{user_update['email']}"})
            if not user_data:
                response['message'] = 'User Does Not exist'
                status = 400
            else:
                if user_update.get('password', []):
                    encoded_password = hashlib.md5(user_update['password'].lower().encode()).hexdigest()
                    user_update['password'] = encoded_password
                mycol.update_one({'email' : user_update['email']}, {"$set" : user_update})
                response['message'] = 'User Data Updated Successfully'
                response['success'] = True
                response['payload'] = 'User Data Updated Successfully'
                status = 200
        
        except:
            print(traceback.format_exc())
            # logger.error(traceback.format_exc())
            response['message'] = "Error"
            status = 400
        finally:
            return(make_response(response, status))

# @app.route('/login',methods=['POST'])
class Login(Resource):
    def __init__(self):
        pass
    def post(self):
        response = {'success' : False, 'message' : 'Failure', "payload" : ''}   
        try:
            status = 400
            mycol = mydb["users"]
            req_json = request.json
            email = req_json['email']
            password =req_json['password']
            response = {'success' : False, 'message' : 'Failure', "payload" : ''}
            payload = {'isLoggedIn' : False, 'name' : ''}
            user_found = mycol.find_one({"email":email})
            # print("endoc",decoded_password,password)
            if not user_found:
                status = 404
                message = 'User Not Found'
                payload = "User Not Found"
                success =False
            else:
                user_name =  user_found.get('name',None)
                isLoggedIn = False if not user_name else True
                success = False if not user_name else True
                message = 'Failure' if not user_name else 'Success'
                saved_password = user_found.pop('password')
                # print('saved_password: ', saved_password)
                encoded_password = hashlib.md5(password.lower().encode()).hexdigest()
                # print('encoded_password: ', encoded_password)
                user_found.pop('_id')
                payload = user_found
                chatcol=mydb[user_found.get('chatId')]
                if list(chatcol.find()):
                    chatcol.insert_one({"content":"Hi","author":"bot"})
                    chatcol.insert_one({"content":"Welcome to  ∏-zza Corner","author":"bot"})
                    chatcol.insert_one({"content":"What kind of pizza do you want?","author":"bot"})
                    chatcol.insert_one({"content":"veg or nonveg","author":"bot"})
                temp = mydb["temp"]
                temp.update({"chatId":user_found.get('chatId')},{"$set":{"level": 1}})
                
                if encoded_password != saved_password:
                    message = 'Incorrect Password'
                    payload = 'Incorrect Password'
                    status = 200
                    success =False
                else:
                    payload = user_found
                    payload['isLoggedIn'] = isLoggedIn
                    status = 200

            response['payload'] = payload
            response['success']  = success
            response['message'] = message         
        except:
            print(traceback.format_exc())
            logger.error(traceback.format_exc())
            response['message'] = "Error"
            status = 400
        finally:
            return(make_response(response, status))




class Chats(Resource):
    def __init__(self):
        self.level=1
        self.pizza=""
        self.size=""
        self.toppings=""
        self.crust=0

    
    def getbotResponse(self,data):
            response = {'success' : False, 'message' : 'Failure', "payload" : ''}   
            try:
                chatId,content = data.get('chatId'),data.get('content')
                if content:
                    content=content.lower().strip()
                mycol = mydb[chatId]
                temp = mydb["temp"]
                users = mydb["users"]
                user = list(users.find({"chatId":chatId}))[0]
                if not list(temp.find({"chatId":chatId})):
                    temp.insert_one({"chatId":chatId,"level":1,"pizza":"","size":"","toppings":"","crust":"","number":0})
                tempdata = list(temp.find({"chatId":chatId}))[0]
                # print('tempdata: ', tempdata)
                if content.lower()=="reset":
                    mycol.insert_one({"content":"What kind of pizza do you want?","author":"bot"})
                    mycol.insert_one({"content":"veg or nonveg","author":"bot"})
                    temp.update({"chatId":chatId},{"$set":{"level": 1}})
                elif content.lower()=="help":
                    mycol.insert_one({"content":"You can use following commands","author":"bot"})
                    mycol.insert_one({"content":"Reset - to Cancel the process and start ordering from start","author":"bot"})
                    mycol.insert_one({"content":"Status or Order status - to get the last placed order status","author":"bot"})
                    mycol.insert_one({"content":"logout - to logout ","author":"bot"})
                elif content.lower()=="status" or content.lower()=="order status" or content.lower()=="orderstatus":
                                ord = mydb[user.get("ordersId")]
                                lastord = user.get("lastorder")
                                status =list(ord.find({"orderId":user.get("lastorder")}))[0]
                                ordst=status.get("ordStatus")
                                mycol.insert_one({"content":f"ORDER ID: {lastord.upper()} , STATUS: {ordst} ","author":"bot"}) 
                else:
                    self.level,self.pizza,self.size,self.toppings,self.crust,self.number = tempdata.get("level"),tempdata.get("pizza"),tempdata.get("size"),tempdata.get("toppings"),tempdata.get("crust"),tempdata.get("number")
                    if  self.level==1:
                        if content =="veg":
                            mycol.insert_one({"content":"OK Please Choose a Pizza","author":"bot"})
                            mycol.insert_one({"content":"Margherita Pizza, Golden Corn Pizza, Jalapeno & Red Paprika Pizza, Double Cheese Margherita Pizza, Crisp Capsicum & Fresh Tomato Pizza, Farmhouse Pizza, Spicy Triple Tango, Paneer Special Pizza","author":"bot"})
                            temp.update({"chatId":chatId},{"$set":{"level": 2}})
                        elif content =="nonveg":
                            mycol.insert_one({"content":"OK Please Choose a Pizza","author":"bot"})
                            mycol.insert_one({"content":"PEPPER BARBECUE CHICKEN, Pepper Barbecue Chicken I Cheese, CHICKEN SAUSAGE, Chicken Sausage I Cheese, Chicken Golden Delight, Non Veg Supreme, Chicken Dominator, PEPPER BARBECUE & ONION, CHICKEN FIESTA, Indi Chicken Tikka","author":"bot"})
                            temp.update({"chatId":chatId},{"$set":{"level": 2}})
                        else:
                            
                            if content.lower()=="ok":
                                mycol.insert_one({"content":"Wanna Order a Pizza ? send veg or nonveg","author":"bot"})
                            else:
                                mycol.insert_one({"content":"Please send the correct option","author":"bot"})
                    elif  self.level==2:
                        if content in ['margherita pizza', 'golden corn pizza', 'jalapeno & red paprika pizza', 'double cheese margherita pizza', 'crisp capsicum & fresh tomato pizza', 'farmhouse pizza', 'spicy triple tango', 'paneer special pizza', 'pepper barbecue chicken', 'pepper barbecue chicken i cheese', 'chicken sausage', 'chicken sausage i cheese', 'chicken golden delight', 'non veg supreme', 'chicken dominator', 'pepper barbecue & onion', 'chicken fiesta', 'indi chicken tikka']:
                            # self.pizza= content
                            mycol.insert_one({"content":"How Large ?","author":"bot"})
                            mycol.insert_one({"content":"Regular,Medium,Large","author":"bot"})
                            temp.update({"chatId":chatId},{"$set":{"level": 3,"pizza":content}})
                        else:
                            mycol.insert_one({"content":"Please send the correct option","author":"bot"})
                    elif  self.level==3:
                        if content.lower().strip() in ["regular","medium","large"]:
                            # self.size=content
                            mycol.insert_one({"content":"Do you want to customise your pizza ?  Toppings, Cheese etc. send the item","author":"bot"})
                            temp.update({"chatId":chatId},{"$set":{"level": 4,"size":content}})
                        else:
                            mycol.insert_one({"content":"Please send the correct option","author":"bot"})

                    elif  self.level==4:
                        if content=="no":
                            content="none"
                        mycol.insert_one({"content":"Pick a crust type ","author":"bot"})
                        mycol.insert_one({"content":"Classic Hand Tossed, Wheat Thin Crust, Cheese Burst, Fresh Pan Pizza, Italian Crust, Double Cheese Crunch ","author":"bot"})
                        temp.update({"chatId":chatId},{"$set":{"level": 5,"toppings":content}})

                    elif  self.level ==5:
                        if content in ['classic hand tossed', 'wheat thin crust', 'cheese burst', 'fresh pan pizza', 'italian crust', 'double cheese crunch']:
                            mycol.insert_one({"content":"How many ? ","author":"bot"})
                            temp.update({"chatId":chatId},{"$set":{"level": 6,"crust":content}})
                        else:
                            mycol.insert_one({"content":"Please send the correct option","author":"bot"})

                    elif  self.level ==6:
                        if  int(content) and int(content)<20: 
                            mycol.insert_one({"content":"Ok! Should i place the order ? ","author":"bot"})
                            temp.update({"chatId":chatId},{"$set":{"level": 7,"number":content}})
                        else:
                            mycol.insert_one({"content":f"comeon who will eat {content} pizzas, order less than 20.","author":"bot"})

                    elif  self.level ==7:
                        if content.lower()=="yes":
                            mycol.insert_one({"content":"Please check this address -- "+str(user.get('address')),"author":"bot"})
                            mycol.insert_one({"content":"If this is correct please send yes , if not send new address ","author":"bot"})
                            temp.update({"chatId":chatId},{"$set":{"level": 8}})
                        elif content.lower()=="no":
                            mycol.insert_one({"content":"cancelled the order ","author":"bot"})
                            temp.delete_one({"chatId":chatId})
                        else:
                            mycol.insert_one({"content":"Please send the correct option","author":"bot"})

                    elif  self.level ==8:
                        if content.lower()=="yes":
                            mycol.insert_one({"content":f"Your Order is Successfully placed. \n Details: \n {self.number} {self.pizza}, size {self.size} with toppings {self.toppings} and crust {self.crust}","author":"bot"})
                            mycol.insert_one({"content":"Our Agent will call you on this number: "+str(user.get('phone-number')),"author":"bot"})
                            temp.delete_one({"chatId":chatId})
                        else:
                            users.update({"chatId":chatId},{"$set":{"address":content}})
                            mycol.insert_one({"content":f"Your Order is Successfully placed. \n Details: \n {self.number} {self.pizza}, size {self.size} with toppings {self.toppings} and crust {self.crust}","author":"bot"})
                            mycol.insert_one({"content":"Our Agent will call you on this number: "+str(user.get('phone-number')),"author":"bot"})
                            temp.delete_one({"chatId":chatId})
                        p2 = threading.Thread(target=Orders(chatId).post, args=({"chatId":chatId,"level":self.level,"pizza":self.pizza,"size":self.size,"toppings":self.toppings,"crust":self.crust,"number":self.number}, ) )
                        p2.start()
                    else:
                        mycol.insert_one({"content":"Please send the correct option","author":"bot"})
                          
                response['message'] = 'Message sent Successfully'
                response['success'] = True
                status = 200
            except:
                print(traceback.format_exc())
                # logger.error(traceback.format_exc())
                response['message'] = "Error"
                status = 400






    def post(self):
        response = {'success' : False, 'message' : 'Failure', "payload" : ''}   
        try:
            message = request.json
            cmessage = dict(message)
            chatId =message.get("chatId")
            if chatId:
                mycol = mydb['users']
                if list(mycol.find({"chatId":chatId})):
                    p1 = threading.Thread(target=self.getbotResponse, args=(cmessage, ) )
                    chatId = str(message.pop('chatId'))
                    # print('message1: ', message)
                    mycol = mydb[chatId]
                    # print('users: ', message)
                    mycol.insert_one(message)
                    p1.start()
                    response['message'] = 'Message sent Successfully'
                    response['success'] = True
                    status = 200
                else:
                    response['payload'] = 'Message NOT  posted, You are an imposter'
                    status = 404
            else:
                response['payload'] = 'Message NOT  posted send the chat id'
                status = 400
        
        except:
            print(traceback.format_exc())
            # logger.error(traceback.format_exc())
            response['message'] = "Error"
            status = 400
        finally:
            return(make_response(response, status))
        

    # @app.route('/view_user')
    def get(self):
        response = {'success' : False, 'message' : 'Failure', "payload" : ''}   
        try:
            message = dict(request.args)
            # print('message: ', message)
            if message.get("chatId"):
                chatId = str(message.pop('chatId'))
                mycol = mydb['users']
                if list(mycol.find({"chatId":chatId})):
                    mycol = mydb[chatId]
                    output=[]
                    # print('mycol.find(): ', list(mycol.find()))
                    if not list(mycol.find()):
                        
                        mycol.insert_one({"content":"Hi","author":"bot"})
                        mycol.insert_one({"content":"Welcome to  ∏-zza Corner","author":"bot"})
                        mycol.insert_one({"content":"help - to see all the commands available","author":"bot"})
                        mycol.insert_one({"content":"What kind of pizza do you want?","author":"bot"})
                        mycol.insert_one({"content":"veg or nonveg","author":"bot"})
                    else:
                        for q in mycol.find():
                            q.pop("_id")
                            output.append(q)
                    response['data'] = output
                    response['message'] = 'Messages received Successfully'
                    response['success'] = True
                    status = 200
                else:
                    response['payload'] = "can't get messages, You are an imposter"
                    status = 404

        except:
            print(traceback.format_exc())
            logger.error(traceback.format_exc())
            response['message'] = "Error"
            status = 400
        finally:
            return(make_response(jsonify(response), status))
    
class Orders:
    def __init__(self,chatId):
        self.chatId=chatId
        self.mycol = mydb["users"]
        self.chatcol = mydb[chatId]
        users = list(self.mycol.find({"chatId":chatId}))
        if users:
            users[0].pop("_id")
            self.user = users[0]
            


    def post(self,data):
        response = {'success' : False, 'message' : 'Failure', "payload" : ''}   
        try:
            ordersId = self.user.get("ordersId")
            if ordersId and data:
                ord = mydb[ordersId]
                letters = string.ascii_lowercase + string.digits
                orderId = ''.join(random.choice(letters) for i in range(11))
                data["orderId"]=orderId
                data["ordStatus"]="Baking"
                ord.insert_one(data)
                self.mycol.update({"chatId":self.chatId},{"$set":{"lastorder": orderId}})
                self.chatcol.insert_one({"content":f"Order ID  is {orderId.upper()}","author":"bot"})



                response['message'] = 'Message sent Successfully'
                response['success'] = True
                status = 200
            else:
                response['payload'] = 'Message NOT  posted send the chat id'
                status = 400
        
        except:
            print(traceback.format_exc())
            # logger.error(traceback.format_exc())
            response['message'] = "Error"
            status = 400
        finally:
            return(make_response(response, status))
        

    # @app.route('/view_user')
    def get(self,type,orderId=None):
        response = {'success' : False, 'message' : 'Failure', "payload" : ''}   
        try:
            if type == "single":
                if orderId:
                    lastorder = self.user.get("lastorder")
                    output = {"orderId":orderId,"status":lastorder}
                    response['data'] = output
                    response['message'] = 'Messages received Successfully'
                    response['success'] = True
                    status = 200
        except:
            print(traceback.format_exc())
            # logger.error(traceback.format_exc())
            response['message'] = "Error"
            status = 400
        finally:
            return(make_response(jsonify(response), status))

api.add_resource(Users, '/user')
api.add_resource(Login, '/login')
api.add_resource(Chats, '/chats')
@app.route('/', methods=['GET'])
def root():
        return render_template('index.html') # Return index.html
@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html')

if __name__ == '__main__':  
    logger = logging.getLogger()
    formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
    logging.Formatter.converter = time.localtime
    # use very short interval for this example, typical 'when' would be 'midnight' and no explicit interval
    handler = logging.handlers.TimedRotatingFileHandler(logs_storage, when="midnight", interval=1, backupCount=10)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    logger.info("Starting Flask")
    app.run(host='localhost', port = 5000,debug=True)