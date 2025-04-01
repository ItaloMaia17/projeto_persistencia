from fastapi import APIRouter

router = APIRouter(prefix="",tags=["Home"],)
@router.get("/Home")
async def root():
    return {"msg": "Bem-vindo a G&I_Tech!"}