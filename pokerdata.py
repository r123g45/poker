import re
from collections import defaultdict

def analyze_poker_data(file_path):
    # Initialize dictionaries to track player stats
    total_buyins = defaultdict(float)
    total_finals = defaultdict(float)
    total_sessions = defaultdict(int)
    
    try:
        with open(file_path, 'r') as file:
            data = file.read()
            
        # Split the data into sessions using a consistent delimiter
        sessions = [session.strip() for session in data.split('—' * 5) if session.strip()]
        
        rahul_session_count = 0  # Counter for Rahul's sessions
        
        for session in sessions:
            # Debug: Print the session being processed
            print(f"Processing session: {session[:50]}...")  # Print first 50 characters
            
            # Find all player entries in this session
            player_entries = re.findall(r'(\w+)\s*-\s*(\d+)\s*-\s*(\d+|clear-\s*\d+|clear)', session)
            
            if not player_entries:
                print(f"Skipping empty or malformed session: {session}")
                continue
            
            for entry in player_entries:
                player, buyin, final = entry
                player = player.strip()
                
                if player == "Rahul":
                    rahul_session_count += 1  # Increment Rahul's session count
                    print(f"Found Rahul in session: {session[:50]}...")  # Debug log
                
                try:
                    buyin = float(buyin.strip())
                    
                    # Handle special "clear" cases
                    if 'clear' in final:
                        # If format is like "clear- 0", extract the number
                        match = re.search(r'clear-\s*(\d+)', final)
                        if match:
                            final = float(match.group(1))
                        else:
                            final = 0.0
                    else:
                        final = float(final.strip())
                    
                    # Update player stats
                    total_buyins[player] += buyin
                    total_finals[player] += final
                    total_sessions[player] += 1
                    
                except ValueError:
                    print(f"Skipping invalid entry for player {player}: {entry}")
        
        print(f"Total sessions for Rahul: {rahul_session_count}")  # Debug log
        
        # Calculate P&L for each player
        results = []
        for player in sorted(total_buyins.keys()):
            pnl = total_finals[player] - total_buyins[player]
            results.append({
                'Player': player,
                'Sessions': total_sessions[player],
                'Total Buy-ins': total_buyins[player],
                'Total Final Stacks': total_finals[player],
                'P&L': pnl
            })
        
        # Sort by P&L (descending)
        results.sort(key=lambda x: x['P&L'], reverse=True)
        
        return results
    
    except Exception as e:
        print(f"Error processing file: {e}")
        return []

def print_results(results):
    print("\n{:<15} {:<10} {:<15} {:<20} {:<15}".format(
        "Player", "Sessions", "Total Buy-ins", "Total Final Stacks", "Profit/Loss"))
    print("-" * 80)
    
    for player in results:
        print("{:<15} {:<10} {:<15,.0f} {:<20,.0f} {:<15,.0f}".format(
            player['Player'],
            player['Sessions'],
            player['Total Buy-ins'],
            player['Total Final Stacks'],
            player['P&L']
        ))
    
    # Calculate and print overall stats
    total_buyin = sum(player['Total Buy-ins'] for player in results)
    total_final = sum(player['Total Final Stacks'] for player in results)
    total_pnl = total_final - total_buyin
    
    print("\n" + "-" * 80)
    print("Overall Stats:")
    print(f"Total Buy-ins across all players: {total_buyin:,.0f}")
    print(f"Total Final Stacks across all players: {total_final:,.0f}")
    print(f"Net P&L (should be close to zero): {total_pnl:,.0f}")

if __name__ == "__main__":
    file_path = "poker_data.txt"
    results = analyze_poker_data(file_path)
    
    if results:
        print_results(results)
    else:
        print("No results to display.")