from pgsanity.pgsanity import check_string

# return 0,si es exitoso
def check_statament(query:str):
    success, msg = check_string(query, add_semicolon=True)
    message=''
    if not success:
        # possibly show the filename with the error message
        message =  msg
    return success,message

if __name__ == "__main__":
    strings_query = '''UPDATE bytsscom_bytsig.contrato_progdes SET mont_progdes = 38449.75 WHERE id_contrato= 127982 WHERE id_progdesembolso = 16053; 
    '''
    success, msg =check_statament(strings_query)
    result = 0
    print(msg)

