UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
dl() { curl -sS --compressed -m 90 -A "$UA" -o "$2" "$1" -w "%{http_code} %{size_download}\t$2\n"; }
B=https://www.planalto.gov.br/ccivil_03
dl $B/constituicao/constituicao.htm cf88.htm
dl $B/leis/l8112cons.htm l8112.htm
dl $B/decreto/d1171.htm d1171_etica.htm
dl $B/leis/l9784.htm l9784.htm
dl $B/decreto-lei/del2848compilado.htm cp.htm
dl $B/decreto-lei/del3689compilado.htm cpp.htm
dl $B/leis/l9455.htm l9455_tortura.htm
dl $B/_ato2004-2006/2006/lei/l11343.htm l11343_drogas.htm
dl $B/leis/2003/l10.826.htm l10826_armas.htm
dl $B/leis/l8072.htm l8072_hediondos.htm
dl $B/_ato2019-2022/2019/lei/L13869.htm l13869_abuso.htm
dl $B/_ato2007-2010/2009/lei/l12037.htm l12037_idcriminal.htm
dl $B/_ato2015-2018/2015/lei/l13103.htm l13103_motorista.htm
dl $B/leis/l8666cons.htm l8666.htm
dl $B/_ato2017-2020/2017/decreto/d9203.htm d9203_governanca.htm
dl $B/_ato2011-2014/2011/lei/l12527.htm l12527_lai.htm
dl $B/leis/l9654.htm l9654_prf.htm
dl $B/_ato2007-2010/2008/lei/l11784.htm l11784.htm
dl $B/_ato2007-2010/2009/decreto/d6949.htm d6949_pcd.htm
dl $B/decreto/1990-1994/anexo/and678-92.pdf pacto_sao_jose.pdf
dl $B/_ato2007-2010/2007/decreto/d6029.htm d6029_etica.htm
