import sqlparse
querys=sqlparse.parse("DELETE FROM bytsscom_bytsig.registro_hoja_ruta_det WHERE id_registro_hr IN (SELECT id_registro_hr FROM bytsscom_bytsig.registro_hoja_ruta WHERE id_hoja_ruta_actual=31081) AND id_corr>4;UPDATE bytsscom_bytsig.registro_hoja_ruta set  id_hoja_ruta_actual=29732, id_corr_actual=4 where id_registro_hr in (SELECT id_registro_hr FROM bytsscom_bytsig.registro_hoja_ruta WHERE id_hoja_ruta_actual=31081);")
for query in querys:
	for token in query.tokens:
		print(token.value + ' ' + str(token.ttype))
