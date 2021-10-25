import uuid
import json
import base64
import requests
import time

def log_info(school, url, est_id):
    with open("./info/names.txt", 'a') as f:
        content = {
            "name": school["result"]["establishment"]["name"],
            "api_url": url,
            "establishment_id": est_id,
            "external_login_only": school["result"]["establishment"]["idp_only"],
            "external_logins": school["result"]["establishment"]["idp_login"]
        }
        f.write(json.dumps(content) + '\n')
                
    filename = "./info/logos/" + school["result"]["establishment"]["name"] + ".png"
    image_data = base64.b64decode(school["result"]["establishment"]["logo"])
    with open(filename, "wb+") as f:
        f.write(image_data)


def main():
    for domain_no in range(1, 12):
        if domain_no == 1:
            domain_no = ""
        api_url = f"https://www{domain_no}.edulinkone.com/api/"
        url = api_url + "?method=EduLink.SchoolDetails"
        establishment_misses = 0
        for est_id in range(1, 100):
            params = json.dumps({
                "jsonrpc": "2.0",
                "method": "EduLink.SchoolDetails",
                "params": {
                    "establishment_id": str(est_id),
                    "from_app": False
                },
                "uuid": str(uuid.uuid4()),
                "id": "1"
            })
            headers = {
                    "X-API-Method": "EduLink.SchoolDetails",
                    "Content-Type": "application/json"
            }
            
            response = requests.post(url, data=params, headers=headers)
            time.sleep(0.2)

            if response.ok:
                res = response.json()
                if res["result"]["success"]:
                    print(res["result"]["establishment"]["name"])
                    log_info(res, api_url, est_id)
                else:
                    establishment_misses += 1
            else:
                print("\tHTTP error")

            if est_id > 5 and establishment_misses > 5: # Avoiding rate limits
                break

                
if __name__ == "__main__":
    main()
