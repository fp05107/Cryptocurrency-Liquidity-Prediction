from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional, Annotated


class Patient(BaseModel):

    name: Annotated[str, Field(max_length=50, title="Name of Patient", description="Less than 50 characters" )]
    email: EmailStr
    linkedin_url: AnyUrl
    age: int
    weight: float = Field(gt=0, lt=120)
    married: bool = False
    allergies: Optional[List[str]] = Field(max_length=5)
    contact_details: Dict[str, str]



def insert_patient_data(patient: Patient):

    print(patient.name)
    print(patient.age)
    print(patient.married)
    print(patient.allergies)
    print(patient.weight)
    print(patient.contact_details)


patient_info = { 'name': 'Subu', 'email': 'Helloy@aho.com', 'age':22, 'weight': 40.4, 'married': True,
                'allergies': ["Hello"], 'contact_details': { 'phone': '6371238379' } }

patient1 = Patient(**patient_info)

insert_patient_data(patient1)
