import pandas as pd
import re
from typing import Union

def neat_display(objects):
    """
    Prints the investigtions in a neat way.
            Parameters:
                objects (list): List of Objects to be displyed
    """
    for _, __ in objects:
        print(_)
        display(__,)
        print(
            "______________________________________________________________________________"
        )
        print()

def list_clean(list_or_none):
    """
    Returns None if the list is empty.
            Parameters:
                    l (list): A List
            Returns:
                    list or None
    """
    if len(list_or_none) == 0:
        list_or_none = None
    return list_or_none

def merge_lists(lists: list) -> list:
    """
   Merge Tow lists or more.
            Parameters:
                    lists (list): A List of lists to be merged
            Returns:
                    Merged List or None
    """
    non_empty_lists = [l for l in lists if l is not None]

    if len(non_empty_lists) == 0:
        return []

    non_empty_lists = [x for list_ in non_empty_lists for x in list_]

    return list(set(non_empty_lists))


def data_investigation(df: pd.DataFrame):
    """
    Prints some investigtions of the Data Frame.
            Parameters:
                    df (DataFrame): The Data Frame to be investigated.
    """
    list_columns_has_one_value = []
    for c in df.columns:
        if df[[c]].value_counts().max() / df[[c]].shape[0] == 1:
            list_columns_has_one_value.append((c, df[[c]].values[0][0]))
    to_drop_one = list_clean(list_columns_has_one_value)
    if to_drop_one is not None:
        to_drop_one = pd.Series(
            [i[1] for i in list_columns_has_one_value],
            index=[i[0] for i in list_columns_has_one_value],
        )

    to_drop_null = list(df.columns[df.isnull().mean() == 1])
    to_drop_null = list_clean(to_drop_null)

    try:
        dtypes = pd.Series(
            [
                re.findall(r"<class '(.*)'>", str(type(i)))[0]
                for i in df.dropna(how="any").head(1).values[0]
            ],
            index=list(df.columns),
        )

    except:
        if to_drop_one is not None:
            if merge_lists([to_drop_null, list(to_drop_one.index)]) is not None:
                df_temp = df.drop(
                    columns=merge_lists([to_drop_null, list(to_drop_one.index)])
                )
        else:
            df_temp = df_temp = df.drop(columns=merge_lists([to_drop_null]))

        try:
            dtypes = pd.Series(
                [
                    re.findall(r"<class '(.*)'>", str(type(i)))[0]
                    for i in df_temp.dropna(how="any").head(1).values[0]
                ],
                index=list(df.columns),
            )
        except:

            types = []
            for col in df_temp.columns:
                types.append(
                    re.findall(
                        r"<class '(.*)'>",
                        str(type(df_temp[[col]].dropna().head(1).values[0][0])),
                    )[0]
                )
            dtypes = pd.Series(types, index=list(df_temp.columns))

    neat_display(
        [
            ("Data Head", df.head(2)),
            (
                "Data Shape",
                f"The data has {df.shape[0]} rows and {df.shape[1]} columns",
            ),
            ("Columns", list(df.columns)),
            ("Columns Must be Dropped (ALL NULLS)", to_drop_null,),
            ("Columns Must be Dropped (HAS ONLY ONE UNIQUE VALUE)", to_drop_one,),
            ("Column Data Type", dtypes),
            (
                "Number of Nulls in Each Column",
                df.isnull().sum().sort_values(ascending=False),
            ),
            (
                "Percentge of Nulls in Each Column",
                df.isnull().mean().sort_values(ascending=False),
            ),
            ("Numeric Columns' Staticts", df.describe()),
        ]
    )

def get_columns_to_drop(df: pd.DataFrame) -> Union[list, None]:
    """
    Return List of Columns to be dropped.
            Parameters:
                    df (DataFrame): The Data Frame to get the columns to drop from it.
            Returns:
                    List of columns to be dropped.
    """
    list_columns_has_one_value = []
    for c in df.columns:
        if df[[c]].value_counts().max() / df[[c]].shape[0] == 1:
            list_columns_has_one_value.append((c, df[[c]].values[0][0]))
    to_drop_one = list_clean(list_columns_has_one_value)
    if to_drop_one is not None:
        to_drop_one = pd.Series(
            [i[1] for i in list_columns_has_one_value],
            index=[i[0] for i in list_columns_has_one_value],
        )

    to_drop_null = list(df.columns[df.isnull().mean() == 1])
    to_drop_null = list_clean(to_drop_null)
    return merge_lists([to_drop_null, list(to_drop_one.index)])
