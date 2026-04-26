from fastapi import APIRouter
from .dashboard_utils import generate_dashboard_insights

router = APIRouter()

@router.get("/dashboard")
def dashboard():
    return {"insights": generate_dashboard_insights()}