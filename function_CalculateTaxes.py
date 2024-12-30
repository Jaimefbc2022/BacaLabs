
import pandas as pd


def calculate_Taxes(salary, country):
    
    # Read Excel file
    
    #try:
       # ruta = "/Users/jaimefbc/Documents/GitHub/BacaLabs/mapping.xlsx"
    #except:
        # Cuando la app no se abre localmente
    
    ruta = "mapping.xlsx"

    
    archivo_excel = ruta  
    datos_excel = pd.read_excel(archivo_excel)

    # Create dataset
    df = pd.DataFrame(datos_excel)

    print(u'\u2501' * 100)
    print("Check 1. This is the dataframe data: " ,"\n \n", df)
    print(u'\u2501' * 100)

    # Inputs

    salario = salary
    country = country

    quantity = salario
    tax_sum = 0
  

    # Calculate Income Taxes

    ## Number of ranges in the country
        
    country_ranges = df.loc[(df['Country'] == country) & (df['TypeCode'] == (1))].shape[0]
        
    print(f"Check 2. Number of tax ranges in {country} : " ,country_ranges)
    print(u'\u2501' * 100)

    ## Number of ranges in the country

    for i in range(0,country_ranges):
            
        # First Range is 1 but the loop starts in 0 so our selected range will always be i+1
        selected_range = df.loc[(df['Country'] == country) & (df['TypeCode'] == (1)) & (df['Range'] == (i+1)), 'To'].values[0]

        # To know which is the amount of money that will be used as base for each range, we need to know which is the maximum taxable salary for the last range
        if i == 0:
            range_minus1 = 0
        
        else:
            range_minus1 = df.loc[(df['Country'] == country) & (df['TypeCode'] == (1)) &(df['Range'] == (i)), 'To'].values[0]

        
        if quantity < (selected_range-range_minus1) :
            base = quantity
        else:
            base = selected_range-range_minus1

        percentage_range =  df.loc[(df['Country'] == country) & (df['TypeCode'] == (1)) &(df['Range'] == (i+1)), 'Percentage'].values[0]
        tax = percentage_range * base
        tax_sum = tax + tax_sum
        quantity = quantity - base
        
        print(f"Selected Range is {i+1}: {selected_range} and corresponding percentage is {percentage_range}. Base: {base}, Fee: {tax}, Remaining: {quantity}")
        
        if quantity == 0:
            break
        
    quantity = salario
    NI_sum = 0
    

    # Calculate National Insurace Taxes

    ## Number of ranges in the country
        
    country_ranges = df.loc[(df['Country'] == country) & (df['TypeCode'] == (2))].shape[0]
        
    print(u'\u2501' * 100)
    print(f"Check 3. Number of NI ranges in {country} : " ,country_ranges)
    print(u'\u2501' * 100)

    ## Number of ranges in the country

    for i in range(0,country_ranges):
            
        # First Range is 1 but the loop starts in 0 so our selected range will always be i+1
        selected_range = df.loc[(df['Country'] == country) & (df['TypeCode'] == (2)) & (df['Range'] == (i+1)), 'To'].values[0]

        # To know which is the amount of money that will be used as base for each range, we need to know which is the maximum taxable salary for the last range
        if i == 0:
            range_minus1 = 0
        
        else:
            range_minus1 = df.loc[(df['Country'] == country) & (df['TypeCode'] == (2)) &(df['Range'] == (i)), 'To'].values[0]

        
        if quantity < (selected_range-range_minus1) :
            base = quantity
        else:
            base = selected_range-range_minus1

        percentage_range =  df.loc[(df['Country'] == country) & (df['TypeCode'] == (2)) &(df['Range'] == (i+1)), 'Percentage'].values[0]
        NI = percentage_range * base
        NI_sum = NI + NI_sum
        quantity = quantity - base
        
        print(f"Selected Range is {i+1}: {selected_range} and corresponding percentage is {percentage_range}. Base: {base}, Fee: {NI}, Remaining: {quantity}")
        
        if quantity == 0:
            break
    
    total_taxes = tax_sum + NI_sum
    return  total_taxes, tax_sum , NI_sum
        
        

        




#print(calculate_Taxes(100000, "UK")[0])




