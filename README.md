# SX PHARMACY MANAGEMENT

### Sistema de Gestão de Farmácia

**Desenvolvido em Python | Tkinter | SQLite**

---

## 1. Descrição do Projecto

O **SX PHARMACY MANAGEMENT** é um sistema de gestão de farmácia desenvolvido em Python, com o objectivo de facilitar e melhorar o controlo das actividades diárias de uma farmácia.

O sistema permite gerir medicamentos, controlar o stock, registar compras e vendas, acompanhar datas de validade e consultar o histórico de operações.

A aplicação possui uma interface gráfica desenvolvida com Tkinter e utiliza SQLite para armazenar os dados localmente.

## 2. Elementos do Grupo

| Nº | Nome completo | GitHub |
|:---:|---|---|
| 1 | Shelton Xavier Mateulane | [@sheltonmateulane654-svg](https://github.com/sheltonmateulane654-svg) |
| 2 | Equisodio Salomão Muzonda | [@equisodiom-17](https://github.com/equisodiom-17) |
| 3 | Nesio Anibal Mahanzul | Não disponível |
| 4 | Edmilson Candido Valente | Não disponível |

## 3. Objectivos do Projecto

- Desenvolver uma aplicação de gestão de farmácia utilizando Python.
- Facilitar o registo e a consulta de medicamentos.
- Melhorar o controlo de entradas e saídas de stock.
- Automatizar o registo de compras e vendas.
- Acompanhar os preços e as datas de validade dos medicamentos.
- Gerar relatórios para facilitar a consulta das operações.

## 4. Funcionalidades

- **Painel principal:** apresenta indicadores gerais da farmácia.
- **Gestão de medicamentos:** permite cadastrar, editar, pesquisar e eliminar medicamentos.
- **Gestão de stock:** controla as quantidades disponíveis e os níveis mínimos.
- **Registo de compras:** regista a entrada de medicamentos e actualiza o stock.
- **Registo de vendas:** regista vendas e actualiza automaticamente as quantidades.
- **Controlo de validade:** acompanha medicamentos próximos do vencimento.
- **Alertas:** identifica produtos com stock baixo ou esgotado.
- **Histórico:** apresenta os movimentos de compras e vendas.
- **Recibos:** permite guardar comprovativos das vendas.
- **Exportação CSV:** permite exportar listas de medicamentos e históricos.

## 5. Tecnologias Utilizadas

| Tecnologia | Utilização |
|---|---|
| Python 3 | Linguagem de programação |
| Tkinter | Interface gráfica |
| SQLite | Gestão da base de dados |
| CSV | Exportação de relatórios |
| Visual Studio Code | Ambiente de desenvolvimento |
| Git | Controlo de versões |
| GitHub | Alojamento do projecto |

## 6. Estrutura do Projecto

```text
SX_PHARMACY_MANAGEMENT/
│
├── main.py
├── farmacia.db
├── README.md
└── .gitignore
```

## 7. Requisitos do Sistema

- Windows, Linux ou macOS.
- Python 3.10 ou superior.
- Visual Studio Code (recomendado).

Não é necessária a instalação de bibliotecas externas, pois o projecto utiliza módulos incluídos na biblioteca padrão do Python.

## 8. Como Executar o Projecto

**1. Clonar o repositório:**

```bash
git clone https://github.com/sheltonmateulane654-svg/SX_PHARMACY_MANAGEMENT.git
```

**2. Entrar na pasta do projecto:**

```bash
cd SX_PHARMACY_MANAGEMENT
```

**3. Executar a aplicação:**

```bash
python main.py
```

## 9. Base de Dados

O sistema utiliza SQLite para armazenar as informações da farmácia.

A base de dados contém tabelas destinadas a:

- Produtos e medicamentos.
- Compras e vendas.
- Movimentos de stock.
- Informações de preços e validade.

Os dados são armazenados localmente, permitindo que continuem disponíveis depois de fechar e abrir a aplicação.

## 10. Segurança e Limitações

- O sistema verifica a disponibilidade de stock antes de registar uma venda.
- Impede a venda de medicamentos com validade expirada.
- Identifica medicamentos que exigem receita.
- Os dados são armazenados numa base de dados local.
- Os preços apresentados são referências e devem ser confirmados junto dos fornecedores.
- A aplicação é um projecto académico e não substitui um sistema certificado nem a validação de um profissional farmacêutico.

## 11. Autor e Desenvolvimento

**Nome do Projecto:** SX PHARMACY MANAGEMENT

**Marca:** SX TECH & DESIGN

**Linguagem:** Python

**Área:** Informática e Sistemas de Gestão

**Finalidade:** Projecto académico

**Ano:** 2026

---

### SX TECH & DESIGN

*Tecnologia, inovação e soluções digitais.*

**© 2026 — Todos os direitos reservados.**
