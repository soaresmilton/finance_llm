import ofxparse
import pandas as pd
import os
from datetime import datetime

## Construindo tabela de transações
df_transactions = pd.DataFrame()

for extrato in os.listdir("Extratos"):
    with open(f'Extratos/{extrato}', encoding='ISO-8859-1') as ofx_file:
        ofx = ofxparse.OfxParser.parse(ofx_file)
    
    transactions_data = []
    for account in ofx.accounts:
        for transaction in account.statement.transactions:
            transactions_data.append({
                "Data": transaction.date,
                "Valor": transaction.amount,
                "Descrição": transaction.memo,
                "ID": transaction.id,
                "type": transaction.type
            })
    
    df_temp = pd.DataFrame(transactions_data)
    df_temp["Valor"] = df_temp["Valor"].astype(float)
    df_temp["Data"] = df_temp["Data"].apply(lambda x: x.date())
    df_transactions = pd.concat([df_transactions, df_temp])
    
df_transactions = df_transactions.set_index("ID")