from factories.wells_fargo import WellsFargoFactory
from factories.chase import ChaseFactory
from client import process_payment

if __name__ == "__main__":
    raw_data = {"amount": 150, "currency": "USD"}

    # Dependency injected gateway: Wells Fargo
    wf_factory = WellsFargoFactory()
    wf_response = process_payment(wf_factory, raw_data)
    print("Wells Fargo Response:", wf_response)

    # Dependency injected gateway: Chase
    chase_factory = ChaseFactory()
    chase_response = process_payment(chase_factory, raw_data)
    print("Chase Response:", chase_response)
