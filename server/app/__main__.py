from app.site.manager import Manager


manager = Manager()

if __name__ == "__main__":
    manager.load_api_resources()
    manager.run()
    ...
