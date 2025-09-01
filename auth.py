tokens_permitidos = {'abc', 'xyz789'} # conjunto con los tokens validos aceptados

# este parametro puede ser un string o none - esta funcion devuelve un booleano
def es_token_valido(autorizacion_header: str | None) -> bool:
    if not autorizacion_header: return False # si no mandaron header, devuelve falso
    partes = autorizacion_header.split() 
    return (len(partes) == 2 
            and partes[0].lower() == 'token' 
            and partes[1] in tokens_permitidos) 
