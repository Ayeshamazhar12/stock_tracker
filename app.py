"""
Stock Portfolio Tracker
A simple application to track stock investments and calculate total portfolio value.
"""

import os
import csv
from datetime import datetime


# Hardcoded stock prices
STOCK_PRICES = {
    "AAPL": 180.50,
    "TSLA": 250.75,
    "GOOGL": 140.25,
    "MSFT": 380.45,
    "AMZN": 175.80,
    "META": 320.15,
    "NVDA": 875.30,
    "AMD": 165.90
}


def display_available_stocks():
    """Display all available stocks and their prices."""
    print("\n" + "="*50)
    print("AVAILABLE STOCKS")
    print("="*50)
    print(f"{'Stock Symbol':<15} {'Price ($)':<15}")
    print("-"*50)
    for symbol, price in sorted(STOCK_PRICES.items()):
        print(f"{symbol:<15} ${price:<14.2f}")
    print("="*50)


def get_valid_stock_input():
    """Get stock symbol from user with validation."""
    while True:
        stock = input("\nEnter stock symbol (or 'QUIT' to finish): ").upper().strip()
        
        if stock == "QUIT":
            return None
        
        if stock in STOCK_PRICES:
            return stock
        else:
            print(f"❌ '{stock}' not found. Available stocks: {', '.join(STOCK_PRICES.keys())}")


def get_valid_quantity_input():
    """Get quantity from user with validation."""
    while True:
        try:
            quantity = float(input("Enter quantity: "))
            if quantity <= 0:
                print("❌ Quantity must be greater than 0.")
                continue
            return quantity
        except ValueError:
            print("❌ Invalid input. Please enter a valid number.")


def build_portfolio():
    """Build portfolio by collecting stock information from user."""
    portfolio = {}
    
    print("\n" + "="*50)
    print("STOCK PORTFOLIO TRACKER")
    print("="*50)
    
    display_available_stocks()
    print("\nAdd stocks to your portfolio:")
    
    while True:
        stock = get_valid_stock_input()
        if stock is None:
            break
        
        quantity = get_valid_quantity_input()
        
        # Add or update stock in portfolio
        if stock in portfolio:
            portfolio[stock] += quantity
            print(f"✓ Updated {stock}: total quantity now = {portfolio[stock]}")
        else:
            portfolio[stock] = quantity
            print(f"✓ Added {stock}: {quantity} shares")
    
    return portfolio


def calculate_portfolio_value(portfolio):
    """Calculate total investment value and breakdown."""
    if not portfolio:
        return 0, {}
    
    breakdown = {}
    total_value = 0
    
    for stock, quantity in portfolio.items():
        stock_value = quantity * STOCK_PRICES[stock]
        breakdown[stock] = {
            "quantity": quantity,
            "price_per_share": STOCK_PRICES[stock],
            "total_value": stock_value
        }
        total_value += stock_value
    
    return total_value, breakdown


def display_portfolio_summary(portfolio, total_value, breakdown):
    """Display portfolio summary with detailed breakdown."""
    print("\n" + "="*60)
    print("PORTFOLIO SUMMARY")
    print("="*60)
    print(f"{'Stock':<10} {'Quantity':<12} {'Price/Share':<15} {'Total Value':<15}")
    print("-"*60)
    
    for stock in sorted(breakdown.keys()):
        data = breakdown[stock]
        print(f"{stock:<10} {data['quantity']:<12.2f} "
              f"${data['price_per_share']:<14.2f} ${data['total_value']:<14.2f}")
    
    print("-"*60)
    print(f"{'TOTAL INVESTMENT VALUE':<37} ${total_value:,.2f}")
    print("="*60)


def save_to_txt(portfolio, total_value, breakdown, filename="portfolio.txt"):
    """Save portfolio to a text file."""
    try:
        with open(filename, 'w') as f:
            f.write("="*60 + "\n")
            f.write("STOCK PORTFOLIO REPORT\n")
            f.write("="*60 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write(f"{'Stock':<10} {'Quantity':<12} {'Price/Share':<15} {'Total Value':<15}\n")
            f.write("-"*60 + "\n")
            
            for stock in sorted(breakdown.keys()):
                data = breakdown[stock]
                f.write(f"{stock:<10} {data['quantity']:<12.2f} "
                       f"${data['price_per_share']:<14.2f} ${data['total_value']:<14.2f}\n")
            
            f.write("-"*60 + "\n")
            f.write(f"{'TOTAL INVESTMENT VALUE':<37} ${total_value:,.2f}\n")
            f.write("="*60 + "\n")
        
        print(f"✓ Portfolio saved to '{filename}'")
        return True
    except IOError as e:
        print(f"❌ Error saving file: {e}")
        return False


def save_to_csv(portfolio, total_value, breakdown, filename="portfolio.csv"):
    """Save portfolio to a CSV file."""
    try:
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # Write header
            writer.writerow(["Stock Portfolio Report"])
            writer.writerow([f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"])
            writer.writerow([])
            
            # Write column headers
            writer.writerow(["Stock", "Quantity", "Price per Share", "Total Value"])
            
            # Write data
            for stock in sorted(breakdown.keys()):
                data = breakdown[stock]
                writer.writerow([
                    stock,
                    f"{data['quantity']:.2f}",
                    f"${data['price_per_share']:.2f}",
                    f"${data['total_value']:.2f}"
                ])
            
            # Write total
            writer.writerow([])
            writer.writerow(["Total Investment Value", f"${total_value:,.2f}"])
        
        print(f"✓ Portfolio saved to '{filename}'")
        return True
    except IOError as e:
        print(f"❌ Error saving file: {e}")
        return False


def save_portfolio_prompt(total_value, breakdown):
    """Prompt user to save portfolio and handle file format selection."""
    if not breakdown:
        print("\n⚠ Portfolio is empty. Nothing to save.")
        return
    
    print("\n" + "="*50)
    save_choice = input("Save portfolio to file? (Y/N): ").upper().strip()
    
    if save_choice != 'Y':
        return
    
    print("\nSelect file format:")
    print("1. Text file (.txt)")
    print("2. CSV file (.csv)")
    print("3. Both formats")
    
    format_choice = input("\nEnter choice (1-3): ").strip()
    
    if format_choice in ['1', '3']:
        save_to_txt({}, total_value, breakdown)
    
    if format_choice in ['2', '3']:
        save_to_csv({}, total_value, breakdown)


def main():
    """Main function to run the stock portfolio tracker."""
    try:
        # Build portfolio
        portfolio = build_portfolio()
        
        if not portfolio:
            print("\n⚠ No stocks added. Exiting.")
            return
        
        # Calculate values
        total_value, breakdown = calculate_portfolio_value(portfolio)
        
        # Display summary
        display_portfolio_summary(portfolio, total_value, breakdown)
        
        # Ask to save
        save_portfolio_prompt(total_value, breakdown)
        
        print("\n✓ Thank you for using Stock Portfolio Tracker!")
        
    except KeyboardInterrupt:
        print("\n\n⚠ Program interrupted by user.")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()