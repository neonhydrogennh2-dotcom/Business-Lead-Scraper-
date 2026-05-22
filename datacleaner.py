import csv 
import pandas as pd 
import re 
import math

def clean_phone_num(phone):
    if not phone or str(phone).strip().upper() == "N/A" or (isinstance(phone, float) and math.isnan(phone)):
        return "N/A"
    
    clean_digits = re.sub(r'\D', '', str(phone))
    
    if clean_digits.startswith("03"): 
        clean_digits = "92" + clean_digits[1:]
    
    elif clean_digits.startswith("3") and len(clean_digits) == 10:
        clean_digits = "92" + clean_digits
        
    return clean_digits


file_path = "leads_businesslist_pk.csv"

column_names = ["Category", "Name", "Address", "Phone"] 

df = pd.read_csv(file_path, names=column_names, header=None).copy()

df = df.dropna(subset=["Name", "Address", "Phone"])

df.drop_duplicates(inplace=True)

df.loc[:, "Phone"] = df["Phone"].apply(clean_phone_num)

# Remove the specific list of layout words
noise_words = ['Established', 'E-mail', 'Map', 'Website', 'Photos', 'Address:']

for word in noise_words:
    df.loc[:, 'Address'] = df['Address'].str.replace(word, '', regex=False)
    df.loc[:, 'Phone'] = df['Phone'].str.replace(word, '', regex=False)

# Strip leading/trailing whitespace left behind
df.loc[:, 'Address'] = df['Address'].str.strip()
df.loc[:, 'Phone'] = df['Phone'].str.strip()

# Drop duplicates ONLY if the phone number is NOT "N/A"
df_valid_phones = df[df["Phone"] != "N/A"].drop_duplicates(subset=["Phone"])
df_nas = df[df["Phone"] == "N/A"]

df_final = pd.concat([df_valid_phones, df_nas], ignore_index=True)

category_counts = df_final['Category'].value_counts()

print("--- Leads Breakdown by Category ---")
print(category_counts)

advertising_leads = df_final[df_final['Category'] == 'advertising']
print("\n--- Sample Advertising Leads ---")
print(advertising_leads.head())

#df.to_csv('cleaned_leads.csv', index=False, encoding='utf-8-sig')