# M-Pesa Integration Setup Guide

This guide explains how to set up the M-Pesa integration for deposits in the Bursar application.

## Prerequisites

1. M-Pesa Developer Account (Safaricom Developer Portal)
2. ngrok account for local testing

## Setup Instructions

### 1. Configure Environment Variables

Edit the `.env` file in the project root to include your M-Pesa API credentials:

```
MPESA_CONSUMER_KEY=your_consumer_key
MPESA_CONSUMER_SECRET=your_consumer_secret
MPESA_API_URL=https://sandbox.safaricom.co.ke
MPESA_BUSINESS_SHORTCODE=your_shortcode
MPESA_PASSKEY=your_passkey
MPESA_SECURITY_CREDENTIAL=your_security_credential
BASE_URL=http://localhost:5000
```

### 2. Set Up ngrok for Local Testing

1. Download and install ngrok from [ngrok.com](https://ngrok.com/)
2. Run ngrok to create a tunnel to your local Flask server:

```
ngrok http 5000
```

3. The Bursar application will automatically detect the ngrok URL and use it for callbacks.

### 3. Testing Deposits

1. Start the Flask application:

```
flask run
```

2. Log in to your Bursar account
3. Click the "Deposit" button on the dashboard
4. You should receive an M-Pesa STK Push on your phone
5. Complete the payment on your phone
6. The deposit should be reflected in your Bursar account

## Troubleshooting

- Check the Flask application logs for detailed error messages
- Verify that your M-Pesa API credentials are correct
- Ensure your phone number is registered with M-Pesa
- For sandbox testing, make sure you're using the test credentials from the Safaricom Developer Portal
