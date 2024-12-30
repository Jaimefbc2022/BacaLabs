def format_number(numero):
    
    if numero == int(numero):
        return f"{numero:,}".replace(",", "X").replace(".", ",").replace("X", ".")
    else:
        return f"{numero:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def format_number_and_currency(numero,country):
    
    euro_symbol = "€"
    pound_symbol = "£"
    
    if numero == int(numero):
        if country == "UK": 
            return f"{pound_symbol}" + f"{numero:,}".replace(",", "X").replace(".", ",").replace("X", ".")
        else:
            return f"{numero:,}".replace(",", "X").replace(".", ",").replace("X", ".") + f"{euro_symbol}"
    else:
        if country == "UK":
            return f"{pound_symbol}" + f"{numero:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        else:
            return f"{numero:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") + f"{euro_symbol}"


