import requests
from bs4 import BeautifulSoup

# Función para obtener la tasa de cambio desde el conversor de Google
def get_exchange_rate(from_currency, to_currency):
    url = f'https://www.google.com/search?q={from_currency}+to+{to_currency}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    
    print(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Buscar el valor de la tasa de cambio en el HTML
        result = soup.find('span', {'class': 'DFlfde', 'data-precision': '2'})
    
        print("result es: ", result)
        if result:
            return float(result.text.replace(',', '.'))
        else:
            print("No se encontró la tasa de cambio.")
            return None
    else:
        print(f"Error al hacer la solicitud: {response.status_code}")
        return None

# Ejemplo de uso: Convertir USD a EUR
from_currency = 'GBP'
to_currency = 'EUR'
rate = get_exchange_rate(from_currency, to_currency)

if rate:
    print(f"La tasa de cambio de {from_currency} a {to_currency} es: {rate}")
