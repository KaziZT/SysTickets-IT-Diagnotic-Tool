from Diagnostics.system_info import get_system_info

from Diagnostics.network_info import get_ip_address, ping_test

from Database.ticket_manager import create_database, create_ticket, view_tickets, update_ticket_status, search_tickets_by_user, filter_tickets_by_status

def show_menu():
    print("IT Support Diagnostic Tool\n")
    print("1. Run System Diagnostics")
    print("2. Run Network Diagnostics")
    print("3. Create Support Ticket")
    print("4. View Tickets")
    print("5. Update Ticket Status")
    print("6. Search Tickets by User")
    print("7. Filter Tickets by Status")
    print("8. Exit")

SYSTEM_DIAGNOSTIC = "1"
NETWORK_DIAGNOSTIC = "2"
CREATE_TICKET = "3"
VIEW_TICKETS = "4"
UPDATE_STATUS = "5"
SEARCH_BY_USER = "6"
FILTER_BY_STATUS = "7"
EXIT_OPTION = "8"

def print_ticket(t):
    print(f"""
ID: {t[0]}
User: {t[1]}
Issue: {t[2]}
Priority: {t[3]}
Status: {t[4]}
OS: {t[5]}
CPU: {t[6]}
Disk Free: {t[7]} GB
IP Address: {t[8]}
Internet: {t[9]}
Created: {t[10]}
-------------------------
""")

def main():
    is_valid = True
    create_database()
    while is_valid:
        show_menu()
        choice = input("Select an option: ")

        if choice == SYSTEM_DIAGNOSTIC:
            system_info = get_system_info()
            for key, value in system_info.items():
                print(f"{key}: {value}")
        elif choice == NETWORK_DIAGNOSTIC:
            print("IP Address:", get_ip_address())
            print("Internet Test (8.8.8.8):", ping_test("8.8.8.8"))
        elif choice == CREATE_TICKET:
            user = input("Enter user name: ")
            issue = input("Describe the issue: ")
            priority = input("Priority (Low/Medium/High): ").capitalize()

            system_info = get_system_info()
            diagnostics = {
                "OS": system_info.get("OS"),
                "Processor": system_info.get("Processor"),
                "Disk Free (GB)": system_info.get("Disk Free (GB)"),
                "IP Address": get_ip_address(),
                "Internet": ping_test("8.8.8.8")
            }

            create_ticket(user, issue, priority, diagnostics)
            print("Ticket created with diagnostics successfully.\n")
        elif choice == VIEW_TICKETS:
            tickets = view_tickets()
            if not tickets:
                print("No tickets found.\n")
            else:
                for t in tickets:
                    print_ticket(t)
                print()
        elif choice == UPDATE_STATUS:
            tickets = view_tickets()

            if not tickets:
                print("No tickets available.\n")
            else:
                for t in tickets:
                    print_ticket(t)

                ticket_id = input("\nEnter Ticket ID to update: ")
                new_status = input("New Status (Open / In Progress / Closed): ")

                update_ticket_status(ticket_id, new_status)
                print("Ticket updated successfully.\n")
        elif choice == SEARCH_BY_USER:
            name = input("Enter user name to search: ")
            results = search_tickets_by_user(name)

            if not results:
                print("No tickets found.\n")
            else:
                for t in results:
                    print_ticket(t)

        elif choice == FILTER_BY_STATUS:
            status = input("Enter status (Open / In Progress / Closed): ")
            results = filter_tickets_by_status(status)

            if not results:
                print("No tickets found.\n")
            else:
                for t in results:
                    print_ticket(t)
        elif choice == EXIT_OPTION:
            print("Exiting program.\n")
            is_valid = False
        else:
            print("Invalid choice. Try again.\n")

if __name__ == "__main__":
    main()