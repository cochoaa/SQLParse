import sqlparse
from sqlparse.sql import Statement, Token
from sqlparse import tokens as TokenType

token_select = Token(TokenType.Keyword.DML,'SELECT')
token_space = Token(TokenType.Text.Whitespace,' ')
token_asterist = Token(TokenType.Wildcard,'*')
token_from = Token(TokenType.Keyword, 'FROM')

def remove_all_extra_spaces(string:str):
    return " ".join(string.split())

def format_statament(string:str):
    string_statament = sqlparse.format(string, strip_comments=True, keyword_case='upper')
    print(string_statament)
    return string_statament

def select_converter(string_stataments: str):
    string_stataments=remove_all_extra_spaces(string_stataments)
    string_stataments=format_statament(string_stataments)
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
        print('Statement Final: ' + str(string_select))
    return list_select;


def validate_stataments(tuple_statament):
    for statament in tuple_statament:
        if statament.get_type() == 'UNKNOWN':
            raise Exception("Sintasis Incorrecta:" + str(statament))
        # if statament.get_type() == 'SELECT':
        #     raise Exception("Sentencia SELECT no es permitida :" + str(statament))

def get_statament_converted(statament: Statement):
    list_tokens=statament.tokens
    if statament.get_type() == 'UPDATE':
        list_tokens.pop(0)
        list_tokens.insert(0,token_select)
        list_tokens.insert(1, token_space)
        list_tokens.insert(2, token_asterist)
        list_tokens.insert(3, token_space)
        list_tokens.insert(4, token_from)
        list_tokens.pop(8)#set
        list_tokens.pop(8)#space
        list_tokens.pop(8)#valores
    elif statament.get_type() == 'DELETE':
        list_tokens.pop(0)
        list_tokens.insert(0,token_select)
        list_tokens.insert(1,token_space)
        list_tokens.insert(2,token_asterist)
    return statament;



if __name__ == "__main__":
    print("File1 is being run directly")
    strings_quey = '''              


SELECT * FROM bytsscom_bytsig.certificacion_meta WHERE id_certificacion=249594;

UPDATE bytsscom_bytsig.certificacion_meta 
   SET mont_meta_cert=23067.00 , mont_meta_nac=23067.00
 WHERE id_certificacion=249594;


SELECT * FROM bytsscom_bytsig.registro_meta WHERE id_registro=147493;

UPDATE bytsscom_bytsig.registro_meta 
SET monto_meta=23067.00, monto_soles=23067.00
WHERE id_registro=147493;

SELECT * FROM bytsscom_bytsig.certificacion WHERE id_certificacion=249594;

UPDATE bytsscom_bytsig.certificacion 
   SET esta_cert='A'
 WHERE id_certificacion=249594;


SELECT * FROM bytsscom_bytsig.certificacion_sec WHERE id_certificacion=249594;

UPDATE bytsscom_bytsig.certificacion_sec 
   SET estado_sec='A'
 WHERE id_certificacion=249594;



SELECT * FROM bytsscom_bytsig.certificacion WHERE id_certificacion=250131;
SELECT * FROM bytsscom_bytsig.certificacion_meta WHERE id_certificacion=250131;
SELECT * FROM bytsscom_bytsig.certificacion_sec WHERE id_certificacion=250131;


INSERT INTO      bytsscom_bytsig.certificacion(id_certificacion, id_anio,       fech_cert, esta_cert, siaf_certificado , tipo_cert, id_certificacion_sup, id_certdoc, id_referencia,  siaf_cert_secuencia,                                                                                                            desc_doc,            sys_fech_registro, id_tipooperacion, id_fuente, siaf_tipo_finan, num_transferencia, id_memo_requerimiento, id_proyecto, id_tipo_doc_ccp) 
				        VALUES(          250131,    2022,    '2022-03-29',       'A',      '0000004317',      'CA',               249289,      'AME',        287967,               '0003', '22-0002555 ENCARGO DEL PROYECTO: Contrato N°  28-2018-FONDECYT-BM-IADT-AV   A FAVOR DE :  ARAKAKI MAKISHI, MONICA', '2022-03-28 21:15:13.132828',              'A',        15,             'T',           '56578',                287967,        3598,         'PRENC');


INSERT INTO bytsscom_bytsig.certificacion_meta(id_certificacion, id_certificacion_sec, id_meta_corr, id_item, id_tarea_meta, mont_meta_cert, id_clasificador, mont_meta_nac)
				        VALUES(          250131,                    1,            1,       0,          9247,        7968.15,            1546,       7968.15);


INSERT INTO  bytsscom_bytsig.certificacion_sec(id_certificacion, id_certificacion_sec, estado_sec,   id_moneda,   tipo_camb_sec,                 nro_doc, siaf_correlativo,      fech_doc, id_tipo_documento)
				        VALUES(          250131,                    1,        'A',         390,        1.000000,       'RD-192-DGA-2022',           '0001',  '2022-03-28',               234);	


'''

    list_querys_select=select_converter(strings_quey)
    print('/*---------Select generado por Conveter SQL---------------------------------------*/')
    for query in list_querys_select:
        print(query)