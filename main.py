from fastapi import FastAPI, Path, Query, HTTPException
import json

app = FastAPI()

def load_data(): 
    with open('patients.json', 'r') as f:
        data = json.load(f)
    return data

@app.get("/")
def hello():
    return { 'message': "Hello" }

@app.get('/about')
def about():
    return { 'message': "Subham is very powerful" }

@app.get('/view')
def view():
    data = load_data()
    return data

@app.get('/patient/{patientId}')
def view_patient(patientId: str = Path(..., description = 'Patient ID Needed', example = 'P001')):
    data = load_data()
    if patientId in data:
        return data[patientId]
    else:
        return { 'status': 404, 'message': "Doesn't exist" }
    

@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description='Sort on the basis of height, weight or bmi'), order: str = Query('asc', description='sort in asc or desc order')):
    valid_fields = ['height', 'weight', 'bmi']
    if(sort_by not in valid_fields):
        raise HTTPException(status_code=400, detail=f'Invalid field select from {valid_fields}' )
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order')
    
    data = load_data()
    sort_order = True if order=='desc' else False
    sorted_data = sorted(data.values(), key=lambda x:x.get(sort_by, 0), reverse=sort_order)

