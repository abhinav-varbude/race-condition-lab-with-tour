from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from app.account import Account

app = FastAPI(title="Simulated Payment Service")

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def dashboard():
    """Serves the guided-tour lab dashboard."""
    return FileResponse("static/index.html")

# One shared in-memory account for this demo, starting with 100.0
account = Account(starting_balance=100.0)


class WithdrawRequest(BaseModel):
    amount: float


@app.post("/withdraw")
def withdraw(req: WithdrawRequest):
    if req.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    success = account.withdraw(req.amount)
    if not success:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    return {"success": True, "balance": account.get_balance()}


@app.get("/balance")
def balance():
    return {"balance": account.get_balance()}


@app.post("/reset")
def reset(starting_balance: float = 100.0):
    """Test-only helper to reset account state between test runs."""
    account.balance = starting_balance
    return {"balance": account.balance}
