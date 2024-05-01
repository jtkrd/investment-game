from abc import ABC, abstractmethod

class Strategy(ABC):
    @abstractmethod
    def select_stocks(self, market_data):
        """
        Selects stocks based on strategy-specific criteria.
        :param market_data: A dictionary containing stock market data.
        :return: A list of stock symbols to buy/sell.
        """
        pass

class AggressiveStrategy(Strategy):
    def select_stocks(self, market_data):
        # Example strategy: Buy stocks that dropped the most in the past day
        sorted_stocks = sorted(market_data.items(), key = lambda x: x[1]['change'])
        return [stock for stock, data in sorted_stocks[:10]]  # buy 10 stocks that dropped the most

class ConservativeStrategy(Strategy):
    def select_stocks(self, market_data):
        # Example strategy: Buy stocks that are most stable (smallest changes)
        sorted_stocks = sorted(market_data.items(), key = lambda x: abs(x[1]['change']))
        return [stock for stock, data in sorted_stocks[:10]]  # buy 10 most stable stocks
    
class RandomStrategy(Strategy):
    def select_stocks(self, market_data):
        # Get all stock symbols from the market data
        stock_list = list(market_data.keys())
        # Shuffle the list of stocks to randomize the order
        random.shuffle(stock_list)
        # Return the first 10 stocks from the shuffled list
        return stock_list[:10]

class CustomStrategy(Strategy):
    def __init__(self, stocks):
        self.stocks = stocks  # Stocks should be a list of stock symbols

    def select_stocks(self, market_data):
        # Return the stocks that are both in the provided list and the market data
        return [stock for stock in self.stocks if stock in market_data]

class Investor:
    
    def __init__(self, name, strategy, balance=100000):
        self.name = name
        self.strategy = strategy
        self.balance = balance
        self.portfolio = {}

    def invest(self, market_data):
        stocks_to_buy = self.strategy.select_stocks(market_data)
        num_stocks = len(stocks_to_buy)
        if num_stocks == 0:
            print("No valid stocks to invest in.")
            return
        
        amount_per_stock = self.balance / num_stocks
        for stock in stocks_to_buy:
            shares_to_buy = int(amount_per_stock / market_data[stock]['price'])
            self.portfolio[stock] = shares_to_buy
            self.balance -= shares_to_buy * market_data[stock]['price']
                
    def display_portfolio(self):
        print(f"{self.name}'s Portfolio:\n{'-'*20}")
        for stock, quantity in self.portfolio.items():
            print(f"{stock}: {quantity} shares")
        print(f"\nRemaining Balance: ${self.balance:.2f}\n")
        
def create_custom_strategy(market_data):
    print("Create your strategy based on:")
    print("Enter minimum market cap (in millions):")
    market_cap = float(input())  # Convert input directly to float
    print("Enter maximum volatility percentage:")
    volatility = float(input())  # Convert input directly to float

    # Function to evaluate if a stock meets the custom criteria
    def custom_criteria(stock_data, min_market_cap, max_market_cap, min_volatility, max_volatility):
        meets_cap = min_market_cap <= stock_data.get('market_cap', float('inf')) <= max_market_cap
        meets_volatility = min_volatility <= stock_data.get('volatility', float('inf')) <= max_volatility
        return meets_cap and meets_volatility

    # Filter the stocks based on the provided criteria
    selected_stocks = [stock for stock, data in market_data.items() if custom_criteria(data)]
    
    # Debugging output to understand what's being selected
    print("Selected stocks based on criteria:", selected_stocks)
    
    # Check if any stocks were selected
    if not selected_stocks:
        print("No valid stocks to invest in based on the criteria provided.")
        return None  # Return None or raise an error as per your game design needs

    return CustomStrategy(selected_stocks[:10])  # Limit to 10 stocks

