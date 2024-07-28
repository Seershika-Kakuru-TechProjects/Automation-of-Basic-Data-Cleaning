from sklearn.impute import SimpleImputer
import pandas as pd
import numpy as np
def handle_missing_values(df, col, option):
    if df[col].dtype == 'object':
        return handle_missing_cat_values(df, col, option)
    else:
        return handling_missing_num_values(df, col, option)


def handle_missing_cat_values(df, col, option):
    if option == 'missing':
        imputer = SimpleImputer(strategy='constant', fill_value='missing')
        df[col] = pd.DataFrame(imputer.fit_transform(df[[col]]))
    elif option == "mode":
        imputer = SimpleImputer(strategy='most_frequent')
        df[col] = pd.DataFrame(imputer.fit_transform(df[[col]]))
    else:
        num_empty_values = df[col].isnull().sum()
        if float(num_empty_values / df.shape[0]) > 0.50:
            df = df.drop(col, axis=1)
    return df


def handling_missing_num_values(df, col, option):
    if option == "mean":
        df[col] = df[col].fillna(df[col].mean())
    elif option == "mode":
        df[col] = df[col].fillna(df[col].mode())
    elif option == "median":
        df[col] = df[col].fillna(df[col].median())
    elif option == "ffill":
        df[col] = df[col].fillna(method="ffill")
    elif option == "bfill":
        df[col] = df[col].fillna(method="bfill")
    elif option == "quadratic interpolation":
        df[col] = df[col].interpolate("quadratic")
    elif option == "linear interpolation":
        df[col] = df[col].interpolate()
    else:
        num_empty_values = df[col].isnull().sum()
        if float(num_empty_values / df.shape[0]) > 0.50:
            df = df.drop(col, axis=1)
    return df

def cat_datatype_conversion (df, col, option):
    if option == "int":
        df[col] = df[col].astype("int")
    elif option == "float":
        df[col] = df[col].astype("float")
    else:
        df[col] = pd.to_datetime(df[col])
    return df

def remove_outliers(df, col):
    percentile25 = df[col].quantile(0.25)
    percentile75 = df[col].quantile(0.75)
    iqr = percentile75 - percentile25
    upper_limit = percentile75 + 1.5 * iqr
    lower_limit = percentile25 - 1.5 * iqr
    upper_array = np.where(df[col] >= upper_limit)[0]
    lower_array = np.where(df[col] <= lower_limit)[0]
    df.drop(index=upper_array, inplace=True)
    df.drop(index=lower_array, inplace=True)
    return df
