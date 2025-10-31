import pandas

def merge_datasets(df1, df2, key):
    df1_copy = df1.copy()
    df2_copy = df2.copy()

    df_agg = df1_copy.merge(
        df2_copy, 
        left_on=key, 
        right_index=True, 
        how='left'
    )
    
    return df_agg