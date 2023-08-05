def get_dataframe_as_csv(send, event, wsc):
    """
    Sends a dataframe as a CSV string
    """
    sheet_index = event['sheet_index']
    df = wsc.dfs[sheet_index]

    send({
        'event': 'api_response',
        'id': event['id'],
        'data': df.to_csv(index=False)
    })