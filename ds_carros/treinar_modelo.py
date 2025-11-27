import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, r2_score

# 1. Carregar os dados
print("Carregando dados...")
df = pd.read_csv('car_price_dataset.csv')

# 2. Pré-processamento (Converter texto em números)
# Precisamos guardar esses "dicionários" (encoders) para usar na API depois.
# Ex: Se a API receber "Honda", ela precisa saber qual número representa Honda.
encoders = {}
colunas_categoricas = ['Brand', 'Model', 'Fuel_Type', 'Transmission']

for col in colunas_categoricas:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le # Salvamos o codificador dessa coluna

# 3. Definir X (Entradas) e y (Saída/Alvo)
X = df.drop('Price', axis=1) # Tudo menos o preço
y = df['Price']              # Apenas o preço

# 4. Separar Treino e Teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. Treinar o Modelo (Regressão Linear)
print("Treinando modelo...")
modelo = LinearRegression()
modelo.fit(X_train, y_train)

# 6. Avaliar o Modelo
previsoes = modelo.predict(X_test)
score = r2_score(y_test, previsoes)
erro_medio = mean_absolute_error(y_test, previsoes)

print(f"--- Resultado do Treinamento ---")
print(f"Acurácia (R²): {score:.2f} (Quanto mais perto de 1.0, melhor)")
print(f"Erro Médio: ${erro_medio:.2f}")

# 7. Salvar tudo para usar na API Flask
arquivo_modelo = 'modelo_carros.pkl'
arquivo_encoders = 'encoders.pkl'

joblib.dump(modelo, arquivo_modelo)
joblib.dump(encoders, arquivo_encoders)
print(f"\nArquivos salvos: {arquivo_modelo} e {arquivo_encoders}")

# --- BÔNUS: Gerar resposta para o Teste Cego ---
# Vamos pegar seu arquivo de teste, aplicar as mesmas transformações e prever o preço.
print("\nGerando previsões para o arquivo de teste cego...")
df_teste = pd.read_csv('car_price_dataset_teste.csv')
df_teste_processado = df_teste.copy()

try:
    for col in colunas_categoricas:
        # Usamos o mesmo encoder do treino. 
        # Cuidado: se houver uma marca no teste que não existia no treino, isso daria erro.
        # Aqui assumimos que os dados são consistentes.
        le = encoders[col]
        df_teste_processado[col] = le.transform(df_teste_processado[col])

    previsoes_teste = modelo.predict(df_teste_processado)
    
    # Adicionar o preço previsto no dataframe original para visualização
    df_teste['Preco_Previsto'] = previsoes_teste
    df_teste.to_csv('resultado_teste_cego.csv', index=False)
    print("Arquivo 'resultado_teste_cego.csv' gerado com sucesso!")

except Exception as e:
    print(f"Aviso: Algum valor do teste não existia no treino. Detalhe: {e}")