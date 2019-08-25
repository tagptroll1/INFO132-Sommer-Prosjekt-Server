import argparse

from app.site.api.data_endpoint import endpoints as data_endpoint
from app.site.api.dropdown_endpoint import endpoints as dropdown
from app.site.api.feedback_endpoint import endpoints as feedback_endpoint
from app.site.api.fill_in_endpoint import endpoints as fill_in
from app.site.api.multi_choice_endpoint import endpoints as multi_choice
from app.site.api.question_endpoint import endpoints as questionset
from app.site.manager import Manager

parser = argparse.ArgumentParser(
    description='Running the server.  -P / --production to disable debug',
)

parser.add_argument(
    "-P",
    '--production',
    action="store_false",
    default=True
)

manager = Manager()

endpoints = (
    dropdown,
    fill_in,
    multi_choice,
    data_endpoint,
    questionset,
    feedback_endpoint
)
manager.load_api_resources(endpoints)

if __name__ == "__main__":
    args = parser.parse_args()
    manager.run(debug=args.production)
