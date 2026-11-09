# IE350 · Hidrômetro digital com RSSF LoRa

Projeto da disciplina **IE350 – Redes de Comunicação Sem Fio para IoT** (FEEC/UNICAMP),
desenvolvido com a **Metodologia das Três Fases (TpM)** e a plataforma Smart TpM.

**Autor:** Lucas Chiomark Pereira Santos · RA 195111

## Objetivo

Avaliar a cobertura e a gerência de uma rede LoRa para medição individualizada de água
em um prédio residencial. O ambiente é perturbado de propósito com o **elevador em
movimento**, para medir o efeito em RSSI, SNR e taxa de sucesso de pacotes (PSR).

## Estrutura do repositório

| Pasta | Conteúdo |
|---|---|
| `framework_dlul/` | Framework de avaliação de cobertura DL/UL via MQTT, níveis N1 a N6 (usado nas medidas) |
| `teste_ul/` | Teste inicial só de uplink, usado para validar o hardware |
| `dados/brutos/` | Arquivos de cada rodada, sem edição, uma pasta por campanha |
| `dados/processados/` | Resumos calculados (`resumo_rodadas.csv`) |
| `analise/` | Scripts de análise (`resumo_rodadas.py`) |
| `gerencia/` | Ferramenta de gerência da rede (entrega de 30/11) |
| `docs/` | Guia do trabalho, roteiro dos ensaios e figuras |

## Framework DL/UL (avaliação de cobertura)

```
N6 tela LoRa Site Survey ─┐
N2/N3 Python (PC) ── MQTT (broker.hivemq.com) ── Gateway NodeMCU ── LoRa ── Nó NodeMCU
N5 processamento ─────────┘        │
                     3_N4_Armazenamento/Dados_Brutos (1 .txt por rodada)
```

A cada medida, o Python publica um pacote de descida (DL) no broker. O gateway o transmite
por LoRa, o nó responde (UL) com a RSSI e o SNR que mediu na descida, e o gateway
acrescenta a RSSI e o SNR da subida. Como o broker é público, o PC e o gateway só precisam
de internet, não precisam estar na mesma rede.

| Nível | Arquivo | Função |
|---|---|---|
| N1/N2 | `0_N1_N2_No_Sensor/no_sensor_dlul/` | Nó sensor: responde cada DL com RSSI/SNR medidos |
| N2 | `1_N2_Gateway/gateway_dlul/` | Gateway: ponte MQTT ↔ LoRa |
| N2/N3 | `2_N2_N3_Borda/N2_N3_LSS_MQTT.py` | Envia os DL, recebe os UL, grava a rodada |
| N4 | `3_N4_Armazenamento/` | Parâmetros, dados brutos e processados |
| N5 | `4_N5_Processamento/N5_Gerencia_SNR.py` | Calcula RSSI, SNR, PSR e taxa de canal |
| N6 | `5_N6_Exibicao/N6_Gerencia_SNR_Radio.py` | Tela: configura o rádio, dispara e mostra os resultados |

### Configuração usada

| Item | Valor |
|---|---|
| Rádio | 903 MHz · SF12 · BW 125 kHz · CR 4/8 · 20 dBm |
| Medidas por rodada | 100, com intervalo calculado pelo ToA (≈ 4 s em SF12) |
| Broker / porta | `broker.hivemq.com` / 1883, QoS 0 |
| Tópicos | `mot_lora_195111/gateway/downlink` e `mot_lora_195111/gateway/uplink` |

### Mapa dos 20 bytes do UL (o que o nó devolve)

| Byte | Conteúdo | Conversão |
|---|---|---|
| 0 | RSSI do DL (medida no nó) | `byte/2 − 74` dBm (byte > 128: subtrai 256 antes) |
| 1 | SNR do DL | `byte/4 − 30` dB |
| 2 | RSSI do UL (medida no gateway) | igual ao byte 0 |
| 3 | SNR do UL | igual ao byte 1 |

Pacote perdido: os 20 bytes do UL são gravados com o valor 9.

### Pinagem (NodeMCU ↔ RFM95)

| RFM95 | NodeMCU | GPIO |
|---|---|---|
| SCK / MISO / MOSI | D5 / D6 / D7 | 14 / 12 / 13 |
| NSS | D8 | 15 |
| RESET | D3 | 0 |
| DIO0 | D1 | 5 |
| LED vermelho / verde (nó) | D4 / D2 | 2 / 4 |

### Como rodar

1. Arduino IDE com o pacote **ESP8266** e as bibliotecas **LoRa** (Sandeep Mistry) e **MQTT** (Joel Gaehwiler).
2. No gateway, copiar `secrets_exemplo.h` para `secrets.h` e preencher a rede Wi-Fi 2.4 GHz do local.
3. Gravar `no_sensor_dlul` e `gateway_dlul` (placa *NodeMCU 1.0*). Os dois já vêm com `PKLORA_NODEMCU` selecionado.
4. No PC: `pip install paho-mqtt pandas matplotlib`.
5. Abrir dois terminais **dentro das pastas dos scripts** (os caminhos são relativos):
   `cd framework_dlul/2_N2_N3_Borda && python N2_N3_LSS_MQTT.py` e
   `cd framework_dlul/5_N6_Exibicao && python N6_Gerencia_SNR_Radio.py`.
