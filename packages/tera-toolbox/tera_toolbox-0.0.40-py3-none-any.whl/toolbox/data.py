def get_url(table, select=["*"], params={}):
    url = "https://sygrjcqvvnsrvxczpnpx.supabase.co/rest/v1/"
    url = url + table
    
    if select:
        select_string = ','.join(select)
        url = url +"?" +"select="+ select_string
        
    if params:
        key_value_pairs = [f'&{key}=eq.{value}' if not isinstance(value, list) else f'&{key}=in.({", ".join(map(str, value))})' for key, value in params.items()]
        params_string = ''.join(key_value_pairs)
        url = url + params_string

    return url

def get_feriados(calendar="anbima"):
    url = get_url(table="feriados",select=['data','descricao'],params={'calendario':f'{calendar}'})
    return url
