# 🚗 Preditor de Preços de Veículos | Projeto de Machine Learning

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![React](https://img.shields.io/badge/Frontend-React-61DAFB)
![Flask](https://img.shields.io/badge/Backend-Flask-black)
![Status](https://img.shields.io/badge/Status-Concluído-success)

> **Autor:** Guilherme Assis - Desenvolvedor Full Stack Júnior  
> **Versão:** 1.0.0

---

## 📑 Índice
1. [Visão Geral](#1-visão-geral)
2. [Tecnologias Utilizadas](#2-tecnologias-utilizadas)
3. [Dataset](#3-dataset)
4. [Arquitetura do Projeto](#4-arquitetura-do-projeto)
5. [Instalação e Execução](#5-instalação-e-execução)
6. [Documentação da API](#6-documentação-da-api)
7. [Estrutura de Arquivos](#7-estrutura-de-arquivos)

---

## 1. Visão Geral
Este projeto é uma aplicação **Full Stack de Inteligência Artificial** capaz de estimar o preço de venda de veículos usados com base em suas características técnicas. 

O sistema demonstra um pipeline completo de Machine Learning, desde a ingestão de dados e treinamento de um modelo de **Regressão Linear**, até o deploy via API REST e consumo por uma interface web moderna.

---

## 2. Tecnologias Utilizadas

### 🧠 Backend (Python)
* **Python 3.x**: Linguagem base.
* **Pandas**: Manipulação e limpeza de dados.
* **Scikit-Learn**: Treinamento do modelo, separação treino/teste e Label Encoding.
* **Joblib**: Persistência do modelo (salvamento em `.pkl`).
* **Flask**: Servidor da API.
* **Flask-CORS**: Permissão de acesso para o Frontend.

### 💻 Frontend (JavaScript)
* **React.js**: Biblioteca de interface.
* **Vite**: Ferramenta de build rápida.
* **CSS3**: Estilização responsiva.

---

## 3. Dataset
O modelo foi treinado com **10.000 registros** de dados históricos de veículos.

* **Fonte:** Kaggle Car Price Dataset
* **Variáveis (Features):** `Marca`, `Modelo`, `Ano`, `Motor`, `Combustível`, `Câmbio`, `Quilometragem`, `Portas`, `Donos`.
* **Alvo (Target):** `Preço`.

---

## 4. Arquitetura do Projeto

### Fluxo de Treinamento
1.  **ETL:** Carregamento e limpeza do CSV.
2.  **Encoding:** Conversão de texto (ex: "Honda") para números.
3.  **Split:** Separação 80% Treino / 20% Teste.
4.  **Treino:** Regressão Linear Múltipla.
5.  **Export:** Geração dos arquivos `modelo_carros.pkl` e `encoders.pkl`.

### Fluxo da Aplicação
1.  **Frontend:** Usuário envia dados via formulário.
2.  **API:** Recebe JSON, converte textos usando os encoders salvos e processa.
3.  **Modelo:** Calcula o preço estimado.
4.  **Retorno:** O valor é exibido na tela do usuário.

---

## 5. Instalação e Execução

### Pré-requisitos
* Python 3.8+
* Node.js e NPM

---

### Passo 1: Backend (API)

**1. Instale as bibliotecas Python**
pip install pandas scikit-learn flask flask-cors joblib

**2. (Opcional) Treine o modelo novamente**
python treinar_modelo.py

**3. Inicie o servidor**
python app.py
O servidor rodará em: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

### Passo 2: Frontend (Interface)

**1. Entre na pasta do frontend**
cd frontend-carros

**2. Instale as dependências**
npm install

**3. Rode o projeto**
npm run dev

**Acesse o link local: http://localhost:5173**

---

### Documentação da API
**POST /predict**
Recebe as características do veículo e retorna o preço estimado.

**Exemplo de Request (JSON):**

{
    "Brand": "Toyota",
    "Model": "Corolla",
    "Year": 2021,
    "Engine_Size": 2.0,
    "Fuel_Type": "Petrol",
    "Transmission": "Automatic",
    "Mileage": 25000,
    "Doors": 4,
    "Owner_Count": 1
}

**Exemplo de Response (200 OK):**

JSON

{
    "sucesso": true,
    "preco_previsto": "23500.00",
    "mensagem": "Cálculo realizado com sucesso!"
}

**Estrutura de Arquivos**
Plaintext

/projeto-ml-carros
│
├── app.py                  # API Flask
├── treinar_modelo.py       # Script de Treinamento
├── car_price_dataset.csv   # Dados brutos
├── modelo_carros.pkl       # Modelo salvo
├── encoders.pkl            # Decodificadores salvos
│
└── frontend-carros/        # Interface React
    ├── src/
    │   ├── App.jsx         # Lógica do Frontend
    │   └── App.css         # Estilos
    └── package.json
