select distinct ctc.nome                                  as receita_master,
                fc.estrutura,
                fd.nrnotafiscal                           nf,
                fd.documentodigitado,
                fd.dataemissao,
                fd.numeropedido                           contrato,
                cast(c.objetocontrato as varchar(600))    as objeto_contrato,
                fd.handle                                 documento,
                fd.documentocontabil,
                p.nome                                    item,
                p.handle,
                ci.handle                                 as handle_item,
                ci.valortotal,
                case
                  when instr(p.nome, '(ISS RETIDO)', -1) > 0 then
                  ci.valortotal - ( ci.irfvalor + ci.valorinss +
                                    ci.valorpisretido
                                    + ci.valorcsll + ci.valorcofinsretido
                                    + ci.valorirpj + ci.issvalor )
                  else ci.valortotal - ( ci.irfvalor + ci.valorinss +
                                         ci.valorpisretido
                                         + ci.valorcsll + ci.valorcofinsretido
                                         + ci.valorirpj )
                end                                       as valor_liquido,
                ci.issvalor                               as iss,
                ( ( case
                      when instr(p.nome, '(ISS RETIDO)', -1) > 0 then
                      ci.valortotal - ( ci.irfvalor + ci.valorinss +
                                        ci.valorpisretido
                                        + ci.valorcsll + ci.valorcofinsretido
                                        + ci.valorirpj + ci.issvalor )
                      else ci.valortotal - (
                           ci.irfvalor + ci.valorinss +
                           ci.valorpisretido
                           + ci.valorcsll + ci.valorcofinsretido
                           + ci.valorirpj )
                    end ) - ci.issvalor )                 as base_valor_provisao
                ,
                to_char(sysdate, 'dd/mm/yyyy hh24:mi:ss') as
                data_atualizacao
from   bennercorp.fn_lancamentos fl
       left outer join bennercorp.fn_lancamentocc lc
                    on ( lc.lancamento = fl.handle )
       left join bennercorp.fn_contas fc
              on ( fc.handle = fl.conta )
       left join bennercorp.fn_documentos fd
              on ( fd.handle = fl.documento )
       left join bennercorp.gn_pessoas gp
              on ( gp.handle = fd.pessoa )
       left join bennercorp.cn_contratos c
              on ( c.numero = fd.numeropedido )
       left join bennercorp.cn_contratos c2
              on ( c.numero = fd.numeropedido
                   and fd.tipodemovimento = 1 ) --xxx
       left join bennercorp.cm_itens ci
              on ( ci.documento = fd.handle )
       left join bennercorp.pd_produtos p
              on ( p.handle = ci.produto )
       inner join bennercorp.pd_produtospai pai
               on ( p.produtopai = pai.handle )
       left join bennercorp.ct_contas ctc
              on ( pai.contacontabilvenda = ctc.handle )
       left join bennercorp.gn_operacoes op
              on ( op.handle = fd.operacao )
       left join bennercorp.fn_tiposdocumentos td
              on ( td.handle = fd.tipodocumento )
       left join (select co.contrato,
                         co.produto,
                         listagg(co.nomecodigo, '; ')
                         within group (order by co.contrato, co.produto) as
                 oportunidade_item
                  from   (select distinct co.contrato,
                                          co.produto,
                                          opor.nomecodigo
                          from   bennercorp.cn_contratoobjetos co
                          inner join bennercorp.k_codigooportunidade opor
                                         on ( co.k_codigooportunidade = opor.handle))
                         co
                  group  by co.contrato,
                            co.produto) opor
              on (opor.contrato = c.handle
                  and opor.produto = p.handle )
WHERE  GP.ehcliente = upper('s')
       and ci.contafinanceira = fc.handle
       and gp.codigo not in ( 873163 )
       and fd.tipodocumento not in ( 57 )
       and fd.datacancelamento is null
       and fd.nrnotafiscal is not null
       and decode(fc.estrutura, '1.03.21', 'A',
                                '1.06.01', 'A',
                                '1.11.06', 'A',
                                '1.11.09', 'A',
                                '1.11.18', 'A',
                                '1.19.04', 'A',
                                '2.02.20', 'A',
                                '2.02.23', 'A',
                                '2.02.30', 'A',
                                '2.02.35', 'A',
                                '2.02.45', 'A',
                                '2.03.31', 'A',
                                '2.04.11', 'A',
                                '2.04.13', 'A',
                                '2.04.30', 'A',
                                '2.06.02', 'A',
                                '2.06.05', 'A',
                                '2.06.14', 'A',
                                '2.06.16', 'A',
                                '2.06.45', 'A',
                                '2.06.51', 'A',
                                '2.07.02', 'A',
                                '2.07.07', 'A',
                                '2.07.12', 'A',
                                '2.08.12', 'A',
                                '2.08.13', 'A',
                                '2.08.14', 'A',
                                '2.08.15', 'A',
                                '2.08.16', 'A',
                                '2.08.17', 'A',
                                '2.09.04', 'A',
                                '2.09.05', 'A',
                                '2.09.13', 'A',
                                '2.09.20', 'A') is null
       and fd.numeropedido = upper('{{nr_pedido_fq}}')
       and ctc.nome = upper('{{receita_master}}')
