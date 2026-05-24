from ninja import NinjaAPI, Router

api = NinjaAPI()
router = Router()

@router.get("/hello")
def hello(request):
    return {"message": "hello"}

api.add_router("", router)  # router připojený na root api