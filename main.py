import os
from services.auth_service import AuthService, SUPERUSER
from services.user_service import UserService
from services.trip_service import TripService
from services.ticket_service import TicketService
from services.admin_service import AdminService
from exceptions import AuthenticationError, InsufficientFundsError, TicketCancellationError

auth_service = AuthService()
user_service = UserService()
trip_service = TripService()
ticket_service = TicketService()
admin_service = AdminService()

current_user = None

def clear_screen():
    os.system('cls' if os.name=='nt' else 'clear')

def show_main_menu():
    clear_screen()
    print("==== Bus Terminal System ====")
    print("1. Register")
    print("2. Login")
    print("3. Admin Login")
    print("4. View Available Trips")
    print("0. Exit")

def show_user_menu():
    clear_screen()
    print(f"==== User Dashboard ({current_user.username}) ====")
    print("1. Add Funds")
    print("2. View Balance")
    print("3. View Available Trips")
    print("4. Reserve Ticket")
    print("5. Pay for Reserved Ticket")
    print("6. Buy Ticket (Direct Payment)")
    print("7. View My Tickets")
    print("8. Cancel Ticket")
    print("9. Logout")

def show_admin_menu():
    clear_screen()
    print(f"==== Admin Dashboard ({current_user.username}) ====")
    print("1. View Total Income")
    print("2. View Trip Income")
    print("3. View Stats")
    print("4. Transactions Report")
    print("0. Logout")

def main():
    global current_user
    while True:
        if not current_user:
            show_main_menu()
            choice = input("Choose an option: ")
            if choice=="1":
                username = input("Enter username: ")
                password = input("Enter password: ")
                try:
                    auth_service.register(username, password)
                    print(" Registration successful!")
                except AuthenticationError as e:
                    print(f" {e}")
                input("Press Enter to continue...")
            elif choice=="2":
                username = input("Enter username: ")
                password = input("Enter password: ")
                try:
                    current_user = auth_service.login(username, password)
                    print(" Login successful!")
                except AuthenticationError as e:
                    print(f" {e}")
                    input("Press Enter to continue...")
            elif choice=="3":
                username = input("Enter admin username: ")
                password = input("Enter admin password: ")
                try:
                    current_user = auth_service.login(username, password)
                    if current_user.username != SUPERUSER:
                        print(" Not an admin!")
                        current_user = None
                        input("Press Enter to continue...")
                except AuthenticationError as e:
                    print(f" {e}")
                    input("Press Enter to continue...")
            elif choice=="4":
                trips = trip_service.list_available_trips()
                print("Available Trips:")
                for t in trips:
                    print(f"Trip ID: {t[0]} | Destination: {t[1]} | Cost: {t[2]} | Available Seats: {t[3]}")
                input("Press Enter to continue...")
            elif choice=="0":
                break
        else:
            if getattr(current_user,'username','')==SUPERUSER:
                show_admin_menu()
                choice = input("Choose an option: ")
                if choice=="1":
                    admin_service.total_income()
                    input("Press Enter to continue...")
                elif choice=="2":
                    trip_id = int(input("Enter Trip ID: "))
                    admin_service.trip_income(trip_id)
                    input("Press Enter to continue...")
                elif choice=="3":
                    admin_service.stats()
                    input("Press Enter to continue...")
                elif choice=="4":
                    admin_service.report_transactions()
                    input("Press Enter to continue...")
                elif choice=="0":
                    current_user = None
            else:
                show_user_menu()
                choice = input("Choose an option: ")
                if choice=="1":
                    try:
                        amount = float(input("Enter amount to add: "))
                        user_service.add_funds(current_user.id, amount)
                        print(" Funds added!")
                    except ValueError:
                        print(" Invalid amount")
                    input("Press Enter to continue...")
                elif choice=="2":
                    balance = user_service.get_balance(current_user.id)
                    print(f"💰 Your balance: {balance}")
                    input("Press Enter to continue...")
                elif choice=="3":
                    trips = trip_service.list_available_trips()
                    print("Available Trips:")
                    for t in trips:
                        print(f"Trip ID: {t[0]} | Destination: {t[1]} | Cost: {t[2]} | Available Seats: {t[3]}")
                    input("Press Enter to continue...")
                elif choice=="4":
                    try:
                        trip_id = int(input("Enter Trip ID to reserve: "))
                        ticket_id = ticket_service.reserve_ticket(current_user.id, trip_id)
                        print(f" Ticket reserved! Ticket ID: {ticket_id}")
                    except Exception as e:
                        print(f" {e}")
                    input("Press Enter to continue...")
                elif choice=="5":
                    try:
                        ticket_id = int(input("Enter Reserved Ticket ID to pay: "))
                        ticket_service.pay_for_reserved_ticket(ticket_id, current_user.id)
                        print(" Payment successful!")
                    except Exception as e:
                        print(f" {e}")
                    input("Press Enter to continue...")
                elif choice=="6":
                    try:
                        trip_id = int(input("Enter Trip ID to buy ticket: "))
                        ticket_id = ticket_service.buy_ticket(current_user.id, trip_id)
                        print(f" Ticket purchased! Ticket ID: {ticket_id}")
                    except (InsufficientFundsError, Exception) as e:
                        print(f" {e}")
                    input("Press Enter to continue...")
                elif choice=="7":
                    tickets = ticket_service.list_tickets_for_user(current_user.id)
                    print("My Tickets:")
                    for t in tickets:
                        print(f"Ticket ID: {t[0]} | Destination: {t[1]} | Seat: {t[2]} | Status: {t[3]}")
                    input("Press Enter to continue...")
                elif choice=="8":
                    try:
                        ticket_id = int(input("Enter Ticket ID to cancel: "))
                        refund = ticket_service.cancel_ticket(ticket_id, current_user.id)
                        print(f" Ticket cancelled! Refund: {refund}")
                    except TicketCancellationError as e:
                        print(f"{e}")
                    input("Press Enter to continue...")
                elif choice=="9":
                    current_user = None

if __name__=="__main__":
    main()