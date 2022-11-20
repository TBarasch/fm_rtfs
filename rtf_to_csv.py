
from re import findall, match
from os import listdir
from RtfToCsv_class import RtfToCsv

files = [f for f in listdir() if f[-4:] == '.rtf']
for f in files:
    rtf_data = RtfToCsv(file_name=f)
    rtf_data.load_data()
    rtf_data.initial_cleaning()
    rtf_data.extract_monetary_symbol(['Salary'])
    rtf_data.get_units(['Salary', 'Height', 'Weight'])
    rtf_data.process_transfer_value(cur_symb=rtf_data.monetary_symbol)
    rtf_data.df = rtf_data.df.rename(columns=rtf_data.col_names)

    rtf_data.df.to_csv(f[:-4]+ '.csv', index=False)

# test.df.head()

