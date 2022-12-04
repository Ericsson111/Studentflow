import os,binascii 
from collections import deque

user_dictionary = ['John', 'Smith', 'Luke', 'Matthew']
user_wallet_dictionary = {'John': ['c923d48c20087e0e780d4ffaeca64ee6b63f3b1ed8710c2cd40a7e32c063acc0', '31247283d389a52a491777189ac2de51ee460cf23a80791662d960c86fc818cd'], 
               'Smith': ['117385d1f3d9a9985d0e90515603200d6f8d1bbf81086d5e6382525eb193d4aa'], 
               'Luke': ['3b9ea03d3aad72d19bb707b3f33bd58931bc09b2b084971e7e6481516ccafc69', '44060681be4df0269881cfa1ac49496bb2d977e51abd30d7937369932e777ca3'], 
               'Matthew': ['ba2ae63f3a5b4ae1516e104828047cbc50e69f657449f70edb1091236a227e7d']}

# user's wallet address consists of 64 digits of numbers and alphabets

wallet_address_dictionary = {'c923d48c20087e0e780d4ffaeca64ee6b63f3b1ed8710c2cd40a7e32c063acc0': 100,
                  '31247283d389a52a491777189ac2de51ee460cf23a80791662d960c86fc818cd': 200,
                  '117385d1f3d9a9985d0e90515603200d6f8d1bbf81086d5e6382525eb193d4aa': 150,
                  '3b9ea03d3aad72d19bb707b3f33bd58931bc09b2b084971e7e6481516ccafc69': 100,
                  '44060681be4df0269881cfa1ac49496bb2d977e51abd30d7937369932e777ca3': 100,
                  'ba2ae63f3a5b4ae1516e104828047cbc50e69f657449f70edb1091236a227e7d': 200}

current_transaction_dictionary = {} # transaction_valid_token = ['sender_wallet_address', 'recipient_wallet_address', amount]
current_transaction_token_array = deque() # Stores awaiting transaction token and use popleft to process the awaiting list

class Transaction_system():
        def transaction_navigation(sender_address: str, recipient_address: str, transaction_amount: int): # navigaet through transaction process
               if Transaction_system.sender_wallet_availability(sender_address, transaction_amount) == True: # if sender wallet do contain enough money
                    if Transaction_system.recipient_wallet_availability(recipient_address) == True:
                          Transaction_system.generate_transaction_code(sender_address, recipient_address, transaction_amount) # add new transaction to waiting list
                          Transaction_system.process_current_transaction_dictionary() 
                    
                    if Transaction_system.recipient_wallet_availability(recipient_address) == False:
                          print("There is no recipient with this address.")
                          
               if Transaction_system.sender_wallet_availability(sender_address, transaction_amount) == False:
                    print("There is not enough currency in this wallet to perform this transaction.")
                      

        def sender_wallet_availability(sender_wallet_address: str, transaction_amount: int): # Determine if user selected wallet contain enough money for transaction
                sender_wallet_amount = int(wallet_address_dictionary[sender_wallet_address])
                if sender_wallet_amount >= transaction_amount:
                    return True
                if sender_wallet_amount < transaction_amount:
                    return False
                
        def recipient_wallet_availability(recipient_wallet_address: str): # determine if the recipient address exist
                try:
                      amount = wallet_address_dictionary[recipient_wallet_address]
                      return True         
                except KeyError:
                      return False

        # ensure the money only flow between the sender and the recipient
        def generate_transaction_code(sender_wallet_address: str, recipient_wallet_address: str, transaction_amount: int): # Generates a valid ID for transaction
               transaction_valid_token = binascii.b2a_hex(os.urandom(75)) # generates a 150 characters token
               current_transaction_token_array.append(transaction_valid_token) # append the transaction token into the waiting list
               current_transaction_dictionary[transaction_valid_token] = [sender_wallet_address, recipient_wallet_address, transaction_amount] 

        def process_current_transaction_dictionary(): # process transaction queue
               token = current_transaction_token_array.popleft()
               sender_address = current_transaction_dictionary[token][0]
               recipient_address = current_transaction_dictionary[token][1]
               transaction_amount = current_transaction_dictionary[token][2]
               return Transaction_system.send_money(sender_address, recipient_address, transaction_amount)

        def send_money(sender_wallet_address: str, recipient_wallet_address: str, transaction_amount: int): # Currency exchange
              wallet_address_dictionary[sender_wallet_address] = int(wallet_address_dictionary[sender_wallet_address]) - int(transaction_amount)
              wallet_address_dictionary[recipient_wallet_address] = int(wallet_address_dictionary[recipient_wallet_address]) + int(transaction_amount)
              print("Transaction Success!")
              print("New wallet address value:\n---------------------------------------------------------------------")
              for address, value in wallet_address_dictionary.items():
                    print(address, value)

class User():
        def new_wallet(username):
              user_new_wallet_address = binascii.b2a_hex(os.urandom(32)).decode(encoding="utf-8")
              user_wallet_dictionary[username].append(user_new_wallet_address)
            
              wallet_address_dictionary[user_new_wallet_address] = 0

              print(user_wallet_dictionary)

        def new_transaction(username: str, recipient: str, amount: int):
              print(user_wallet_dictionary[username]) # list
              # select wallet
              wallet = int(input("Please select which wallet will be used for this transaction(0-9)")) 
              sender_address = user_wallet_dictionary[username][wallet]
              Transaction_system.transaction_navigation(sender_address, recipient, amount)

User.new_wallet('Smith')
