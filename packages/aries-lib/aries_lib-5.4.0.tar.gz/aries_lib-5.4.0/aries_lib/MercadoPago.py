import re
import mercadopago
from datetime import datetime

__all__ = (
    "MercadoPago"
)

class Verify():
    def Name(name: str):
        if re.match(r'^[A-Za-zÁ-ú]{3,}(?: [A-Za-zÁ-ú]{3,})?$',name):
            return True

        return False   

    def SurName(surname: str):
        if re.match(r'^[A-Za-zÁ-ú]{3,}$',surname):
            return True

        return False   

    def Email(email: str):
        if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$',email):
            
            if email.split('@')[1].split('.')[0] in ['gmail', 'outlook', 'yahoo', 'hotmail']:
                return True

        return False     
    

class MercadoPago():
    def __init__(self, token):
        self.token = token
        self.acess_granted = False
        self.sdk = mercadopago.SDK(self.token)
        self.payment = self.sdk.payment()
        self.user = {
            "first_name": None,
            "second_name": None,
            "email": None
        }

    def Data(self, user: dict) -> None:
        """   
        Add the user information
        
        params:
            USER = Require[dict]
                first_name -> Require[str]
                second_name -> Require[str]
                email -> Require[str]
        """

        required = {
            "first_name": Verify.Name,
            "second_name": Verify.SurName,
            "email": Verify.Email
        }

        for requirement, function in required.items():
            if not requirement in user:
                raise ValueError(f"{requirement} not specified")

            if not function(user[requirement]):
                raise ValueError(f"{requirement} must be valid")

            self.user[requirement] = user[requirement]
        
        self.acess_granted = True

    def PaymentPix(self, price: int = 1, product: str = "Unknown", amount: int = 1) -> dict:
        """   
        Create a pix payment 

        params: 
            price -> Require[int]
            product -> Require[int]
            amount -> Require[int]
        """

        if not self.acess_granted:
            raise ResourceWarning("Need use MercadoPago.Data(**args) first")
        
        payment_data = {
            "transaction_amount": price,
            "description": product,
            "payment_method_id": 'pix',
            "payer": {
                "email": self.user["email"],
                "first_name": f"{self.user['first_name']} {self.user['second_name']}"
            }
        }

        payment_response = self.payment.create(payment_data)
        payment = payment_response["response"]

        if int(payment_response["status"]) < 200 or int(payment_response["status"]) > 299:
            return {
                "error": payment_response["response"]["message"]
            }

        return {
            "id": payment["id"],
            "url": payment["point_of_interaction"]["transaction_data"]["ticket_url"],
            "qrcode": payment["point_of_interaction"]["transaction_data"]["qr_code"],
            "qrcode_base64": payment["point_of_interaction"]["transaction_data"]["qr_code_base64"]
        }
    
    def GetStatus(self, payment_id: int):
        """   
        Get payment status

        params: 
            payment_id -> Require[int]
        """

        query = self.payment.get(payment_id)
        
        if int(query["status"]) < 200 or int(query["status"]) > 299:
            return {
                "error": query["response"]["message"]
            }

        return query["response"]["status"]
