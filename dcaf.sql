SELECT slo.cd_oportunidade oportunidade_id 
      ,slo.cd_codigo codigo_oportunidade
      ,slio.ds_contrato_benner
      ,slo.tp_status
      ,slo.nm_vertical
      ,slo.nm_regional
      ,slo.dt_criacao
      ,slo.dt_fechamento
      ,slo.dt_estim_fechamento
      ,slo.ds_porte
      ,slo.ds_tipo                                  
      ,slo.nm_razao_social
      ,slo.nr_cnpj
      ,slo.nm_dono
      ,slo.nm_sponsor
      ,slo.nm_parceiro                                             
      ,slo.ds_classificacao
      ,slio.cd_item_oportunidade
      ,slio.ds_item
      ,slio.nm_vertical_item
      ,slio.nr_quantidade
      ,slio.nr_preco_unitario
      ,slio.nr_preco_total
      ,slio.nr_desconto
      ,slio.nr_preco_total_desconto
      ,slio.dt_modificacao_item
      ,slio.dt_insert
      ,slio.tp_venda  
      ,slio.tp_servico
      ,slio.ds_primeira_parcela 
      ,slio.nr_quantidade
  FROM mvgestor.sl_oportunidades slo
      ,mvgestor.sl_itens_oportunidades slio
WHERE slo.cd_oportunidade = slio.cd_oportunidade
  AND InStr(Lower(tp_status),'ganha') > 0
  AND slio.ds_contrato_benner is not null
--  AND slo.cd_oportunidade = '0065f00000NI2JvAAL'
  AND slio.ds_contrato_benner = 'FQF/00024179/2024'
--   AND slo.dt_fechamento BETWEEN TO_DATE({{data_inicial}},'dd/mm/yyyy hh24:mi:ss') 
--   AND TO_DATE({{data_final}},'dd/mm/yyyy hh24:mi:ss')
  AND slo.dt_fechamento BETWEEN TO_DATE('01/01/2024 00:00:00','dd/mm/yyyy hh24:mi:ss') 
  AND TO_DATE('01/06/2024 23:59:59','dd/mm/yyyy hh24:mi:ss')
  AND nm_empresa NOT IN ('TESTE - 9PLAY')
  AND UPPER(slo.nm_vertical) LIKE '%' || upper('conect')||'%'
  ORDER BY slo.cd_oportunidade