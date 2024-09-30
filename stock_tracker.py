import tkinter as tk
from tkinter import messagebox
import yfinance as yf

class StockPortfolioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Portfolio Tracker")
        
        # Center the window on the screen
        window_width = 600
        window_height = 400
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (window_width / 2))
        y_coordinate = int((screen_height / 2) - (window_height / 2))
        root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
        
        self.root.configure(bg="#2c3e50")
        self.portfolio = {}  # Dictionary to store stock data
        self.setup_ui()

    def setup_ui(self):
        # Title Label
        self.title_label = tk.Label(
            self.root, text="Stock Portfolio Tracker", font=("Helvetica", 20, "bold"), bg="#34495e", fg="white"
        )
        self.title_label.pack(pady=10)

        # Stock input frame
        self.stock_frame = tk.Frame(self.root, bg="#2c3e50")
        self.stock_frame.pack(pady=20)

        # Input box to add stock symbol
        self.stock_symbol_label = tk.Label(self.stock_frame, text="Stock Symbol:", font=("Helvetica", 12), bg="#2c3e50", fg="white")
        self.stock_symbol_label.grid(row=0, column=0, padx=5)

        self.stock_symbol_entry = tk.Entry(self.stock_frame, font=("Helvetica", 12), width=10)
        self.stock_symbol_entry.grid(row=0, column=1, padx=5)

        # Input box to add stock quantity
        self.stock_quantity_label = tk.Label(self.stock_frame, text="Quantity:", font=("Helvetica", 12), bg="#2c3e50", fg="white")
        self.stock_quantity_label.grid(row=0, column=2, padx=5)


        self.stock_quantity_entry = tk.Entry(self.stock_frame, font=("Helvetica", 12), width=10)
        self.stock_quantity_entry.grid(row=0, column=3, padx=5)

        # Add button
        self.add_button = tk.Button(self.stock_frame, text="Add Stock", font=("Helvetica", 12), bg="#1abc9c", fg="white", command=self.add_stock)
        self.add_button.grid(row=0, column=4, padx=5)

        # Portfolio display frame
        self.portfolio_frame = tk.Frame(self.root, bg="#ecf0f1")
        self.portfolio_frame.pack(pady=20)

        self.update_button = tk.Button(self.root, text="Update Prices", font=("Helvetica", 12), bg="#e67e22", fg="white", command=self.update_prices)
        self.update_button.pack(pady=10)

        self.quit_button = tk.Button(self.root, text="Quit", font=("Helvetica", 12), bg="#e74c3c", fg="white", command=self.root.quit)
        self.quit_button.pack(pady=10)

    def add_stock(self):
        symbol = self.stock_symbol_entry.get().upper()
        quantity = self.stock_quantity_entry.get()

        if not symbol or not quantity:
            messagebox.showerror("Error", "Please provide both stock symbol and quantity.")
            return

        try:
            quantity = int(quantity)
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a number.")
            return

        # Fetch stock data using yfinance
        try:
            stock_data = yf.Ticker(symbol)
            stock_price = stock_data.history(period="1d")['Close'][0]
        except:
            messagebox.showerror("Error", "Failed to retrieve stock data.")
            return

        # Add to portfolio
        self.portfolio[symbol] = {'quantity': quantity, 'price': stock_price}

        # Clear the input fields
        self.stock_symbol_entry.delete(0, tk.END)
        self.stock_quantity_entry.delete(0, tk.END)

        self.display_portfolio()

    def display_portfolio(self):
        # Clear the frame before re-displaying the updated portfolio
        for widget in self.portfolio_frame.winfo_children():
            widget.destroy()

        row = 0
        for symbol, data in self.portfolio.items():
            quantity = data['quantity']
            price = data['price']
            value = quantity * price

            stock_label = tk.Label(self.portfolio_frame, text=f"{symbol}: {quantity} shares @ ${price:.2f} - Value: ${value:.2f}", font=("Helvetica", 12), bg="#ecf0f1", fg="#2c3e50")
            stock_label.grid(row=row, column=0, pady=5)

            # Add remove button for each stock
            remove_button = tk.Button(self.portfolio_frame, text="Remove", font=("Helvetica", 10), bg="#e74c3c", fg="white", command=lambda sym=symbol: self.remove_stock(sym))
            remove_button.grid(row=row, column=1, padx=5)
            row += 1

    def update_prices(self):
        for symbol in self.portfolio.keys():
            try:
                stock_data = yf.Ticker(symbol)
                new_price = stock_data.history(period="1d")['Close'][0]
                self.portfolio[symbol]['price'] = new_price
            except:
                messagebox.showerror("Error", f"Failed to update price for {symbol}.")

        self.display_portfolio()

    def remove_stock(self, symbol):
        if symbol in self.portfolio:
            del self.portfolio[symbol]
            self.display_portfolio()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = StockPortfolioApp(root)
    root.mainloop()
