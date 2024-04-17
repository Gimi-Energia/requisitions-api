import json


def load_json_file(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


def format_user_data(user):
    email = user["Email Address [Required]"]
    name = email.split("@")[0].capitalize()
    domain = email.split("@")[1]

    if "gimi.com.br" in domain:
        company = "Gimi"
    elif "gimibonomi.com.br" in domain:
        company = "GBL"
    elif "gimipogliano.com.br" in domain:
        company = "GPB"
    else:
        company = "Gimi"

    password = f"{name}#3530"

    return {
        "model": "users.user",
        "fields": {
            "email": email,
            "name": name,
            "company": company,
            "type": "Requester",
            "password": password,
        },
    }


def create_fixture_from_json(file_path, output_file):
    data = load_json_file(file_path)
    users = data["users"]
    formatted_users = [format_user_data(user) for user in users]

    with open(output_file, "w") as f:
        json.dump(formatted_users, f, indent=4)


fixture = create_fixture_from_json("export_google.json", "requesters.json")
