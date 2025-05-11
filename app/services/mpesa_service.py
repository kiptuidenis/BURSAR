import requests
import base64
from datetime import datetime
from flask import current_app
from ..models import Transaction, User

class MPESAService:
    def __init__(self):
        self.consumer_key = current_app.config['MPESA_CONSUMER_KEY']
        self.consumer_secret = current_app.config['MPESA_CONSUMER_SECRET']
        self.api_url = current_app.config['MPESA_API_URL']
        self.business_shortcode = current_app.config['MPESA_BUSINESS_SHORTCODE']
        self.passkey = current_app.config['MPESA_PASSKEY']
        self.security_credential = current_app.config['MPESA_SECURITY_CREDENTIAL']
        
    def _generate_auth_token(self):
        """Generate OAuth token for MPESA API"""
        auth_string = f"{self.consumer_key}:{self.consumer_secret}"
        auth_bytes = auth_string.encode("ascii")
        encoded_auth = base64.b64encode(auth_bytes).decode('ascii')
        
        headers = {
            'Authorization': f'Basic {encoded_auth}'
        }
        
        try:
            response = requests.get(
                f"{self.api_url}/oauth/v1/generate?grant_type=client_credentials",
                headers=headers
            )
            response.raise_for_status()
            return response.json()['access_token']
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"Error generating MPESA auth token: {str(e)}")
            raise

    def _generate_password(self):
        """Generate password for STK Push"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        string_to_encode = f"{self.business_shortcode}{self.passkey}{timestamp}"
        return base64.b64encode(string_to_encode.encode()).decode('utf-8'), timestamp
            
    def initiate_stk_push(self, phone_number, amount=0):
        """Initiate STK Push prompt to customer's phone"""
        token = self._generate_auth_token()
        password, timestamp = self._generate_password()
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            "BusinessShortCode": self.business_shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": str(amount),
            "PartyA": phone_number.replace('+', ''),
            "PartyB": self.business_shortcode,
            "PhoneNumber": phone_number.replace('+', ''),
            "CallBackURL": f"{current_app.config['BASE_URL']}/api/mpesa/stk/callback",
            "AccountReference": "Bursar Deposit",
            "TransactionDesc": "Deposit to Bursar account" 
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/mpesa/stkpush/v1/processrequest",
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            result = response.json()
            
            if result.get('ResponseCode') == '0':
                return {
                    'success': True,
                    'CheckoutRequestID': result.get('CheckoutRequestID')
                }
            
            return {
                'success': False,
                'error': result.get('ResponseDescription', 'Failed to initiate STK push')
            }
            
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"Error initiating STK push: {str(e)}")
            raise
            
    def check_stk_push_status(self, checkout_request_id):
        """Check the status of an STK Push request"""
        token = self._generate_auth_token()
        password, timestamp = self._generate_password()
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            "BusinessShortCode": self.business_shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "CheckoutRequestID": checkout_request_id
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/mpesa/stkpushquery/v1/query",
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            result = response.json()
            
            if result.get('ResponseCode') == '0':
                return {
                    'ResultCode': result.get('ResultCode'),
                    'ResultDesc': result.get('ResultDesc')
                }
            
            return {'pending': True}
            
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"Error checking STK push status: {str(e)}")
            raise
    
    def initiate_b2c_payment(self, phone_number, amount, reason="Daily Budget Transfer"):
        """Initiate Business to Customer (B2C) payment"""
        token = self._generate_auth_token()
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            "InitiatorName": "testapi",
            "SecurityCredential": self.security_credential,
            "CommandID": "BusinessPayment",
            "Amount": str(amount),
            "PartyA": self.business_shortcode,
            "PartyB": phone_number,
            "Remarks": reason,
            "QueueTimeOutURL": f"{current_app.config['BASE_URL']}/api/mpesa/timeout",
            "ResultURL": f"{current_app.config['BASE_URL']}/api/mpesa/result",
            "Occasion": ""
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/mpesa/b2c/v1/paymentrequest",
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            result = response.json()
            
            # Create transaction record
            transaction = Transaction(
                user_id=User.query.filter_by(phone_number=phone_number).first().id,
                amount=amount,
                type='credit',
                description=reason,
                mpesa_reference=result['ConversationID'],
                status='pending'
            )
            
            db.session.add(transaction)
            db.session.commit()
            
            return {
                'success': True,
                'transaction_id': transaction.id,
                'reference': result['ConversationID']
            }
            
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"Error initiating B2C payment: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
            
    def check_transaction_status(self, conversation_id):
        """Check the status of a B2C transaction"""
        token = self._generate_auth_token()
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            "Initiator": "testapi",
            "SecurityCredential": "your-security-credential",
            "CommandID": "TransactionStatusQuery",
            "TransactionID": conversation_id,
            "PartyA": "your-shortcode",
            "IdentifierType": "1",
            "ResultURL": f"{current_app.config['BASE_URL']}/api/mpesa/status/result",
            "QueueTimeOutURL": f"{current_app.config['BASE_URL']}/api/mpesa/status/timeout",
            "Remarks": "Transaction status check",
            "Occasion": ""
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/mpesa/transactionstatus/v1/query",
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"Error checking transaction status: {str(e)}")
            raise