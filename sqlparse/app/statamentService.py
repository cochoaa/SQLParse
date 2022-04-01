import sqlparse
from sqlparse.sql import Statement, Token, Where, Identifier as Table
from sqlparse import tokens as TokenType

token_select = Token(TokenType.Keyword.DML,'SELECT')
token_space = Token(TokenType.Text.Whitespace,' ')
token_asterist = Token(TokenType.Wildcard,'*')
token_from = Token(TokenType.Keyword, 'FROM')

def remove_all_extra_spaces(string:str):
    return " ".join(string.split())

def format_statament(string:str):
    string_statament = sqlparse.format(string, strip_comments=True, keyword_case='upper')
    return string_statament

def select_converter(string_stataments: str):
    string_stataments=remove_all_extra_spaces(string_stataments)
    string_stataments=format_statament(string_stataments)
    tuple_statament = sqlparse.parse(string_stataments)
    print("Cantidad de querys: " + str(len(tuple_statament)))
    validate_stataments(tuple_statament)
    list_select = []
    for statament in tuple_statament:
        if statament.get_type()!='INSERT':
            string_select = statament_converter(statament)
        list_select.append(string_select)
    return list_select;


def validate_stataments(tuple_statament):
    for statament in tuple_statament:
        if statament.get_type() == 'UNKNOWN':
            raise Exception("Sintasis Incorrecta:" + str(statament))
        if statament.get_type() == 'SELECT':
            raise Exception("Sentencia SELECT no es permitida :" + str(statament))

def statament_converter(statament: Statement):
    print('Statement Inicial: ' + str(statament))
    list_tokens=statament.tokens
    if statament.get_type() == 'UPDATE':
        list_tokens.pop(0)
        list_tokens.insert(0,token_select)
        list_tokens.insert(1, token_space)
        list_tokens.insert(2, token_asterist)
        list_tokens.pop(6)#set
        list_tokens.pop(6)#space
        list_tokens.pop(6)#valores
    elif statament.get_type() == 'DELETE':
        list_tokens.pop(0)
        list_tokens.insert(0,token_select)
        list_tokens.insert(1,token_space)
        list_tokens.insert(2,token_asterist)
    return str(statament);



if __name__ == "__main__":
    print("File1 is being run directly")
    strings_quey = '''              
    
    delete   FROM        bytsscom_bytsig.registro_hoja_ruta_det WHERE id_registro_hr     IN (SELECT id_registro_hr FROM bytsscom_bytsig.registro_hoja_ruta WHERE id_hoja_ruta_actual=31081) AND id_corr>4;
                        
                        
    UPDATE      bytsscom_bytsig.registro_hoja_ruta set  id_hoja_ruta_actual=29732, id_corr_actual=4 where id_registro_hr in (SELECT id_registro_hr FROM bytsscom_bytsig.registro_hoja_ruta WHERE id_hoja_ruta_actual=31081);
      
      
      
            UPDATE WEBQPROTESORERIA.LISTA_ITEM_SERVICIO   t
    SET t.UDIDESTAB = 12100
    WHERE t.UD_ID = 12100
      AND t.COD_ITEM LIKE '10759';'''

    list_querys_select=select_converter(strings_quey)
    for query in list_querys_select:
        print(query)