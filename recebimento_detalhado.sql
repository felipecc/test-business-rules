SELECT ROWNUM id
     , documento_id
     , doc_origem_id
     , documentonf
     , doc_numero_pedido
     , (SELECT LISTAGG(OP.NOMECODIGO  , ', ') WITHIN GROUP (ORDER BY OP.NOMECODIGO )
          FROM BENNERCORP.CN_LIBERACOESFATURAMENTO LF
             , BENNERCORP.CN_CONTRATOS CONTRATO
             , BENNERCORP.CN_CONTRATOOBJETOS CO
             , BENNERCORP.K_CODIGOOPORTUNIDADE OP
             , BENNERCORP.CM_ITENS I
             , BENNERCORP.FN_DOCUMENTOS DOC_ORIGEM
             , BENNERCORP.FN_DOCUMENTOS D
         WHERE LF.CONTRATO = CONTRATO.HANDLE
           AND LF.CONTRATOOBJETO = CO.HANDLE
           AND CO.K_CODIGOOPORTUNIDADE = OP.HANDLE
           AND LF.STATUS = 2
           AND CONTRATO.TIPOCONTRATO IN (9,10)
           AND LF.ITEMNF = I.HANDLE
           AND I.DOCUMENTO = DOC_ORIGEM.HANDLE
           AND DOC_ORIGEM.DOCUMENTOORIGEM = D.HANDLE
           AND i.handle = recebido.item_id
     ) OPORTUNIDADE
     , EMPRESA
     , FILIAL_ID
     , FILIAL
     , numero_nota
     , item_id
     , item
     , emissao
     , datacancelamento
     , datavencimento
     , datainclusao
     , dataliquidacao
     , dt_recebimento data_da_baixa
     , codigo_cliente_portal_fin
     , codigo_cliente
     , nome_cliente
     , parcela_id
     , REPLACE(to_char(valor_faturado_bruto, '99999999999999999999999990D999999', 'nls_numeric_characters='',.'''),' ','') valor_faturado_bruto
     , REPLACE(to_char(valor_faturado_liquido, '99999999999999999999999990D999999', 'nls_numeric_characters='',.'''),' ','') valor_faturado_liquido
     /*FORMULA: valor_do_item / valor_faturado_bruto */
     , REPLACE(to_char(Round((valor_do_item / valor_faturado_bruto),6), '99999999999999999999999990D999999', 'nls_numeric_characters='',.'''),' ','')  fator_do_item
     /*FORMULA: valor_faturado_liquido - (valor_faturado_bruto * ( aliquota_iss / 100))*/
     , REPLACE(to_char(valor_faturado_liquido - (valor_faturado_bruto * ( aliquota_iss / 100)), '99999999999999999999999990D999999', 'nls_numeric_characters='',.'''),' ','') valor_faturado_liquido_s_iss
     , REPLACE(to_char(valor_do_item, '99999999999999999999999990D999999', 'nls_numeric_characters='',.'''),' ','') valor_do_item
     , REPLACE(to_char(valor_parcela, '99999999999999999999999990D999999', 'nls_numeric_characters='',.'''),' ','') valor_parcela
     /*FORMULA: valor_parcela * (valor_do_item / valor_faturado_bruto )*/
     , REPLACE(to_char(Round(valor_parcela * (valor_do_item / valor_faturado_bruto ),6), '99999999999999999999999990D999999', 'nls_numeric_characters='',.'''),' ','')   valor_a_rec_por_item
     , REPLACE(to_char(Round((aliquota_iss / 100),6), '99999999999999999999999990D999999', 'nls_numeric_characters='',.'''),' ','')  aliquota_iss
     /*FORMULA: (valor_faturado_bruto * (valor_parcela * (valor_do_item / valor_faturado_bruto )) / valor_faturado_liquido) * ( aliquota_iss / 100)*/
     , REPLACE(to_char(Round(((valor_faturado_bruto * (valor_parcela * (valor_do_item / valor_faturado_bruto )) / valor_faturado_liquido) * ( aliquota_iss / 100)),6), '99999999999999999999999990D999999', 'nls_numeric_characters='',.'''),' ','')  valor_iss_da_parcela
     /* FORMULA: (valor_parcela * (valor_do_item / valor_faturado_bruto )) - (valor_faturado_bruto * (valor_parcela * (valor_do_item / valor_faturado_bruto )) / valor_faturado_liquido) * ( aliquota_iss / 100)*/
     , REPLACE(to_char(Round((valor_parcela * (valor_do_item / valor_faturado_bruto )) - (valor_faturado_bruto * (valor_parcela * (valor_do_item / valor_faturado_bruto )) / valor_faturado_liquido) * ( aliquota_iss / 100),6), '99999999999999999999999990D999999', 'nls_numeric_characters='',.'''),' ','')  valor_a_rec_por_item_s_iss
     , REPLACE(to_char(vl_recebido_bruto, '99999999999999999999999990D999999', 'nls_numeric_characters='',.'''),' ','') vl_recebido_bruto
     , REPLACE(to_char(vl_recebido_liquido, '99999999999999999999999990D999999', 'nls_numeric_characters='',.'''),' ','') vl_recebido_liquido

     , REPLACE(to_char(Round((vl_recebido_liquido * (valor_do_item / valor_faturado_bruto)),6), '99999999999999999999999990D999999', 'nls_numeric_characters='',.'''),' ','')  valor_recebido_por_item
     , REPLACE(to_char(Round((vl_recebido_bruto * (valor_do_item / valor_faturado_bruto)),6), '99999999999999999999999990D999999', 'nls_numeric_characters='',.'''),' ','')  valor_recebido_por_item_bruto
     , REPLACE(to_char(Round((vl_juros_recebido),6), '99999999999999999999999990D999999', 'nls_numeric_characters='',.'''),' ','')  vl_juros_recebido
     /* FORMULA: (valor_parcela_bruto + valor_juros_recebido *  fator_do_item */
     , REPLACE(to_char(Round((vl_recebido_bruto * (valor_do_item / valor_faturado_bruto) + vl_juros_recebido * (valor_do_item / valor_faturado_bruto)),6), '99999999999999999999999990D999999', 'nls_numeric_characters='',.'''),' ','') valor_rec_por_item_bruto_c_j
      /*VALOR LIQUIDO RECEBIDO POR PARCELA - (VALOR_ISS_DA_PARCELA * FATOR_PARCELA_RECEBIDO) */
     , REPLACE(to_char(Round((vl_recebido_liquido * (valor_do_item / valor_faturado_bruto)) - ((valor_faturado_bruto * (valor_parcela * (valor_do_item / valor_faturado_bruto )) / valor_faturado_liquido) * ( aliquota_iss / 100)),6), '99999999999999999999999990D999999', 'nls_numeric_characters='',.'''),' ','') valor_base_comissao
     , recebido.handle_item
  FROM (
SELECT FD.HANDLE  DOCUMENTO_ID
      , DOC_ORIGEM.HANDLE  DOC_ORIGEM_ID
      , FD.NUMEROPEDIDO  doc_numero_pedido
      , FD.DOCUMENTODIGITADO DOCUMENTONF
      , E.HANDLE EMPRESA_ID
      , E.NOME EMPRESA
      , FD.FILIAL FILIAL_ID
      , F.NOME FILIAL
      , FD.NRNOTAFISCAL numero_nota
      , To_Char(FD.DATAEMISSAO,'DD/MM/YY') EMISSAO
      , To_Char(FD.DATACANCELAMENTO,'DD/MM/YY') DATACANCELAMENTO
      , To_Char(FP.datavencimento,'DD/MM/YY') datavencimento
      , To_Char(FP.datainclusao,'DD/MM/YY') datainclusao
      , To_Char(FP.dataliquidacao,'DD/MM/YY') dataliquidacao
      , C.K_CODIGOPORTALFINANCEIRO codigo_cliente_portal_fin
      , C.codigo codigo_cliente
      , c.nome nome_cliente
      , CI.VALORTOTAL VALORTOTALITEM
      , To_Char(TRUNC(FD.DATAEMISSAO,'MM'),'DD/MM/YY') COMPETENCIA
      , PP.HANDLE item_id
      , FP.HISTORICO historico_parcela
      , TRIM(REPLACE(REPLACE(PP.DESCRICAO,CHR(13),''),CHR(10),'')) ITEM
      , fp.handle parcela_id
      , FD.VALORESBAIXADOS  DOC_VALOR_BAIX
      , FD.ABATIMENTOS      DOC_VALOR_ABAT
      , FD.ACRESCIMOS       DOC_VALOR_ACREC
      , fd.valornominal     valor_faturado_bruto
      , fd.valorliquido     valor_faturado_liquido
      , FP.VALOR            VALOR_PARCELA
      , FP.valoresbaixados VALOR_PARCE_BAIX
      , Sum(CI.VALORTOTAL) valor_do_item
      , Nvl(fdt.aliquotaiss,0) aliquota_iss
      , FD.TIPODOCUMENTO
      , FD.HISTORICO historico_documento
      , FD.documentocontabil
      , FD.valoresbaixados VALOR_DOCUMENTO
      , FD.abatimentos VALOR_ABAT_DOCUMENTO
      , FD.acrescimos VALOR_ACRE_DOCUMENTO
      , To_Char(rec.dt_recebimento,'DD/MM/YY') dt_recebimento
      , rec.vl_recebido_liquido
      , rec.vl_recebido_bruto
      , rec.vl_juros_recebido
      , ci.handle handle_item

  FROM BENNERCORP.FN_DOCUMENTOS FD
     , BENNERCORP.FN_DOCUMENTOS DOC_ORIGEM
     , BENNERCORP.FN_PARCELAS FP
     , BENNERCORP.EMPRESAS E
     , BENNERCORP.FILIAIS F
     , BENNERCORP.CM_ITENS CI
     , BENNERCORP.PD_PRODUTOS PP
     , BENNERCORP.GN_PESSOAS C
     , BENNERCORP.FN_DOCUMENTOTRIBUTOS fdt
     , ( SELECT fm.documento ds_documento
               ,fm.parcela   cd_parcela
               ,Max(FM.data) dt_recebimento
               ,Sum(Nvl(fm.valor,0)) vl_recebido_liquido
               ,Sum(Nvl(fm.valortotal,0)) vl_recebido_bruto
               ,Sum(Nvl(fm.juros,0)) vl_juros_recebido
           FROM BENNERCORP.FN_MOVIMENTACOES FM
          WHERE 1 = 1
            AND fm.OPERACAO = 62   --- somente baixa
            AND FM.data BETWEEN TO_DATE('01/01/2023 00:00:00','dd/mm/yyyy hh24:mi:ss') AND TO_DATE('11/10/2024 00:00:00','dd/mm/yyyy hh24:mi:ss')
            GROUP BY fm.documento
                    ,fm.parcela
        ) rec

 WHERE 1 = 1
   AND FD.HANDLE  = FP.documento
   AND fd.empresa = fp.empresa
   AND fd.filial = fp.filial
   AND FD.HANDLE = DOC_ORIGEM.DOCUMENTOORIGEM
   AND FD.EMPRESA = E.HANDLE
   AND FD.FILIAL = F.HANDLE
   AND DOC_ORIGEM.HANDLE = CI.DOCUMENTO
   AND CI.PRODUTO = PP.HANDLE
   AND FD.PESSOA = C.HANDLE
   AND fd.handle = fdt.documento
   AND FD.TIPODEMOVIMENTO = 1
   AND FD.EHCONTASPAGAR = 'N'
   AND FD.ENTRADASAIDA = 'S'
   AND FD.OPERACAOCANCELAMENTO IS NULL
   AND FD.DATACANCELAMENTO IS NULL
   AND FD.EHPREVISAO = 'N'
   AND fd.handle = rec.ds_documento
   AND fp.handle = rec.cd_parcela
   AND fd.NUMEROPEDIDO = 'FQF/00024179/2024'
--   AND  FD.HANDLE = 5514245

GROUP BY FD.HANDLE
       , DOC_ORIGEM.HANDLE
       , FD.DOCUMENTODIGITADO
       , FD.NUMEROPEDIDO
       , E.HANDLE
       , E.NOME
       , FD.FILIAL
       , F.NOME
       , FD.NRNOTAFISCAL
       , To_Char(FD.DATAEMISSAO,'DD/MM/YY')
       , To_Char(FD.DATACANCELAMENTO,'DD/MM/YY')
       , To_Char(FP.datavencimento,'DD/MM/YY')
       , To_Char(FP.datainclusao,'DD/MM/YY')
       , To_Char(FP.dataliquidacao,'DD/MM/YY')
       , C.k_codigoportalfinanceiro
       , C.codigo
       , c.nome
       , To_Char(TRUNC(FD.DATAEMISSAO,'MM'),'DD/MM/YY')
       , PP.HANDLE
       , FP.HISTORICO
       , TRIM(REPLACE(REPLACE(PP.DESCRICAO,CHR(13),''),CHR(10),''))
       , fp.handle
       , FD.VALORESBAIXADOS
       , FD.ABATIMENTOS
       , FD.ACRESCIMOS
       , fd.valornominal
       , fd.valorliquido
       , FP.VALOR
       , FP.valoresbaixados
       , CI.VALORTOTAL
       , Nvl(fdt.aliquotaiss,0)
       , FD.TIPODOCUMENTO
       , FD.HISTORICO
       , FD.documentocontabil
       , FD.valoresbaixados
       , FD.abatimentos
       , FD.acrescimos
       , rec.dt_recebimento
       , rec.vl_recebido_liquido
       , rec.vl_recebido_bruto
       , rec.vl_juros_recebido
       , ci.handle
       )  recebido
  GROUP BY documento_id
      , doc_origem_id
      , doc_numero_pedido
      , documentonf
      , EMPRESA
      , codigo_cliente_portal_fin
      , codigo_cliente
      , FILIAL_ID
      , FILIAL
      , numero_nota
      , item_id
      , item
      , emissao
      , datacancelamento
      , datavencimento
      , datainclusao
      , dataliquidacao
      , codigo_cliente
      , nome_cliente
      , parcela_id
      , documentocontabil
      , valor_faturado_bruto
      , valor_faturado_liquido
      , valor_do_item
      , valor_parcela
      , aliquota_iss
      , dt_recebimento
      , vl_recebido_liquido
      , vl_recebido_bruto
      , vl_juros_recebido
      , ROWNUM
      , recebido.handle_item

order by documento_id
       , parcela_id