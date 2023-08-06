# App Name

## Description
This code provides functionality to authenticate with Facebook and retrieve user data using the Facebook Graph API.

## Prerequisites
- Python 3.x installed
- Facebook Developer Account
- Facebook App created
- Select the fields you want to get from the profiles

## Usage
1. Open the `facebook.py` file in a text editor.
2. Update the following fields with your app details:
   - `access_token`: Replace with your Facebook access token.
   - `appSecret`: Replace with your Facebook app secret.
   - `app_id`: Replace with your Facebook app ID.
   - `appUri`: Replace with your Facebook app redirect URI.
3. Update in db classes database details

## Authentication
1. In the `facebook.py` file, locate the `authenticate_and_get_token` function.
2. Run the code to obtain the authorization URL: `python facebook.py`.
3. Copy the authorization URL displayed in the terminal and open it in a browser.
4. Log in to Facebook with the desired user account and authorize the app.
5. After authorization, you will be redirected to a URL with the authorization code.
6. Copy the authorization code from the URL and paste it into the terminal.
7. The code will exchange the authorization code for an access token.

## Retrieving User Data
1. run main.py
2. Write your desired fields to get.



