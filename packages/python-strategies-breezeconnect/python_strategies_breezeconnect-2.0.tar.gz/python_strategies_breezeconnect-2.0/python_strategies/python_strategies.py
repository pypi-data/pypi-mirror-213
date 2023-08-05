import threading
import queue
import time 
#import datetime
import sys
import asyncio
import nest_asyncio
from breeze_connect import BreezeConnect
nest_asyncio.apply()

class Strategies:
    
    #initialize strategy object
    def __init__(self,app_key,secret_key,api_session,max_profit,max_loss):
        
        
        self.maxloss = int(max_loss)
        self.maxprofit = int(max_profit)
        self.calllock = threading.Lock()
        self.putlock = threading.Lock()
        self.currentcall = 0
        self.currentput = 0
        self.flag = False
        self.client = BreezeConnect(app_key)
        self.client.generate_session(secret_key,api_session)
        self.client.ws_connect()
    
    def squareoff(self,rightval,exchange_code, stock_code, product_type, expiry_date, right, strike_price, action, order_type, validity, stoploss, quantity, price,validity_date, trade_password, disclosed_quantity):
        data = self.client.square_off(exchange_code=exchange_code,
                            product_type="options",
                            stock_code=stock_code,
                            expiry_date=expiry_date,
                            right=rightval,
                            strike_price=strike_price,
                            action=action,
                            order_type=order_type,
                            validity=validity,
                            stoploss="0",
                            quantity=quantity,
                            price=price,
                            validity_date=validity_date,
                            trade_password="",
                            disclosed_quantity="0")
        
        print(f"square off status of {rightval} is",data)
        
    def get_date_format(self,expiry_date):
        month_names = {
                            '01': 'Jan',
                            '02': 'Feb',
                            '03': 'Mar',
                            '04': 'Apr',
                            '05': 'May',
                            '06': 'Jun',
                            '07': 'Jul',
                            '08': 'Aug',
                            '09': 'Sep',
                            '10': 'Oct',
                            '11': 'Nov',
                            '12': 'Dec'
                      }
        year = expiry_date[:4]
        month = expiry_date[5:7]
        day = expiry_date[8:10]
        formatted_date = f"{day}-{month_names[month]}-{year}"
        return(formatted_date)
        
    def trigger(self,product_type, rightval, stock_code, strike_price, quantity, expiry_date, order_type, validity, validity_date, exchange_code, stoploss, call_price, put_price, executed_price,flag):
        #print(f"current call is {self.currentcall} Rs and current put is {self.currentput} Rs")
        net_gain_loss = (self.currentcall + self.currentput)*int(quantity)
        print(f"net gain/loss received : {net_gain_loss} Rs with call gain per quantity :{self.currentcall} Rs and with put gain per quantity: {self.currentput} Rs")
        
        formatted_date = self.get_date_format(expiry_date)
        
        if(net_gain_loss > 0 and net_gain_loss >= self.maxprofit):
            print("maxprofit has reached...")
            print("SquareOff operation on both contracts call and put begins....")
            
            self.squareoff(rightval,exchange_code, stock_code, product_type, expiry_date, "Call", strike_price, "buy", order_type, validity, stoploss, quantity, call_price, validity_date, "", disclosed_quantity="0")
            self.squareoff(rightval,exchange_code, stock_code, product_type, expiry_date, "Put", strike_price, "buy", order_type, validity, stoploss, quantity, put_price, validity_date, "", disclosed_quantity="0")
            
            self.client.unsubscribe_feeds(exchange_code=exchange_code, stock_code=stock_code, product_type="options", expiry_date= formatted_date, strike_price=strike_price, right="Call", get_exchange_quotes=True, get_market_depth=False)
            self.client.unsubscribe_feeds(exchange_code=exchange_code, stock_code=stock_code, product_type="options", expiry_date= formatted_date, strike_price=strike_price, right="Put", get_exchange_quotes=True, get_market_depth=False)
            print("-------------END--------------")
            self.flag = True
        if(net_gain_loss < 0 and net_gain_loss <= self.maxloss):
            print("maxloss has reached...")
            print("SquareOff operation on both contracts call and put begins....")
            self.squareoff(rightval,exchange_code, stock_code, product_type, expiry_date, "Call", strike_price, "buy", order_type, validity, stoploss, quantity, call_price, validity_date, "", disclosed_quantity="0")
            self.squareoff(rightval,exchange_code, stock_code, product_type, expiry_date, "Put", strike_price, "buy", order_type, validity, stoploss, quantity, put_price, validity_date, "", disclosed_quantity="0")
            self.client.unsubscribe_feeds(exchange_code=exchange_code, stock_code=stock_code, product_type="options", expiry_date= formatted_date, strike_price=strike_price, right="Call", get_exchange_quotes=True, get_market_depth=False)
            self.client.unsubscribe_feeds(exchange_code=exchange_code, stock_code=stock_code, product_type="options", expiry_date= formatted_date, strike_price=strike_price, right="Put", get_exchange_quotes=True, get_market_depth=False)
            print("---------------END-----------------")
            self.flag = True
            
    async def calculate_current_call(self,product_type,rightval,stock_code, strike_price, qty, expiry_date, order_type, validity, validity_date, exchange_code, stoploss, call_price,put_price,executed_price,flag):
        print(f"inside current call() method:{rightval}")
        resultcall = []
        formatted_date = self.get_date_format(expiry_date)
        
        def ticks2(data):
            resultcall.append(data)
            with self.calllock:
                #while(result!=[]):
                value = resultcall.pop(0)
                print(f"Call : current market value of call order is {value['last']} Rs and executed price : {value['last']}")
                self.currentcall = float(value['last']) - float(executed_price)
                #print(f"current market value of call order is {value} Rs, The difference between current put price and executed price is {self.currentcall}")
                if(self.flag == False):
                    self.trigger(product_type, rightval, stock_code, strike_price, qty, expiry_date, order_type, validity, validity_date, exchange_code, stoploss, call_price,put_price,executed_price,flag)
                #time.sleep(2)
                
        self.client.ticks2 = ticks2
        self.client.subscribe_feeds(exchange_code = exchange_code, stock_code = stock_code, product_type = product_type, expiry_date= formatted_date, strike_price=strike_price, right = rightval, get_exchange_quotes=True, get_market_depth=False)
         
    async def calculate_current_put(self,product_type,rightval,stock_code, strike_price, qty, expiry_date, order_type, validity, validity_date, exchange_code, stoploss, call_price,put_price,executed_price,flag):
        print(f"inside current put method():{rightval}")
        result = []
        formatted_date = self.get_date_format(expiry_date)
        
        def ticks(data):
            result.append(data)
            with self.putlock:
                
                value = result.pop(0)
                print(f"Put : current market value of call order is {value['last']} Rs and executed price : {value['last']}")
                self.currentput = float(value['last']) - float(executed_price)
                #print(f"current market value of put order is {value} Rs , The difference between current put price and executed price is {self.currentput}")
                if(self.flag == False):
                    self.trigger(product_type, rightval, stock_code, strike_price, qty, expiry_date, order_type, validity, validity_date, exchange_code, stoploss, call_price,put_price,executed_price,flag)
                #time.sleep(2)
        
        self.client.ticks = ticks
        self.client.subscribe_feeds(exchange_code = exchange_code, stock_code = stock_code, product_type = product_type, expiry_date= formatted_date, strike_price=strike_price, right = rightval, get_exchange_quotes=True, get_market_depth=False)
        
    def profit_and_loss2(self,product_type, stock_code, strike_price, qty, expiry_date, order_type, validity, validity_date, exchange_code, stoploss, call_price, put_price, orderids,call_execution,put_execution):
        #self.calculate_current_call(product_type,"Call", stock_code, strike_price, qty, expiry_date, order_type, validity, validity_date, exchange_code, stoploss, call_price,put_price,call_execution,flag = False)
        #self.calculate_current_put(product_type,"Put", stock_code, strike_price, qty, expiry_date, order_type, validity, validity_date, exchange_code, stoploss, call_price,put_price,put_execution,flag = False)
        p1  =  mp.Process(target = self.calculate_current_call, args = (product_type,"Call", stock_code, strike_price, qty, expiry_date, order_type, validity, validity_date, exchange_code, stoploss, call_price, put_price, call_execution, False))
        p2  =  mp.Process(target = self.calculate_current_put, args = (product_type,"Put", stock_code, strike_price, qty, expiry_date, order_type, validity, validity_date, exchange_code, stoploss, call_price, put_price, put_execution, False))
        
        p1.start()
        p2.start()
        
        p1.join()
        p2.join()
        
    async def profit_and_loss(self,product_type, stock_code, strike_price, qty, expiry_date, order_type, validity, validity_date, exchange_code, stoploss, call_price, put_price, orderids,call_execution,put_execution):
        #self.calculate_current_call(product_type,"Call", stock_code, strike_price, qty, expiry_date, order_type, validity, validity_date, exchange_code, stoploss, call_price,put_price,call_execution,flag = False)
        #self.calculate_current_put(product_type,"Put", stock_code, strike_price, qty, expiry_date, order_type, validity, validity_date, exchange_code, stoploss, call_price,put_price,put_execution,flag = False)
        p1  =  asyncio.create_task(self.calculate_current_call(product_type,"Call", stock_code, strike_price, qty, expiry_date, order_type, validity, validity_date, exchange_code, stoploss, call_price, put_price, call_execution, False))
        p2  =  asyncio.create_task(self.calculate_current_put(product_type,"Put", stock_code, strike_price, qty, expiry_date, order_type, validity, validity_date, exchange_code, stoploss, call_price, put_price, put_execution, False))
        
        #task1 = asyncio.create_task(perform_operation1())
        #task2 = asyncio.create_task(perform_operation2())

        # Wait for all tasks to complete
        await asyncio.gather(p1, p2)
        
        
    async def long_straddle(self, product_type, stock_code, strike_price, qty, expiry_date, order_type, validity, validity_date, exchange_code, stoploss, put_price, call_price):
        def place_order_method(stock_code,exchange_code,product,action,order_type,stoploss,quantity,price,validity,validity_date,expiry_date,right,strike_price,res_queue):
         
            data =  self.client.place_order(stock_code=stock_code,
                    exchange_code=exchange_code,
                    product="options",
                    action = "buy",
                    order_type=order_type,
                    stoploss=stoploss,
                    quantity=qty,
                    price = price,
                    validity= validity,
                    validity_date = validity_date,
                    disclosed_quantity = "0",
                    expiry_date = expiry_date,
                    right= right,
                    strike_price=strike_price)
            print(data)
            res_queue.put(data)
            return(data)
                  
        res_queue = queue.Queue()
        #create thread for call and put order to execute simultaneously for buy type
        t1 = threading.Thread(target = place_order_method,args = (stock_code,exchange_code,"options","buy",order_type,stoploss,qty,call_price,validity,validity_date,expiry_date,"Call",strike_price,res_queue))
        t1.start()
        t1.join()
        
        firstresponse = res_queue.get()
        
        res_queue = queue.Queue()
        t2 = threading.Thread(target = place_order_method,args = (stock_code,exchange_code,"options","buy",order_type,stoploss,qty,put_price,validity,validity_date,expiry_date,"Put",strike_price,res_queue))
        t2.start()
        t2.join()
        secondresponse = res_queue.get()
        
        
        #if one of the order fails then squareoff the other one which is successfull
        if(firstresponse.get('Success',None)!=None and secondresponse.get('Success',None)==None):
            
            order_id = firstresponse['Success']['order_id']
            self.client.square_off(exchange_code="NFO",
                    product = "options",
                    stock_code = stock_code,
                    expiry_date= expiry_date,
                    right="Call",
                    strike_price= strike_price,
                    action="buy",
                    order_type= order_type,
                    validity = validity,
                    stoploss="0",
                    quantity = qty,
                    price = price,
                    validity_date = validity_date,
                    trade_password="",
                    disclosed_quantity="0")
            
            if(data.get("Success",None) == None):
                print("PUT Order SquareOff has not been successfull")
                print("----------END-------------------")
            else:
                print("PUT Order SquareOff has  been successfull")
                print("----------END-------------------")
            
            return("Call Order Failed...")
        
        elif(secondresponse.get('Success',None)!=None and firstresponse.get('Success',None)==None):
            
            order_id = secondresponse['Success']['order_id']
            
            data = self.client.square_off(exchange_code="NFO",
                    product = "options",
                    stock_code = stock_code,
                    expiry_date= expiry_date,
                    right="Put",
                    strike_price = strike_price,
                    action="buy",
                    order_type= order_type,
                    validity = validity,
                    stoploss="0",
                    quantity = qty,
                    price = price,
                    validity_date = validity_date,
                    trade_password="",
                    disclosed_quantity="0")
            
            if(data.get("Success",None) == None):
                print("Call Order SquareOff has not been successfull")
            else:
                print("Call Order SquareOff has  been successfull")
            return("Put order failed....")
        
        elif(firstresponse.get('Success',None)==None and secondresponse.get('Success',None)==None):
            print("both order call and put have failed")
            print("------------END----------------")
            
        
        else:
            orderids = [] #0th index will contain call order, #1st index will contain put order 
            orderids.append(firstresponse['Success']['order_id']) 
            orderids.append(secondresponse['Success']['order_id'])            
            #define a mechanism to get profit and loss
            print("----lets wait for 100 seconds for getting the executed status---")
            time.sleep(100)
            details = self.client.get_order_detail(exchange_code=exchange_code,
                        order_id= orderids[0])
            print(details)
            call_execution = -1
            put_execution = -1
            
            print(orderids)
            for entry in details['Success']:
                if(entry['status'] == "Executed"):
                    call_execution = entry['average_price']
                    break
                    
            details = self.client.get_order_detail(exchange_code=exchange_code,
                        order_id= orderids[1])
            print(details)
            for entry in details['Success']:
                if(entry['status'] == "Executed"):
                    put_execution = entry['average_price']
                    break
                    
            if(call_execution == -1 or put_execution == -1):
                print("Dear User order could not execute within time limit ..cancelling it")
                if(call_execution == -1):
                    #call cancel order api
                    print("call order could not execute due to some reason so cancelling order")
                    self.client.cancel_order(exchange_code=exchange_code,
                    order_id = orderids[0])
                    
                if(put_execution == -1):
                    #call cancel order api
                    print("put order could not execute due to some reason so cancelling order")
                    status = self.client.cancel_order(exchange_code=exchange_code,
                    order_id = orderids[1])
                    
            else:
                print("Call order got executed at price :{0} Rs and Put Order got executed at price : {1} Rs".format(call_execution,put_execution))
                await self.profit_and_loss(product_type, stock_code, strike_price, qty, expiry_date, order_type, validity, validity_date, exchange_code, stoploss, call_price, put_price, orderids,call_execution,put_execution)
            