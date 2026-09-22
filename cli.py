import argparse
import sys
from tracker import ExpenseTracker

def main():
    parser = argparse.ArgumentParser(description="Expense Tracker CLI Tool")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new transaction")
    add_parser.add_argument("--title", "-t", required=True, help="Transaction title")
    add_parser.add_argument("--amount", "-a", type=float, required=True, help="Amount")
    add_parser.add_argument("--type", choices=["Expense", "Income"], default="Expense", help="Transaction type")
    add_parser.add_argument("--category", "-c", default="Miscellaneous", help="Category name")
    add_parser.add_argument("--date", "-d", help="Date (YYYY-MM-DD), default is today")
    add_parser.add_argument("--payment", "-p", default="Cash", help="Payment method (Cash, Credit Card, etc.)")
    add_parser.add_argument("--note", "-n", default="", help="Optional note")

    # List command
    list_parser = subparsers.add_parser("list", help="List transactions")
    list_parser.add_argument("--category", "-c", help="Filter by category")
    list_parser.add_argument("--type", choices=["Expense", "Income", "All"], help="Filter by type")
    list_parser.add_argument("--search", "-s", help="Search keyword")
    list_parser.add_argument("--limit", "-l", type=int, default=20, help="Max items to list")

    # Delete command
    del_parser = subparsers.add_parser("delete", help="Delete a transaction by ID")
    del_parser.add_argument("id", type=int, help="Transaction ID")

    # Summary command
    subparsers.add_parser("summary", help="Show financial summary and analytics")

    # Budget command
    budget_parser = subparsers.add_parser("budget", help="View or set category budget limits")
    budget_parser.add_argument("--set", action="store_true", help="Set budget mode")
    budget_parser.add_argument("--category", "-c", help="Category name")
    budget_parser.add_argument("--limit", "-l", type=float, help="Monthly budget limit")

    # Export command
    export_parser = subparsers.add_parser("export", help="Export data to CSV or JSON")
    export_parser.add_argument("--format", choices=["csv", "json"], default="csv", help="Export format")
    export_parser.add_argument("--output", "-o", required=True, help="Output file path")

    # Import command
    import_parser = subparsers.add_parser("import", help="Import data from CSV or JSON")
    import_parser.add_argument("--format", choices=["csv", "json"], default="csv", help="Import format")
    import_parser.add_argument("--input", "-i", required=True, help="Input file path")

    args = parser.parse_args()

    tracker = ExpenseTracker()

    if args.command == "add":
        trans_id = tracker.add_transaction(
            title=args.title,
            amount=args.amount,
            trans_type=args.type,
            category=args.category,
            date=args.date,
            payment_method=args.payment,
            note=args.note
        )
        print(f" Successfully added {args.type} #{trans_id}: {args.title} (${args.amount:.2f})")

    elif args.command == "list":
        transactions = tracker.get_transactions(
            category=args.category,
            trans_type=args.type,
            search=args.search,
            limit=args.limit
        )
        if not transactions:
            print("No transactions found.")
            return

        print(f"\n{'ID':<5} {'Date':<12} {'Type':<8} {'Category':<18} {'Amount':<10} {'Title':<25}")
        print("-" * 80)
        for t in transactions:
            symbol = "+" if t['type'] == 'Income' else "-"
            print(f"{t['id']:<5} {t['date']:<12} {t['type']:<8} {t['category']:<18} {symbol}${t['amount']:<9.2f} {t['title']:<25}")

    elif args.command == "delete":
        success = tracker.delete_transaction(args.id)
        if success:
            print(f" Deleted transaction #{args.id}.")
        else:
            print(f" Transaction #{args.id} not found.")

    elif args.command == "summary":
        summary = tracker.get_summary()
        print("\n================ FINANCIAL SUMMARY ================")
        print(f" Total Income:  ${summary['total_income']:.2f}")
        print(f" Total Expense: ${summary['total_expense']:.2f}")
        print(f" Net Balance:   ${summary['net_balance']:.2f}")
        print(f" Savings Rate:  {summary['savings_rate']:.1f}%")
        print("--------------------------------------------------")
        print(" Expenses by Category:")
        for cat, total in summary['by_category'].items():
            print(f"  - {cat:<20}: ${total:.2f}")
        print("==================================================\n")

    elif args.command == "budget":
        if args.set:
            if not args.category or args.limit is None:
                print("Error: --category and --limit are required when setting a budget.")
                return
            tracker.set_budget(args.category, args.limit)
            print(f" Budget for '{args.category}' set to ${args.limit:.2f}/month.")
        else:
            budgets = tracker.get_budgets()
            print("\n================ CATEGORY BUDGETS ================")
            print(f"{'Category':<20} {'Spent':<10} {'Limit':<10} {'% Spent':<10} {'Status':<10}")
            print("-" * 65)
            for b in budgets:
                status = " OVER" if b['is_over'] else "OK"
                print(f"{b['category']:<20} ${b['spent']:<9.2f} ${b['monthly_limit']:<9.2f} {b['percentage']:<9.1f}% {status:<10}")
            print("==================================================\n")

    elif args.command == "export":
        if args.format == "csv":
            count = tracker.export_csv(args.output)
        else:
            count = tracker.export_json(args.output)
        print(f" Exported {count} transactions to {args.output}")

    elif args.command == "import":
        if args.format == "csv":
            count = tracker.import_csv(args.input)
        else:
            count = tracker.import_json(args.input)
        print(f" Imported {count} transactions from {args.input}")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
