import pandas as pd
import numpy as np
import re
import time
from datetime import datetime
from IPython.display import display

@pd.api.extensions.register_dataframe_accessor("pw")

class App:

    def __init__(self, df):
        self.df = df

    def list_splitter(self, columns, delete = False):
        df = self.df
        data = df.copy()
        new_col = []
        temp_col = []
        temp_dict = {}
        double_columns = df.columns[df.columns.duplicated()]
        double = []

        if not isinstance(delete, bool):
            print("\033[1;31m" + "delete is supposed to be a boolean")
            return

        try:
            if isinstance(columns, list):
                pass
            else:
                raise TypeError
        except TypeError:
            print("\033[1;31m" + 'A list was expected')
            return

        try:
            if 'True' in df.columns or 'False' in df.columns:
                raise NameError
        except NameError:
            print("\033[1;31m" + "True and False can't be column names")
            return

        [double.append(x) for x in columns if (x in double_columns.unique().values) and (x not in double)]
        try:
            if double:
                raise ValueError
        except ValueError:
            print('These columns cant be in the dataframe multiple times: {0}'.format(double))
            return

        for col in columns:
            if isinstance(col, str):
                dummy_columns = pd.get_dummies(df[col].apply(pd.Series).stack()).sum(level=0)
                for i in dummy_columns:
                    if i not in new_col:
                        new_col.append(i)

        for new in new_col:
            if new not in df.columns:
                data[new] = False
            else:
                print('The column {0} exist already'.format(new))
                answer = None
                while answer not in ("yes", "no", "j", "n", "ja", "y", "ye", "ne", "nee"):
                    answer = input("Do you want to put the data in a different column?: ")

                    if answer.lower() in ("yes", "ja", "j", "ye", "y"):
                        colname = ''
                        while colname in new_col or colname == '' or colname in df.columns or colname in temp_dict.values():
                            colname = input("What is the name of the new col?: ")
                        temp_dict[new] = colname
                        data[colname] = False

                    elif answer.lower() in ("no", "n", "ne", "nee"):
                        temp_col.append(new)

                    else:
                        print("Please enter yes or no.")

        new_col = [x for x in new_col if x not in temp_col]
        new_col = [x for x in new_col if x != True]
        new_col = [x for x in new_col if x != False]

        try:
            del data[True]
            del data[False]
        except:
            pass

        for col in columns:
            for index, value in df[col].items():
                for new in new_col:
                    if isinstance(value, list) and new in value and new in temp_dict.keys():
                        data[temp_dict[new]].loc[index] = True
                    elif isinstance(value, list) and new in value:
                        data[new].loc[index] = True
                    elif (isinstance(value, int) or isinstance(value, str)) and new == value and new in temp_dict.keys():
                        data[temp_dict[new]].loc[index] = True
                    elif (isinstance(value, int) or isinstance(value, str)) and new == value:
                        data[new].loc[index] = True
            if delete == True:
                del data[col]

        return data

    @property
    def explore_column_names(self):
        df = self.df
        data = df.copy()
        wrong = []
        tomuch = {}

        double_columns = data.columns[data.columns.duplicated()]
        try:
            if double_columns.values:
                raise ValueError
        except ValueError:
            print('These columns cant be in the dataframe multiple times: {0}'.format(double_columns.unique().values))
            return

        data = data.rename(columns=str.lower)
        # removes all double spaces in column name
        data.columns = data.columns.str.replace('\s?\s+', ' ', regex=True)
        # Removes all spaces at the start and end
        data.columns = data.columns.str.strip()

        exceptions = {'ü': 'u', 'ä': 'a', 'ö': 'o', 'ë': 'e', 'ï': 'i', '%': '_procent_', '&': '_and_', ' ': '_', '-': '_'}

        for v, k in exceptions.items():
            data.columns = data.columns.str.replace(v, k)

        data.columns = data.columns.str.replace('__', '_')

        # removes all the values that Javascript doesnt allow
        data.columns = data.columns.str.replace('[^0-9_$a-z]', '', regex=True)

        for i in data.columns:
            original = i
            try:
                if re.match(r'[^_$a-z]', i[0]) or re.match(r'_', i[-1]):
                    while re.match(r'[^_$a-z]', i[0]):
                        i = i[1:]
                        if re.match(r'_', i[0]):
                            i = i[1:]

                    while re.match(r'_', i[-1]):
                        i = i[:-1]
                    data.rename(columns={original: i}, inplace=True)
            except IndexError as error:
                wrong.append(original)

        dup_columns = data.columns[data.columns.duplicated()]

        for index, (first, second) in enumerate(zip(df.columns, data.columns)):
            if first != second:
                print(first, '--->', second)
            if second in wrong:
                index = wrong.index(second)
                wrong[index] = first
            elif second in dup_columns.values:
                tomuch.setdefault(second, []).append(first)

        if tomuch:
            print('')
            for key, value in tomuch.items():
                print('The values {1} will be changed to: {0}'.format(key, value))

        if wrong:
            print('\nThe columnname(s) are invalid: {0}'.format(wrong))

    @property
    def explore_datatypes(self):
        df = self.df
        print(f"{'index' : <8}{'type' : <10}{'dtype' : <8}{'nulls' : <6}{'nunique': <10}{'column' : <1}")
        for i in df:
            try:
                a = df[i].dropna().unique()
            except:
                type = 'list'
            else:
                if df[i].isna().sum() == df[i].shape[0]:
                    type = 'empty'
                elif all(isinstance(element, (bool, np.bool_)) for element in a):
                    type = 'boolean'
                elif all(isinstance(element, (np.int64, np.float64, int, float)) for element in a):
                    type = 'number'
                elif all(isinstance(element, str) for element in a):
                    type = 'string'
                elif all(isinstance(element, (pd.Timestamp, np.datetime64)) for element in a):
                    type = 'datetime'
                else:
                    type = 'multiple'

                # prints index of the column
                def index():
                    return "\033[0;30m" + f"{df.columns.get_loc(i) : <7}"

                # prints the type of all the values
                def etype():
                    if type == 'empty':
                        return "\033[0;31m" + f"{type : <9}"
                    else:
                        return "\033[0;30m" + f"{type : <9}"

                # prints the dtypes
                def dtype():
                    return "\033[0;30m" + f"{df[i].dtype.name: <7}"

                # prints the number of nulls
                def nulls():
                    if type == 'empty':
                        return "\033[0;31m" + f"{df[i].isna().sum(): <5}"
                    else:
                        return "\033[0;30m" + f"{df[i].isna().sum(): <5}"

                # prints the number of unique values
                def nunique():
                    if type == 'list':
                        return "\033[0;30m" + f"{'NaN': <9}"
                    else:
                        if type == 'empty':
                            return "\033[0;31m" + f"{df[i].nunique() : <9}"
                        elif df[i].nunique() == 1:
                            return "\033[0;31m" + f"{df[i].nunique(): <9}"
                        return "\033[0;30m" + f"{df[i].nunique(): <9}"

                # prints the column name
                def column():
                    return "\033[0;30m" + f"{i : <6}"

            print(index(),etype(),dtype(),nulls(),nunique(),column())

        pass

    def column_merge(self, columns, delete = False):
        df = self.df
        data = df.copy()
        dict = {}
        double_columns = df.columns[df.columns.duplicated()]
        double = []

        if not isinstance(delete, bool):
            print("\033[0;31m" + "delete is supposed to be a boolean")
            return

        try:
            if isinstance(columns, list):
                pass
            else:
                raise TypeError
        except TypeError:
            print("\033[0;31m" + 'A list was expected')
            return

        try:
            if len(columns) <= 1:
                raise IndexError
        except IndexError:
            print("\033[0;31m" + 'The list must have multiple values')
            return

        [double.append(x) for x in columns if (x in double_columns.unique().values) and (x not in double)]

        try:
            if double:
                raise ValueError
        except ValueError:
            print('These columns cant be in the dataframe multiple times: {0}'.format(double))
            return

        for c in columns:
            if c == columns[0]:
                pass
            else:
                dict[c] = columns[0]

        for k, v in dict.items():
            data[v] = np.where(data[v].isnull(), data[k], data[v])
            if delete == True:
                del data[k]

        return data

    def column_to_numeric(self, columns, force = False):
        df = self.df
        data = df.copy()
        error_value = []
        double_columns = df.columns[df.columns.duplicated()]
        double = []

        if not isinstance(force, bool):
            print("\033[0;31m" + "force is supposed to be a boolean")
            return

        try:
            if isinstance(columns, list):
                pass
            else:
                raise TypeError
        except TypeError:
            print("\033[0;31m" + 'A list was expected')
            return

        [double.append(x) for x in columns if (x in double_columns.unique().values) and (x not in double)]

        try:
            if double:
                raise ValueError
        except ValueError:
            print('These columns cant be in the dataframe multiple times: {0}'.format(double))
            return df

        for col in columns:
            try:
                if all((isinstance(i, (np.int64, np.float64, int, float, str)) or pd.isna(i)) for i in df[col].unique()):
                    for i, val in df[col].items():
                        if isinstance(val, (np.int64, np.float64, int, float)) or pd.isna(val):
                            pass
                        elif re.match('([0-9]+(([,.])?[0-9]+)?)$', val):
                            data[col].iloc[i] = pd.to_numeric(val.replace(',', '.'))
                        else:
                            if not re.match('([0-9]+(([,.])?[0-9]+)?)$', val) and force == True:
                                data[col].loc[i] = np.nan
                            elif not (re.match('([0-9]+(([,.])?[0-9]+)?)$', val)):
                                error_value.append(val)
                        if error_value:
                            raise ValueError
                else:
                    raise TypeError

            except TypeError:
                print("\033[0;31m" + "The column {0} doesn't contain only strings".format(col))
                return

            except ValueError:
                print("\033[0;31m" + "The column {0} has values which can't be converted to numbers: {1}".format(col, error_value))
                return

        return data

    def replace_double_column_names(self):
        df = self.df.copy()
        dup_columns = df.columns[df.columns.duplicated()]
        df_columns = df.columns
        new_columns = []
        dict = {}

        for item in df_columns:
            counter = 0
            newitem = item
            while newitem in new_columns:
                counter += 1
                newitem = "{}_{}".format(item, counter)
            new_columns.append(newitem)
        df.columns = new_columns

        for i, c in dup_columns.value_counts().iteritems():
            for c in range(c):
                dict['%s_%s' % (i, c + 1)] = i

        return df

    def sorting(self):
        df = self.df
        data = df.copy()

        data = data.reindex(sorted(data.columns), axis=1)

        return data

    def explore_double(self):
        df = self.df.copy()
        dup_columns = df.columns[df.columns.duplicated()]
        df_columns = df.columns
        new_columns = []
        change_columns = []
        dict = {}

        if not dup_columns.values.any():
            print("\033[0;31m" + "There are no double column names")
            return

        for item in df_columns:
            counter = 0
            newitem = item
            while newitem in new_columns:
                counter += 1
                newitem = "{}_{}".format(item, counter)
                if newitem not in change_columns:
                    if item not in change_columns:
                        change_columns.append(item)
                    change_columns.append(newitem)
            new_columns.append(newitem)
        df.columns = new_columns

        for i, c in dup_columns.value_counts().iteritems():
            for c in range(c):
                dict['%s_%s' % (i, c + 1)] = i

        df = df[change_columns].reindex(sorted(df[change_columns].columns), axis=1)

        return df

    def cleaning(self):
        df = self.df
        data = df.copy()
        double_columns = df.columns[df.columns.duplicated()]
        double = []


        try:
            if double:
                raise ValueError
        except ValueError:
            print('These columns cant be in the dataframe multiple times: {0}'.format(double))
            return

        # Makes all the columns lowercase
        data = data.rename(columns=str.lower)

        try:
            data = data.applymap(lambda x: pd.to_numeric(x, errors='ignore'))
        except:
            pass

        # removes all dubble spaces in column name
        data.columns = data.columns.str.replace('\s+s+', ' ', regex=True)
        # Replaces all spaces with underscores
        data.columns = data.columns.str.replace(' ', '_')
        # Replaces all 'streepjes' with underscores
        data.columns = data.columns.str.replace('-', '_')
        # Removes all spaces at the start and end
        data.columns = data.columns.str.strip()

        exceptions = {'ü': 'u', 'ä': 'a', 'ö': 'o', 'ë': 'e', 'ï': 'i', '%': '_procent_', '&': '_and_', ' ': '_', '-': '_'}

        for v, k in exceptions.items():
            data.columns = data.columns.str.replace(v, k)

        data.columns = data.columns.str.replace('__', '_')

        # removes all the values that Javascript doesnt allow
        data.columns = data.columns.str.replace('[^0-9_$a-z]', '', regex=True)

        # trimms all values
        data = data.applymap(lambda x: x.strip() if type(x) == str else x)
        data = data.applymap(lambda x: ' '.join(x.split()) if type(x) == str else x)

        for i in data:
            l = i
            try:
                while re.match('[^_$a-z]', i[0]):
                    i = i[1:]
                data.rename(columns={l: i}, inplace=True)

            except IndexError as error:
                print('the column {0} contains no letter, underscore or dollar sign, how should the column be named?'.format(l))
                colname = ''
                while colname == '' or re.match('[^_$a-z]', colname[0]) or colname in data.columns:
                    colname = input('{0} to: '.format(l))
                data.rename(columns={l: colname}, inplace=True)

        new_columns = []

        for index, (first, second) in enumerate(zip(df.columns, data.columns)):

            newitem = second
            while second in new_columns and (newitem == '' or re.match('[^_$a-z]', newitem[0]) or newitem in data.columns):
                newitem = input("{0} to: ".format(first))
            new_columns.append(newitem)
        data.columns = new_columns

        monthname = 'january|february|march|april|may|june|july|august|september|october|november|december'
        shortmonts = 'jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|march|april|june|july'

        day = r'((3[01]){1}|([12][0-9]){1}|(0?[1-9]){1}){1}'
        month = r'((1[0-2]){1}|(0?[1-9]){1}){1}'
        year = r'([12]{1}[0-9]{3}){1}'
        hms = r'(([2][0-3]){1}|([0-1][0-9]){1}){1}(:[0-5]{1}[0-9]{1}){2}'

        date_dict = {
            r'\b(' + year + '-{1}' + month + '-{1}' + day + ' ' + hms + r')\b': '%Y-%m-%d %H:%M:%S',
            r'\b(' + year + '-{1}' + day + '-{1}' + month + ' ' + hms + r')\b': '%Y-%d-%m %H:%M:%S',
            r'\b(' + day + '-{1}' + month + '-{1}' + year + ' ' + hms + r')\b': '%d-%m-%Y %H:%M:%S',
            r'\b(' + month + '-{1}' + day + '-{1}' + year + ' ' + hms + r')\b': '%m-%d-%Y %H:%M:%S',
            r'\b(' + day + '/{1}' + month + '/{1}' + year + r')\b': '%d/%m/%Y',
            r'\b(' + month + '/{1}' + day + '/{1}' + year + r')\b': '%m/%d/%Y',
            r'\b(' + year + '/{1}' + month + '/{1}' + day + r')\b': '%Y/%m/%d',
            '((3[01]|[12][0-9]|0?[1-9])-(1[0-2]|0?[1-9])-([12][0-9]{3}))': '%d-%m-%Y',
            '((1[0-2]|0?[1-9])-(3[01]|[12][0-9]|0?[1-9])-([12][0-9]{3}))': '%m-%d-%Y',
            '(([12][0-9]{3})-(1[0-2]|0?[1-9])-(3[01]|[12][0-9]|0[1-9]))': '%Y-%m-%d',
            '(' + monthname + ' (3[01]|[12][0-9]|[1-9]), ([12][0-9]{3}))': '%B %d, %Y',
            '(([12][0-9]{3}), (3[01]|[12][0-9]|[1-9]) ' + monthname + ')': '%Y, %d %B',
            '([12][0-9]{3}, (' + monthname + ') (3[01]|[12][0-9]|[1-9]))': '%Y, %B %d',
        }

        strings = []
        numbers = []
        dates = []
        lists = []

        for i in data:
            try:
                a = data[i].unique()
            except:
                data[i] = data[i].apply(lambda x: [x] if type(x) is not np.ndarray else x)
                lists.append(i)
            else:
                r = r"(" + ")|(".join(date_dict) + ")"
                if all(isinstance(element, (np.int64, np.float64, int, float)) for element in a):
                    numbers.append(i)
                elif all(isinstance(element, str) for element in a):
                    temp = []
                    for aa in a:
                        if re.match(r, aa, flags=re.IGNORECASE):
                            temp.append(aa)
                    if len(a) == len(temp):
                        dates.append(i)
                    else:
                        strings.append(i)
                else:
                    data[i] = data[i].apply(str)
                    strings.append(i)
        #
        for i in dates:
            for k in date_dict.keys():
                data[i] = data[i].apply(
                    lambda x: time.mktime(datetime.strptime(x, date_dict[k]).timetuple()) if type(x) == str and (
                        re.match(k, x, flags=re.IGNORECASE)) else x)

        return data