6. Na tela N6, conferir a configuração e clicar em **INICIAR**. A rodada é gravada em
   `3_N4_Armazenamento/Dados_Brutos/`. Depois, copie o arquivo para `dados/brutos/`
   com o nome padrão.

## Medidas preliminares (01/10/2026)

Validação de ponta a ponta do framework com nó e gateway lado a lado, a **2,5 m** de
distância, no mesmo ambiente. Cinco rodadas de 100 pacotes, todas em SF12/BW125/CR4/8/20 dBm.
Arquivos em `dados/brutos/preliminares_2026-10-01/`.

| Rodada | PSR | RSSI UL (dBm) | σ UL | RSSI DL (dBm) | σ DL | SNR UL (dB) |
|---|---|---|---|---|---|---|
| P1 (13:27) | 100.0% | -36.1 | 5.45 | -34.6 | 5.23 | 10.29 |
| P2 (13:37) | 90.0% | -42.9 | 5.25 | -42.0 | 1.75 | 9.94 |
| P3 (13:54) | 100.0% | -34.8 | 1.80 | -33.1 | 1.50 | 10.18 |
| P4 (14:06) | 100.0% | -35.9 | 1.30 | -33.9 | 1.22 | 9.77 |
| P5 (14:15) | 100.0% | -35.5 | 0.96 | -33.7 | 0.76 | 9.94 |

Calculado com `python analise/resumo_rodadas.py`. Na rodada P2, 10 pacotes se perderam
com o enlace forte (RSSI ≈ −42 dBm), então a causa provável não é o rádio, e sim o
caminho Wi-Fi/MQTT. Isso será observado na campanha.

## Validação do sistema (09/11/2026)

Teste de ponta a ponta antes da campanha: nó e gateway na mesma mesa, gateway no Wi-Fi e
PC no broker público. 20 pacotes em SF12/BW125/CR4/8/20 dBm, intervalo de 4,06 s.

| Rodada | PSR | RSSI UL (dBm) | σ UL | RSSI DL (dBm) | σ DL | SNR UL (dB) |
|---|---|---|---|---|---|---|
| V1 (10:53) | 100% | −39.5 | 0.60 | −37.5 | 0.51 | 10.64 |

Arquivo em `dados/brutos/validacao_2026-11-09/`. Resultado: framework, gateway, nó e broker
funcionando, pronto para a campanha no prédio.

## Campanha de cobertura (prédio, com elevador)

![Cenários](docs/figuras/cenarios_teste.png)

| Rodada | Gateway | Nó | Elevador |
|---|---|---|---|
| A0 | Térreo | 2º andar, fixo | Parado (linha de base) |
| A1 | Térreo | 2º andar, fixo | Em movimento contínuo |
| B0 | Casa de máquinas | 2º andar, fixo | Parado (linha de base) |
| B1 | Casa de máquinas | 2º andar, fixo | Em movimento contínuo |
| C1 | Térreo | Dentro da cabine | Parada em cada andar |
| C2 | Térreo | Dentro da cabine | Em movimento contínuo |

Procedimento completo em `docs/IE350_Roteiro_Ensaios_Campo.pdf`. Nome dos arquivos:
`R_<rodada>_<posicaoGW>_<posicaoNo>_<condicao>_<AAAA-MM-DD>.txt`.

## Teste de uplink (UL)

Primeiro experimento, só de subida: o nó envia a luminosidade do LDR a cada segundo e o
gateway entrega o pacote e a RSSI ao PC pela USB (`teste_ul/UL_Test.py` mostra os
gráficos). Usa a mesma pinagem do framework e 903 MHz/SF7/17 dBm. Não grava arquivo.

## Créditos

O framework DL/UL ("MoT LoRa Site Survey", WissTek IoT: Branquinho, Felipe e Anderson) e
o teste UL (kit PK-LoRa V2, WissTek-IoT) são materiais distribuídos na disciplina. Os
créditos originais foram mantidos nos arquivos. Neste repositório: adaptação para NodeMCU,
tópicos e credenciais, organização, documentação, script de análise e a campanha de
medidas, por Lucas Chiomark Pereira Santos.

## Status

- [x] Fase 1 (negócio) e Fase 2 (requisitos) na Smart TpM
- [x] Fase 3: tecnologias e planilha de projeto
- [x] Teste de uplink (UL) com ESP8266
- [x] Framework de avaliação de cobertura DL/UL via MQTT + medidas preliminares
- [ ] Campanha de medidas no prédio (A0 a C2)
- [ ] Framework de gerência (30/11)
- [ ] Apresentação (07/12 ou 14/12)
