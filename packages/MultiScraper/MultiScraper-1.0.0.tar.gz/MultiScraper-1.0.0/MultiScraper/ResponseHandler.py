def about_response_message(response_code):
    if response_code == 200:
        print("Success: The request was successful.")
    elif response_code == 400:
        print("Bad Request: The server could not understand the request. Check your request parameters.")
    elif response_code == 401:
        print("Unauthorized: The request requires user authentication. Make sure you include valid credentials.")
    elif response_code == 403:
        print("Forbidden: The server refused to fulfill the request. Verify your access permissions.")
    elif response_code == 404:
        print("Not Found: The requested resource was not found. Check the URL or resource identifier.")
    elif response_code == 500:
        print("Internal Server Error: The server encountered an unexpected condition. Try again later.")
    else:
        print(f"Unknown Response Code: {response_code}. Check the API documentation for the correct response codes.")