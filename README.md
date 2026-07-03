# 📊 Dashboard de Atendimento e Performance Operacional

## 📌 Sobre o projeto

Este projeto foi desenvolvido com o objetivo de consolidar dados provenientes de diferentes fontes, realizar o tratamento das informações utilizando Python e disponibilizar uma base única para construção de dashboards no Power BI.

O pipeline ETL realiza a leitura de arquivos em diferentes formatos (CSV, TXT e XLSX), padroniza a estrutura dos dados, calcula indicadores operacionais e gera uma base consolidada pronta para análise.

---

# Objetivos

- Consolidar dados de múltiplas fontes
- Padronizar informações
- Calcular indicadores operacionais
- Gerar uma base única para análise
- Construir um dashboard executivo no Power BI

---

# Tecnologias utilizadas

- Python
- Pandas
- OpenPyXL
- Git
- GitHub
- Power BI

---

# Estrutura do projeto

```
Case_Analise_Dados
│
├── data/
├── scripts/
│   └── consolidacao.py
│
├── output/
│   └── base_consolidada.csv
│
├── dashboard/
│
├── images/
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

# Pipeline ETL

O processo desenvolvido contempla as seguintes etapas:

- Leitura dos arquivos CSV, TXT e XLSX
- Padronização das colunas
- Conversão de datas e horários
- Consolidação das bases
- Tratamento de inconsistências
- Cálculo dos tempos de espera e atendimento
- Classificação dos atendimentos
- Exportação da base consolidada

---

# Indicadores calculados

- Total de atendimentos
- Total de abandonos
- Tempo médio de espera
- Tempo médio de atendimento
- Distribuição por loja
- Percentual de abandono

---

# Dashboard Power BI

O dashboard apresenta indicadores executivos para acompanhamento da operação, permitindo identificar oportunidades de melhoria por meio da análise dos principais KPIs de atendimento.

> 🚧 Em desenvolvimento.

---

# Como executar

Clone o repositório:

```bash
git clone https://github.com/sabbrinaa-cloud/dashboard-atendimento-performance.git
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute:

```bash
python scripts/consolidacao.py
```

A base consolidada será gerada automaticamente na pasta:

```
output/
```

---

# Próximas melhorias

- Dashboard executivo em Power BI
- Inclusão de imagens do dashboard
- Documentação das métricas
- Melhorias na visualização dos indicadores

---

# Autora

**Sabrina Sá**

Projeto desenvolvido para fins de estudo e demonstração de conhecimentos em Engenharia de Dados, ETL e Business Intelligence.
