# IE350 · Hidrômetro digital com RSSF LoRa

Projeto da disciplina **IE350 – Redes de Comunicação Sem Fio para IoT** (FEEC/UNICAMP),
desenvolvido com a **Metodologia das Três Fases (TpM)** e a plataforma Smart TpM.

**Autor:** Lucas Chiomark Pereira Santos · RA 195111

## Objetivo

Avaliar a cobertura e gerenciar uma rede de sensores sem fio LoRa para medição
individualizada de água em um prédio residencial. O ambiente é perturbado de propósito
com o **elevador em movimento**, para medir o impacto em RSSI, SNR e taxa de sucesso de
pacotes (PSR).

## Cenários de teste

![Cenários](docs/figuras/cenarios_teste.png)

| Rodada | Gateway          | Nó              | Elevador                    |
|--------|------------------|-----------------|-----------------------------|
| A0     | Térreo           | 2º andar, fixo  | Parado (linha de base)      |
| A1     | Térreo           | 2º andar, fixo  | Em movimento contínuo       |
| B0     | Casa de máquinas | 2º andar, fixo  | Parado (linha de base)      |
| B1     | Casa de máquinas | 2º andar, fixo  | Em movimento contínuo       |
| C1     | Térreo           | Dentro da cabine| Parada em cada andar        |
| C2     | Térreo           | Dentro da cabine| Em movimento contínuo       |

Configuração de rádio fixa em todas as rodadas: 915 MHz · BW 125 kHz · SF12 · CR 4/8 ·
20 dBm · 100 pacotes por rodada · intervalo de 8 s.

## Estrutura do repositório

Organizada pelos níveis do framework da TpM:

| Pasta                 | Nível | Conteúdo                                             |
|-----------------------|-------|------------------------------------------------------|
| `firmware/no_sensor/` | N1    | Firmware do nó de teste (ESP8266 + LoRa)             |
| `firmware/gateway/`   | N2/N3 | Firmware do rádio base / gateway LoRa–MQTT           |
| `borda/`              | N3    | Scripts Python de controle da campanha (MQTT)        |
| `dados/brutos/`       | N4    | Um arquivo por rodada, sem tratamento                |
| `dados/processados/`  | N4    | Resultados calculados por rodada                     |
| `analise/`            | N5    | Estatística (média, σ, PSR, margem) e gráficos       |
| `gerencia/`           | N6    | Ferramenta de gerência: estados, limiares e alarmes  |
| `docs/`               | —     | Guia, plantas, corte e fotos do ambiente             |

## Padrão de nome dos arquivos de dados

```
R_<rodada>_<posicaoGW>_<posicaoNo>_<condicao>_<AAAA-MM-DD>.txt
ex.: R_A1_GWterreo_No2and_mov_2026-11-17.txt
```

## Status

- [x] Fase 1 (negócio) e Fase 2 (requisitos) na Smart TpM
- [x] Fase 3: tecnologias e planilha de projeto
- [ ] Framework de avaliação de cobertura: códigos + medidas (09/11)
- [ ] Framework de gerência (30/11)
- [ ] Apresentação (07/12 ou 14/12)
