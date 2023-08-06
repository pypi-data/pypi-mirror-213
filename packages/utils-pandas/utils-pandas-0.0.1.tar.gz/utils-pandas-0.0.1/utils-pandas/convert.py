def to_json(df, column=None):
    if column is None:
        column = df.columns[0]
    
    cols = df.columns.difference([column])
    d = (df.groupby(column)[cols]
            .apply(lambda x: x.to_dict('r'))
            .reset_index(name='dados')
            .to_dict(orient='records'))
    
    return d