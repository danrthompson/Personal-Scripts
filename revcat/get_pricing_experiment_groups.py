import requests
import json

# Configuration
REVENUECAT_API_KEY = "sk_htJhFOuVJgjtBPpnAnyOgxjIDvxrL"
REVENUECAT_ENDPOINT = "https://api.revenuecat.com/v1/subscribers"
# MIXPANEL_TOKEN = "your_mixpanel_project_token"


# Fetch user data from RevenueCat
def fetch_revenuecat_data():
    headers = {
        "Authorization": f"Bearer {REVENUECAT_API_KEY}",
    }

    response = requests.get(REVENUECAT_ENDPOINT, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(
            f"Error fetching data from RevenueCat: {response.status_code} - {response.text}"
        )


# Example of handling the data
def process_user_data(user_data):
    users = user_data.get("subscribers", {})

    for user_id, user_info in users.items():
        pricing_group = (
            user_info.get("entitlements", {})
            .get("your_entitlement_identifier", {})
            .get("pricing_group", "unknown")
        )
        # Here you can add more logic to handle other user attributes if needed
        print(f"User ID: {user_id}, Pricing Group: {pricing_group}")


# Main script
if __name__ == "__main__":
    user_data = fetch_revenuecat_data()
    process_user_data(user_data)
