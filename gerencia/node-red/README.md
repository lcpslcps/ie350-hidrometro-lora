# Painel Node-RED do enlace LoRa

Tela web que mostra, em tempo real, os pacotes que passam pelo broker durante uma rodada:
RSSI e SNR nos dois sentidos, PSR, margem do enlace, σ da RSSI, gráficos por medida e
os últimos pacotes. Usa só nós nativos do Node-RED, sem paleta extra.

![Painel](../../docs/figuras/painel_nodered.png)

*Imagem: reprodução dos 20 pacotes da rodada de validação V1 (09/11).*

## Como usar

1. No Node-RED: menu ☰ → **Importar** → selecionar `painel_lora_nodered.json` → **Importar** → **Deploy**.
2. Abrir **http://localhost:1880/lora** no navegador.
3. Digitar o nome do teste (ex.: `A1_GWterreo_No2and_mov`) e clicar em **Novo teste**.
4. Rodar o framework normalmente (N2/N3 + N6 → INICIAR). A tela acompanha ao vivo.
5. Ao terminar, aparece "Teste finalizado" e o botão **Exportar CSV** fica verde. O arquivo
   baixa como `<nome>_<AAAA-MM-DD_HH-MM>.csv`.
6. **Importar** abre depois, em modo revisão, um CSV exportado ou o `.txt` bruto do framework
   (`3_N4_Armazenamento/Dados_Brutos`).

O teste em andamento fica salvo no navegador: atualizar a página (F5) não apaga os dados.
O dado oficial de cada rodada continua sendo o `.txt` do framework; o CSV é uma cópia
prática para a análise.

### Colunas do CSV

`teste, data_hora (hora local), medida, total, rssi_ul, snr_ul, rssi_dl, snr_dl, psr, margem, sf, bw, cr, pot`

O PC com o Node-RED só precisa de internet: ele assina os mesmos tópicos do broker público
(`mot_lora_195111/gateway/uplink` e `.../downlink`), sem interferir no framework.

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `painel_lora_nodered.json` | Flow para importar (já contém tudo abaixo) |
| `fn_dl.js` / `fn_ul.js` | Código das functions que decodificam os 20 bytes |
| `painel.html` | Página da tela (Chart.js via CDN) |

PSR na tela = respostas UL válidas ÷ pacotes DL enviados desde a medida 1 da rodada.
Margem = menor RSSI (UL ou DL) − sensibilidade do SX1276 em SF12/BW125 (−137 dBm).
