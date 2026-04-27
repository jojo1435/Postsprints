from app import app

from source.seeds.plans import seed_plans

def menu():
    print("\n=== FLASK SQLALCHEMY SEED MENU ===")
    print("1) Seed Plans")
    print("0) Exit")

def run_seed(option):
    if option == "1":
        seed_plans()

    elif option == "0":
        print("Closing")
        return False

    else:
        print("Invalid option")

    return True

with app.app_context():

    running = True

    while running:
        menu()
        option = input("Select an option: ")
        running = run_seed(option)