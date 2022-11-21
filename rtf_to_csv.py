from os import listdir, makedirs, path
import pandas as pd
# pd.set_option('display.max_columns', None)



class RtfToCsv:
    


    def __init__(self, file_name = None, test_df = None) -> None:
        if file_name:
            self.file_name = file_name
        if isinstance(test_df, pd.DataFrame):
            self.df = test_df
            self.col_names = {i:i for i in self.df.columns}
            # self.initial_cleaning()

        


    def load_data(self):
        self.df = pd.read_csv(self.file_name, sep="|", na_values=[' ', '-', '- -    ', '- - ', '- - -', '_ _ _', 'N/A'], skipinitialspace=True)

    def update_and_remove(self,columns: list, strings: list):
        """
        update eventual column names with string and remove said string from column values

        columns and strings must be lists of the same length
        """
        for col,s in zip(columns,strings):
            if not s:
                continue
            self.df[col] = self.df[col].str.replace(s, "").str.rstrip().str.lstrip()
            self.col_names[col] += '_'+s

    def initial_cleaning(self):
        # remove white space before and after col name
        self.df.columns = [col.lstrip().rstrip().replace(' ', '_') for col in self.df.columns]
        self.df = self.df.drop(columns=[i for i in self.df.columns if 'Unnamed:' in i])
        self.col_names = {i:i for i in self.df.columns}
        # remove the rows that are generated as just "-" charecter
        if not any(char.isdigit() for char in self.df['UID'][0]) and len(set(self.df['UID'][0])) == 1:
            self.df = self.df[self.df.index % 2 != 0]
        elif not any(char.isdigit() for char in self.df['UID'][1]) and len(set(self.df['UID'][0])) == 1:
            self.df = self.df[self.df.index % 2 == 0]
        else:
            raise Exception("RTF file has unexpected format, please check example file for refrence.") 

    def extract_monetary_symbol(self, cols: list) -> None:
        cols = [i for i in cols if i in self.df.columns]
        self.monetary_symbol = None
        
        for col in cols:
            if self.monetary_symbol:
                break
            
            text_split = self.df[col].str.split(' ').values.tolist()
            for row in text_split:
                if not row[0]:
                    continue
                if not row[0][0].isalnum() and row[0][1].isnumeric():
                    self.monetary_symbol = row[0][0]
                    break
        # update final column names and remove symbol from column string
        self.update_and_remove(cols,[self.monetary_symbol]*len(cols))

    def get_units(self,cols: list) -> None:
        """"""
        cols = [i for i in cols if i in self.df.columns]
        units = []
        
        for col in cols:
            # print(col)
            found = False
            text_split = self.df[col].str.split(' ').values.tolist()
            for row in text_split:
                if len(row) > 1:
                    if row[1].replace('/', '').isalpha():
                        units.append(row[1])
                        found = True
                        break
            if not found:
                units.append(None)
        # update final column names and remove unit from column string
        self.update_and_remove(cols,units)

    def process_transfer_value(self, cur_symb = None):
        """
        """
        new_cols = ['Transfer_Value_Lower','Transfer_Value_Upper']
        d = {'K':'000', 'M': '000000', 'B':'000000000'}
        d[cur_symb] = ""
        temp = pd.DataFrame(self.df['Transfer_Value'].str.split('-').values.tolist(), columns=new_cols)

        for i in temp.columns:
            temp[i] = temp[i].str.lstrip().str.rstrip()
            for key, val in d.items():
                temp[i] = temp[i].str.replace(key,val,regex=True)
                temp[i] = temp[i].str.replace(pat=r"(\d*)[.,](\d)0(0*)", repl=r"\1\2\3") # TODO: dynamically determine digits after deliminator
        temp['Transfer_Value_Upper'] = temp['Transfer_Value_Upper'].fillna(temp['Transfer_Value_Lower'])

        # add new cols to col name dict
        self.df = pd.concat([self.df.drop(columns='Transfer_Value'), temp],axis=1)
        for i in new_cols:
            self.col_names[i] = i + "_" + cur_symb
        del self.col_names['Transfer_Value']

        
        
            
        



if __name__ == '__main__':
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter(action='ignore', category=FutureWarning)
        # Warning-causing lines of code here
        files = [f for f in listdir() if f[-4:] == '.rtf']
        if not path.exists("Converted_CSV"):
                makedirs("Converted_CSV")
        for f in files:
            rtf_data = RtfToCsv(file_name=f)
            rtf_data.load_data()
            rtf_data.initial_cleaning()
            rtf_data.extract_monetary_symbol(['Salary'])
            rtf_data.get_units(['Salary', 'Height', 'Weight'])
            rtf_data.process_transfer_value(cur_symb=rtf_data.monetary_symbol)
            rtf_data.df = rtf_data.df.rename(columns=rtf_data.col_names)
            rtf_data.df.to_csv(f"Converted_CSV/{f[:-4]}.csv", index=False)