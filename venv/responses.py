# responses.py

from random import choice

# Data structure to store bet information
bet_data = []
bets_closed = False
table_title = None  # Variable to store the table title


def process_bet(username: str, teamname: str, money: int) -> str:
    if bets_closed:
        return '''Bets are currently closed. You cannot place a new bet at the moment.'''

    # Store the bet information in the data structure
    bet_data.append({'username': username, 'team_name': teamname, 'money': money})
    if teamname.upper() == 'RCB':
        return f"Bet placed on {teamname} with {money} money by {username}.   E SALA CUP NAMDE!!"
    else:
        return f"Bet placed on {teamname} with {money} money by {username}."


def process_bet_user(author_username: str, target_username: str, teamname: str, money: int) -> str:
    if bets_closed:
        return "Bets are currently closed. You cannot place a new bet at the moment."

    # Store the bet information for the specified user
    bet_data.append({'username': target_username, 'team_name': teamname, 'money': money})

    # Add a special message for RCB bets
    if teamname.lower() == 'rcb':
        return f"Bet placed on behalf of {target_username} on {teamname} with {money} money by {author_username}. E SALA CUP NAMDE!"
    else:
        return f"Bet placed on behalf of {target_username} on {teamname} with {money} money by {author_username}."
def close_bets() -> str:
    global bets_closed
    bets_closed = True
    return "Bets are now closed. No new bets will be accepted until bets are opened again with $betopen."

def open_bets() -> str:
    global bets_closed
    bets_closed = False
    return "Bets are now open. You can place new bets."

def set_table_title(title: str) -> str:
    global table_title
    table_title = title
    return f"Table title set to: {title}. The title cannot be changed until the table is cleared using $clear."

def get_bet_table() -> str:
    # Generate a larger table of bet information with manually adjusted centering
    table = "```plaintext\n"
    if table_title:
        table += f"{table_title:^80}\n"
    table += "---------------|-----------|-----------\n"
    table += "    Username   | Team Name |  Amount   \n"
    table += "---------------|-----------|-----------\n"

    for bet in bet_data:
        table += f"{bet['username']:^14} |{bet['team_name']:^11}|{bet['money']:^12}\n"

    table += "```"
    return table

def clear_bet_table() -> str:
    # Clear the bet table
    bet_data.clear()
    return "Bet table has been cleared."

def get_help_response() -> str:
    # Help message with code formatting
    help_message = (
        "```\n"
        "$hello      : Greet the user.\n"
        "$roll dice  : Roll a six-sided die.\n"
        "$bet        : { $bet team_name amount } Place a bet on a team with the specified amount of money.\n"
        "$betuser    : { $betuser username team_name amount } Place a bet on behalf of someone else.\n"
        "$betclosed  : Close bets and stop accepting new bets until $betopen is called.\n"
        "$betopen    : Open bets and allow users to place new bets.\n"
        "$bettable   : Display a table of current bets.\n"
        "$tabletitle : Set the title for the bet table (can't be changed until cleared)\n"
        "$clear      : Clear the bet table and start over.\n"
        "$help       : Display this help message.\n"

        "```"
    )
    return help_message

def get_response(user_input: str, author_username: str) -> str:
    lowered = user_input.lower()

    if lowered.startswith('$'):
        if lowered.startswith('$hello'):
            return f'Hello there, {author_username}!'
        elif lowered.startswith('$roll dice'):
            return f'{author_username}, you called: {choice(range(1, 7))}'
        elif lowered.startswith('$bet '):
            # Split the input into parts
            parts = lowered.split()

            if len(parts) == 3:
                _, teamname, money_str = parts

                # Check if teamname is valid (you may replace the list with your teams)
                valid_teams = ['CSK', 'DC', 'GT', 'KKR', 'RCB', 'LSG', 'PK', 'RR', 'SRH']
                if teamname.upper() not in valid_teams:
                    return f"Invalid team name. {author_username}, please choose from: " + ", ".join(valid_teams)

                # Check if money is a valid integer
                try:
                    money = int(money_str)
                except ValueError:
                    return f"Invalid money value. {author_username}, please enter a valid integer."

                # Process the bet
                return process_bet(author_username, teamname, money)
            else:
                return f"Invalid command format. {author_username}, usage: $bet teamname money"
        elif lowered.startswith('$betuser '):
            # Split the input into parts
            parts = lowered.split()

            if len(parts) == 4:
                _, target_username, teamname, money_str = parts

                # Check if teamname is valid (you may replace the list with your teams)
                valid_teams = ['CSK', 'DC', 'GT', 'KKR', 'RCB', 'LSG', 'PK', 'RR', 'SEH']
                if teamname.upper() not in valid_teams:
                    return f"Invalid team name. {author_username}, please choose from: " + ", ".join(valid_teams)

                # Check if money is a valid integer
                try:
                    money = int(money_str)
                except ValueError:
                    return f"Invalid money value. {author_username}, please enter a valid integer."

                # Process the bet on behalf of the specified user
                return process_bet_user(author_username, target_username, teamname, money)
            else:
                return f"Invalid command format. {author_username}, usage: $betuser username teamname money"
        elif lowered.startswith('$betclosed'):
            return close_bets()
        elif lowered.startswith('$betopen'):
            return open_bets()
        elif lowered.startswith('$bettable'):
            return get_bet_table()
        elif lowered.startswith('$tabletitle '):
            # Extract the title from the command
            title = user_input[len('$tabletitle '):].strip()
            # Check if the title is provided
            if not title:
                return "Please provide a title for the table."
            # Set the table title
            return set_table_title(title)
        elif lowered.startswith('$clear'):
            return clear_bet_table(),open_bets()
        elif lowered.startswith('$help'):
            return get_help_response()
        else:
            return choice(['I do not understand', 'invalid command'])
    else:
        return ''  # Bot doesn't respond to messages that don't start with "$"