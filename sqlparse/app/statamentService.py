import sqlparse
from sqlparse.sql import Statement, Token, Where
from sqlparse import tokens as TokenType

token_select = Token(TokenType.Keyword.DML,'SELECT')
token_space = Token(TokenType.Text.Whitespace,' ')
token_asterist = Token(TokenType.Wildcard,'*')
token_from = Token(TokenType.Keyword, 'FROM')

def format_statament(string:str):
    """
    Remove WhiteSpace after sentence
    :param string:
    :return:
    """
    string_statament = sqlparse.format(string, strip_comments=True)
    return string_statament

def remove_all_extra_spaces(string:str):
    string=" ".join(string.split())
    return format_statament(string)

def select_converter(string_stataments: str):
    string_stataments=remove_all_extra_spaces(string_stataments)
    tuple_statament = sqlparse.parse(string_stataments)
    print("Cantidad de querys: " + str(len(tuple_statament)))
    validate_stataments(tuple_statament)
    list_select = []
    for statament in tuple_statament:
        print('Statement Inicial: ' + str(statament))
        string_select=''
        if statament.get_type()!='INSERT' and statament.get_type()!='SELECT':
            string_select = str(get_statament_converted(statament))
        list_select.append(string_select)
        print('Statement   Final: ' + str(string_select))
    return list_select;

def validate_stataments(tuple_statament):
    for statament in tuple_statament:
        if statament.get_type() == 'UNKNOWN':
            raise Exception("Sintasis Incorrecta:" + str(statament))
        # if statament.get_type() == 'SELECT':
        #     raise Exception("Sentencia SELECT no es permitida :" + str(statament))

def get_stat_select_from():
    stat_select_from=[token_select,token_space,token_asterist,token_space,token_from]
    return stat_select_from;

def insert_dml_select(statament: Statement):
    list_tokens = statament.tokens
    stat_select_from=get_stat_select_from()
    list_tokens[0:0]=stat_select_from

def is_token_set(token:Token):
    return token.value.upper()=='SET' and token.ttype==TokenType.Keyword

def is_token_final(token:Token):
    return token.value.upper()==';' and token.ttype==TokenType.Punctuation

def is_token_where(token:Token):
    return isinstance(token, Where)

def remove_keyword_set(statament: Statement):
    list_tokens = statament.tokens
    index_token_set=index_token_where=index_token_final=0
    for i, token in enumerate(list_tokens):
        if is_token_set(token):
            index_token_set = i
        if is_token_where(token):
            index_token_where = i
        if is_token_final(token):
            index_token_final = i
    if index_token_set<index_token_where:
        del list_tokens[index_token_set:index_token_where]
    else:
        del list_tokens[index_token_set:index_token_final]

def remove_first_tokens(statament: Statement,n:int):
    list_tokens = statament.tokens
    for i in range(n) :
        del list_tokens[0]

def get_statament_converted(statament: Statement):
    DML_TYPE=statament.get_type()
    if DML_TYPE in {'DELETE'}:
        remove_first_tokens(statament,3)
    elif DML_TYPE in {'UPDATE'}:
        remove_keyword_set(statament)
        remove_first_tokens(statament,1)
    insert_dml_select(statament)
    return statament;

if __name__ == "__main__":
    strings_query = '''
    '''
    list_querys_select=select_converter(strings_query)
    print('/*---------Select generado por Conveter SQL---------------------------------------*/')
    for query in list_querys_select:
        print(query)