from app.site.manager import Manager
from app.site.api.dropdown_endpoint import endpoints as dropdown
from app.site.api.fill_in_endpoint import endpoints as fill_in
from app.site.api.multi_choice_endpoint import endpoints as multi_choice
from app.site.api.data_endpoint import endpoints as data_endpoint


manager = Manager()

if __name__ == "__main__":
    endpoints = (dropdown, fill_in, multi_choice, data_endpoint)
    manager.load_api_resources(endpoints)
    manager.run()
