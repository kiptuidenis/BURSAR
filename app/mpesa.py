"""
M-Pesa integration module for Bursar application
This module provides helper functions for M-Pesa integration
"""
from flask import current_app
from .services.mpesa_service import MPESAService

def initiate_deposit(phone_number, amount=10):
    """
    Initiate an M-Pesa STK push for deposit
    
    Args:
        phone_number (str): The phone number to send the STK push to
        amount (int): The amount to deposit (minimum 10 KES)
        
    Returns:
        dict: The result of the STK push request
    """
    mpesa_service = MPESAService()
    return mpesa_service.initiate_stk_push(phone_number, amount)

def check_deposit_status(checkout_request_id):
    """
    Check the status of an M-Pesa STK push request
    
    Args:
        checkout_request_id (str): The checkout request ID from the STK push
        
    Returns:
        dict: The status of the STK push request
    """
    mpesa_service = MPESAService()
    return mpesa_service.check_stk_push_status(checkout_request_id)

def format_phone_number(phone_number):
    """
    Format a phone number for M-Pesa API
    
    Args:
        phone_number (str): The phone number to format
        
    Returns:
        str: The formatted phone number
    """
    # Remove any leading + if present
    phone = phone_number.replace('+', '')
    
    # If the number starts with 0, replace it with 254
    if phone.startswith('0'):
        phone = '254' + phone[1:]
    
    # If the number doesn't start with 254, add it
    if not phone.startswith('254'):
        phone = '254' + phone
        
    return phone