def player_options_menu(market_data):
    print("Choose your investment approach:")
    print("1. Freely choose and input 10 stock symbols")
    print("2. Choose a predefined strategy")
    print("3. Create your own strategy based on criteria")

    choice = input("Enter your choice (1, 2, or 3): ")
    
    if choice == '1':
        player_stocks = get_player_stocks(market_data)
        player_strategy = CustomStrategy(player_stocks)
    elif choice == '2':
        player_strategy = choose_predefined_strategy()
    elif choice == '3':
        player_strategy = create_custom_strategy(market_data)
    else:
        print("Invalid choice, please select 1, 2, or 3.")
        return player_options_menu(market_data)
    
    return player_strategy

def choose_predefined_strategy():
    print("Available Strategies:")
    print("1. Aggressive Strategy")
    print("2. Conservative Strategy")
    print("3. Random Strategy")
    strategy_choice = input("Choose a strategy (1-3): ")
    
    if strategy_choice == '1':
        return AggressiveStrategy()
    elif strategy_choice == '2':
        return ConservativeStrategy()
    elif strategy_choice == '3':
        return RandomStrategy()
    else:
        print("Invalid choice. Please select a valid strategy.")
        return choose_predefined_strategy()

def get_float_input(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input, please enter a numeric value.")
            
def safe_float_input(prompt):
    while True:
        input_str = input(prompt)
        try:
            values = list(map(float, input_str.split(',')))
            if len(values) == 2:
                return values
            else:
                print("Please enter exactly two values separated by a comma.")
        except ValueError:
            print("Invalid input; please ensure you enter numeric values.")
            
def create_custom_strategy(market_data):
    min_market_cap, max_market_cap = safe_float_input("Enter minimum and maximum market cap (in millions), separated by a comma (e.g., 0.1, 500):")
    min_volatility, max_volatility = safe_float_input("Enter minimum and maximum volatility percentage, separated by a comma (e.g., 10, 50):")

    selected_stocks = [
        stock for stock, data in market_data.items()
        if min_market_cap <= data.get('market_cap', float('inf')) <= max_market_cap and
        min_volatility <= data.get('volatility', float('inf')) <= max_volatility
    ]

    print("Selected stocks based on criteria:", selected_stocks)

    if not selected_stocks:
        print("No valid stocks to invest in based on the criteria provided.")
        return None

    return CustomStrategy(selected_stocks[:10])  # Limit to 10 stocks

def get_player_stocks(market_data):
    print("Enter up to 10 stock symbols, separated by commas (e.g., AAPL, GOOGL, MSFT):")
    input_string = input("Enter stock symbols: ")
    stock_list = [stock.strip().upper() for stock in input_string.split(',')]
    player_stocks = []
    for stock in stock_list:
        if stock in market_data:
            if stock not in player_stocks and len(player_stocks) < 10:
                player_stocks.append(stock)
            elif len(player_stocks) >= 10:
                print("Maximum of 10 stocks reached. Additional stocks are ignored.")
                break
        else:
            print(f"Invalid stock symbol {stock}. Please try again.")
    return player_stocks

def calculate_portfolio_return(portfolio, initial_market_data, final_market_data):
    initial_value = sum(initial_market_data[stock]['price'] * quantity for stock, quantity in portfolio.items())
    final_value = sum(final_market_data[stock]['price'] * quantity for stock, quantity in portfolio.items() if stock in final_market_data)

    if initial_value == 0:
        print("Initial portfolio value is zero; no investments were made.")
        return 0  # Return 0 to indicate no growth or loss
    return ((final_value - initial_value) / initial_value) * 100

def compare_portfolios(investors, initial_market_data, final_market_data):
    results = {}
    for investor in investors:
        return_pct = calculate_portfolio_return(investor.portfolio, initial_market_data, final_market_data)
        results[investor.name] = return_pct
        print(f"{investor.name}'s portfolio return: {return_pct:.2f}%")
    best_performer = max(results, key=results.get)
    print(f"The best performing portfolio is {best_performer} with a return of {results[best_performer]:.2f}%.")

market_data = {
    'AAPL': {'price': 150, 'change': -0.5, 'market_cap': 2200, 'volatility': 25},
    'GOOGL': {'price': 2720, 'change': -1.0, 'market_cap': 1800, 'volatility': 30},
    'MSFT': {'price': 280, 'change': 0.2, 'market_cap': 2000, 'volatility': 22},
    'AMZN': {'price': 3100, 'change': -2.0, 'market_cap': 1600, 'volatility': 35},
    'FB': {'price': 275, 'change': 0.5, 'market_cap': 900, 'volatility': 40},
    'NFLX': {'price': 480, 'change': -0.3, 'market_cap': 300, 'volatility': 50},
    'TSLA': {'price': 900, 'change': 1.5, 'market_cap': 800, 'volatility': 60},
    'BABA': {'price': 88, 'change': -1.2, 'market_cap': 500, 'volatility': 45},
    'V': {'price': 210, 'change': 0.4, 'market_cap': 500, 'volatility': 18},
    'MA': {'price': 330, 'change': 0.1, 'market_cap': 400, 'volatility': 20},
    'INTC': {'price': 48, 'change': -0.8, 'market_cap': 220, 'volatility': 30},
    'AMD': {'price': 106, 'change': 1.0, 'market_cap': 130, 'volatility': 55},
    'PYPL': {'price': 104, 'change': -0.2, 'market_cap': 250, 'volatility': 28},
    'CSCO': {'price': 45, 'change': 0.6, 'market_cap': 200, 'volatility': 23},
    'IBM': {'price': 135, 'change': -0.4, 'market_cap': 120, 'volatility': 19},
    'NVDA': {'price': 300, 'change': 2.0, 'market_cap': 500, 'volatility': 50},
    'ORCL': {'price': 88, 'change': 0.3, 'market_cap': 250, 'volatility': 20},
    'ACN': {'price': 310, 'change': -0.7, 'market_cap': 180, 'volatility': 17},
    'KO': {'price': 60, 'change': 0.1, 'market_cap': 230, 'volatility': 12},
    'PEP': {'price': 160, 'change': -0.1, 'market_cap': 200, 'volatility': 15}
}

market_data_next_year = {
    'AAPL': {'price': 165},  # Increased
    'GOOGL': {'price': 2900},  # Increased
    'MSFT': {'price': 300},  # Increased
    'AMZN': {'price': 2800},  # Decreased
    'FB': {'price': 295},  # Increased
    'NFLX': {'price': 500},  # Increased
    'TSLA': {'price': 950},  # Increased
    'BABA': {'price': 95},  # Increased
    'V': {'price': 225},  # Increased
    'MA': {'price': 350},  # Increased
    'INTC': {'price': 52},  # Increased
    'AMD': {'price': 116},  # Increased
    'PYPL': {'price': 110},  # Increased
    'CSCO': {'price': 50},  # Increased
    'IBM': {'price': 145},  # Increased
    'NVDA': {'price': 330},  # Increased
    'ORCL': {'price': 95},  # Increased
    'ACN': {'price': 330},  # Increased
    'KO': {'price': 65},  # Increased
    'PEP': {'price': 170}   # Increased
}

# Get the player's chosen strategy
player_strategy = player_options_menu(market_data)

# Create a player with the chosen strategy
player = Investor("Player", player_strategy)

# Creating investors with different strategies
investor1 = Investor("Alice", AggressiveStrategy())
investor2 = Investor("Bob", ConservativeStrategy())

# Simulate the investment decisions
investor1.invest(market_data)
investor2.invest(market_data)
player.invest(market_data)

# Display portfolios
player.display_portfolio()
investor1.display_portfolio()
investor2.display_portfolio()

# Assume time passes and now we evaluate the portfolios one year later
compare_portfolios([investor1, investor2, player], market_data, market_data_next_year)