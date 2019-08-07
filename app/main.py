import argparse

from flask import Flask

from app.site.manager import Manager
from app.site.api.dropdown_endpoint import endpoints as dropdown
from app.site.api.fill_in_endpoint import endpoints as fill_in
from app.site.api.multi_choice_endpoint import endpoints as multi_choice
from app.site.api.data_endpoint import endpoints as data_endpoint


parser = argparse.ArgumentParser(
    description='Running the server.  -P / --production to disable debug',
)

parser.add_argument(
     "-P", '--production', 
    action="store_false",
    default=True
)

flask_app = Flask(__name__)
manager = Manager(flask_app)

if __name__ == "__main__":
    endpoints = (dropdown, fill_in, multi_choice, data_endpoint)
    manager.load_api_resources(endpoints)

    args = parser.parse_args()
    manager.run(debug=args.production)
