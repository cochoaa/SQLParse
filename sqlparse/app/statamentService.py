import sqlparse
import re
from checkSintax import check_statament
from sqlparse.sql import Statement, Token, Where
from sqlparse import tokens as TokenType

token_select = Token(TokenType.Keyword.DML,'SELECT')
token_space = Token(TokenType.Text.Whitespace,' ')
token_asterist = Token(TokenType.Wildcard,'*')
token_from = Token(TokenType.Keyword, 'FROM')
token_comma = Token(TokenType.Punctuation, ',')

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
    return string
def remove_all_extra_coments(string:str):
    string = format_statament(string)
    regex = "--.*"
    filtered_lines = []
    for line in string.splitlines():
        result = re.search(regex,line)
        if result:
            token = result.group()
            line = line.replace(token,'')
        filtered_lines.append(line)
    string="\r".join(filtered_lines)
    return string

def check_syntax_statament(query:str):
     success, msg=check_statament(query)
     print(msg)
     if not success:
        raise Exception(msg+':\r'+query)

def select_converter(string_stataments: str):
    string_stataments=remove_all_extra_coments(string_stataments)
    string_stataments = remove_all_extra_spaces(string_stataments)
    tuple_statament = sqlparse.parse(string_stataments)
    print("Cantidad de querys: " + str(len(tuple_statament)))

    list_select = []
    list_errors = []
    error=False
    for statament in tuple_statament:
        print('Statement Inicial: ' + str(statament))
        string_select=''
        try:
            check_syntax_statament(str(statament))
            if statament.get_type() != 'INSERT' and statament.get_type() != 'SELECT':
                string_select = str(get_statament_converted(statament))
        except Exception as e:
            error = True
            list_errors.append(str(e))
        list_select.append(string_select)
        print('Statement   Final: ' + str(string_select))
    if error:
        list_select=list_errors
    return error,list_select

def get_stat_select_from():
    stat_select_from=[token_select,token_space,token_asterist,token_space,token_from]
    return stat_select_from

def insert_dml_select(statament: Statement):
    list_tokens = statament.tokens
    stat_select_from=get_stat_select_from()
    list_tokens[0:0]=stat_select_from

def insert_dml_join(statament: Statement,token_table_join: Token):
    list_tokens = statament.tokens
    stat_join = [token_comma,token_table_join]
    list_tokens[3:3] = stat_join

def is_token_set(token:Token):
    return token.value.upper()=='SET' and token.ttype==TokenType.Keyword

def is_token_final(token:Token):
    return token.value.upper()==';' and token.ttype==TokenType.Punctuation

def is_token_where(token:Token):
    return isinstance(token, Where)
def is_token_from(token:Token):
    return token.value.upper()=='FROM' and token.ttype==TokenType.Keyword

def remove_keyword_set(statament: Statement):
    list_tokens = statament.tokens
    index_token_set=index_token_final = 0
    index_token_where = None
    index_token_from = None
    for i, token in enumerate(list_tokens):
        if is_token_set(token):
            index_token_set = i
        if is_token_from(token):
            index_token_from = i
        if is_token_where(token):
            index_token_where = i
        if is_token_final(token):
            index_token_final = i
    if  index_token_from:
        del list_tokens[index_token_set:index_token_from]
    elif index_token_where:
        del list_tokens[index_token_set:index_token_where]
    else:
        del list_tokens[index_token_set:index_token_final]

def pop_keyword_from(statament: Statement):
    list_tokens = statament.tokens
    index_token_from = None
    table = None
    for i, token in enumerate(list_tokens):
        if is_token_from(token):
            index_token_from = i
    if  index_token_from:
        del list_tokens[index_token_from:index_token_from+2]#remove FROM and space
        table = list_tokens.pop(index_token_from)
    return table
def remove_first_tokens(statament: Statement,n:int):
    list_tokens = statament.tokens
    for i in range(n) :
        del list_tokens[0]

def converter_update(statament: Statement):
    remove_keyword_set(statament)
    table=pop_keyword_from(statament)
    if table:
        insert_dml_join(statament,table)
    remove_first_tokens(statament, 1)
    insert_dml_select(statament)
    return statament

def converter_delete(statament: Statement):
    remove_first_tokens(statament, 3)
    insert_dml_select(statament)
    return statament

def get_statament_converted(statament: Statement):
    DML_TYPE=statament.get_type()
    if DML_TYPE in {'DELETE'}:
        converter_delete(statament)
    elif DML_TYPE in {'UPDATE'}:
        converter_update(statament)
    return statament

if __name__ == "__main__":
    strings = '''
    --------------------------------------- CONTINUACION ---------------------------------------------
UPDATE bytsscom_bytpoa.plan_pim_transferencia  ppt
SET monto_trans = tbl.tresmeeses
FROM (SELECT  id_plan_pim_trans, trunc((monto_trans / 12 )*3,2) AS tresmeeses
FROM bytsscom_bytpoa.plan_pim_transferencia  where estado_trans != 'X' AND id_plan_pim_trans in (5661,5660,5659,5658,5657,5656,5655,5654,5653,5652,5651,5650,5649,5648,5647,5646,
										5645,5644,5643,5642,5641,5640,5639,5638,5637,5636,5635,5634,5633,5632)) tbl
										WHERE  tbl.id_plan_pim_trans = ppt.id_plan_pim_trans;
SELECT bytsscom_bytpoa.cuadro_necesidades_activate(6);
----
    '''
    list_querys_select=select_converter(strings)
    print('/*---------Select generado por Conveter SQL---------------------------------------*/')
    for query in list_querys_select:
        print(query)