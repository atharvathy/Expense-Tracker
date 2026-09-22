import sys
import os

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "cli":
        # Remove 'cli' from argv so argparse parses remaining args
        sys.argv.pop(1)
        import cli
        cli.main()
    else:
        print(" Starting ExpenseTracker Web Dashboard...")
        print(" Server running on http://127.0.0.1:5000 (Press Ctrl+C to quit)")
        from app import app
        app.run(host="127.0.0.1", port=5000, debug=True)

if __name__ == "__main__":
    main()
