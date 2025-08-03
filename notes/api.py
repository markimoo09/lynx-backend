from ninja import NinjaAPI

api = NinjaAPI()

@api.get("/")
def hello_world(request):
    return "Hello World"