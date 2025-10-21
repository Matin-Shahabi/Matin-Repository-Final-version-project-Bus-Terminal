import argparse
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

def main():
    parser = argparse.ArgumentParser(description="Bus Terminal CLI")
    subparsers = parser.add_subparsers(dest="command")

    # ------------------ Register ------------------
    reg_parser = subparsers.add_parser("register")
    reg_parser.add_argument("--username", required=True)
    reg_parser.add_argument("--password", required=True)

    # ------------------ Login ------------------
    login_parser = subparsers.add_parser("login")
    login_parser.add_argument("--username", required=True)
    login_parser.add_argument("--password", required=True)

    # ------------------ Add Funds ------------------
    addfund_parser = subparsers.add_parser("add_funds")
    addfund_parser.add_argument("--user_id", type=int, required=True)
    addfund_parser.add_argument("--amount", type=float, required=True)

    # ------------------ View Balance ------------------
    balance_parser = subparsers.add_parser("balance")
    balance_parser.add_argument("--user_id", type=int, required=True)

    # ------------------ List Trips ------------------
    trips_parser = subparsers.add_parser("list_trips")

    # ------------------ Buy Ticket ------------------
    buy_parser = subparsers.add_parser("buy_ticket")
    buy_parser.add_argument("--user_id", type=int, required=True)
    buy_parser.add_argument("--trip_id", type=int, required=True)

    # ------------------ Cancel Ticket ------------------
    cancel_parser = subparsers.add_parser("cancel_ticket")
    cancel_parser.add_argument("--user_id", type=int, required=True)
    cancel_parser.add_argument("--ticket_id", type=int, required=True)

    # ------------------ Admin Commands ------------------
    total_parser = subparsers.add_parser("total_income")
    trip_parser = subparsers.add_parser("trip_income")
    trip_parser.add_argument("--trip_id", type=int, required=True)
    stats_parser = subparsers.add_parser("stats")

    args = parser.parse_args()

    try:
        if args.command == "register":
            auth_service.register(args.username, args.password)
            print(f" User {args.username} registered successfully!")

        elif args.command == "login":
            user = auth_service.login(args.username, args.password)
            print(f" Logged in as {user.username}")

        elif args.command == "add_funds":
            user_service.add_funds(args.user_id, args.amount)
            print(f" Added {args.amount} to user {args.user_id}")

        elif args.command == "balance":
            balance = user_service.get_balance(args.user_id)
            print(f" User {args.user_id} balance: {float(balance):.2f}")

        elif args.command == "list_trips":
            trips = trip_service.list_available_trips()
            print("Available Trips:")
            for t in trips:
                print(f"Trip ID: {t[0]} | Destination: {t[1]} | Cost: {t[2]} | Available Seats: {t[3]}")

        elif args.command == "buy_ticket":
            ticket_id = ticket_service.buy_ticket(args.user_id, args.trip_id)
            print(f" =====Ticket purchased! Ticket ID: {ticket_id}")

        elif args.command == "cancel_ticket":
            refund = ticket_service.cancel_ticket(args.ticket_id, args.user_id)
            print(f"===== Ticket cancelled! Refund: {refund:.2f}")

        elif args.command == "total_income":
            admin_service.total_income()

        elif args.command == "trip_income":
            admin_service.trip_income(args.trip_id)

        elif args.command == "stats":
            admin_service.stats()

        else:
            parser.print_help()

    except (AuthenticationError, InsufficientFundsError, TicketCancellationError) as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()