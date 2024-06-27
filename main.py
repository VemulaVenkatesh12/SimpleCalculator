
import math
from fastapi import FastAPI, HTTPException, Body, Request
from pydantic import BaseModel, ValidationError
 
app = FastAPI()

# Define a Pydantic model for validation
class CalculationRequest(BaseModel):
    a: int | float
    b: int | float



def perform_operation(operation: str, a: float | int , b: float | int) -> float:
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        if b == 0:
            raise HTTPException(status_code=400, detail="Division by zero is not allowed")
        return a / b
    
    elif operation == "modulus":
        if b == 0:
            raise HTTPException(status_code=400, detail="Modulus by zero is not allowed")
        return a % b
    elif operation == "exponentiation":
        return a ** b
    elif operation == "floor_divide":
        if b == 0:
            raise HTTPException(status_code=400, detail="Floor division by zero is not allowed")
        return a // b
    elif operation == "square_root":
        if a < 0:
            raise HTTPException(status_code=400, detail="Cannot take square root of a negative number")
        return math.sqrt(a)
    else:
        raise HTTPException(status_code=400, detail="Invalid operation")
 
# Endpoint to handle calculation requests
@app.post("/calculate/{operation}")
async def calculate(operation: str,  body: dict = Body(...)):
    try:
        if len(body) != 2 or not all(key in body for key in ['a', 'b']):
            raise HTTPException(status_code=400, detail="Request body must contain exactly two key-value pairs 'a' and 'b'")
        calculation_request = CalculationRequest(**body)
        result = perform_operation(operation, calculation_request.a, calculation_request.b)
        return {"result": result}
    
    except ValidationError as e:
        raise HTTPException(status_code=400, detail="Validation error: {}".format(e))

