import { useState } from 'react'
import './App.css'

function App() {
  // Estado para guardar os dados do formulário
  // Os nomes aqui devem ser IGUAIS aos que o Python espera
  const [formData, setFormData] = useState({
    Brand: '',
    Model: '',
    Year: 2020,
    Engine_Size: 1.5,
    Fuel_Type: 'Petrol',
    Transmission: 'Manual',
    Mileage: 50000,
    Doors: 4,
    Owner_Count: 1
  })

  const [resultado, setResultado] = useState(null)
  const [erro, setErro] = useState(null)
  const [loading, setLoading] = useState(false)

  // Atualiza o estado quando o usuário digita
  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  // Envia os dados para a API Python
  const handleSubmit = async (e) => {
    e.preventDefault()
    setErro(null)
    setResultado(null)
    setLoading(true)

    // Converter números (o HTML entrega como string, o Python quer int/float)
    const dadosParaEnviar = {
      ...formData,
      Year: Number(formData.Year),
      Engine_Size: Number(formData.Engine_Size),
      Mileage: Number(formData.Mileage),
      Doors: Number(formData.Doors),
      Owner_Count: Number(formData.Owner_Count)
    }

    try {
      // Faz a requisição para o seu Backend
      const response = await fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(dadosParaEnviar)
      })

      const data = await response.json()

      if (data.sucesso) {
        setResultado(data.preco_previsto)
      } else {
        setErro("Erro na previsão: " + (data.erro || "Desconhecido"))
      }
    } catch (error) {
      setErro("Erro de conexão. O servidor Python (app.py) está rodando?")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <header>
        <h1>🚗 Preditor de Preços</h1>
        <p>Sistema de Avaliação de Veículos com IA</p>
      </header>

      <div className="content-grid">
        <form onSubmit={handleSubmit} className="card form-card">
          <h2>Dados do Veículo</h2>
          
          <div className="input-group">
            <label>Marca</label>
            <input name="Brand" value={formData.Brand} onChange={handleChange} placeholder="Ex: Honda" required />
          </div>

          <div className="input-group">
            <label>Modelo</label>
            <input name="Model" value={formData.Model} onChange={handleChange} placeholder="Ex: Civic" required />
          </div>

          <div className="row">
            <div className="input-group">
              <label>Ano</label>
              <input type="number" name="Year" value={formData.Year} onChange={handleChange} required />
            </div>
            <div className="input-group">
              <label>Motor (L)</label>
              <input type="number" step="0.1" name="Engine_Size" value={formData.Engine_Size} onChange={handleChange} required />
            </div>
          </div>

          <div className="row">
            <div className="input-group">
              <label>Combustível</label>
              <select name="Fuel_Type" value={formData.Fuel_Type} onChange={handleChange}>
                <option value="Petrol">Gasolina (Petrol)</option>
                <option value="Diesel">Diesel</option>
                <option value="Hybrid">Híbrido</option>
                <option value="Electric">Elétrico</option>
              </select>
            </div>
            <div className="input-group">
              <label>Câmbio</label>
              <select name="Transmission" value={formData.Transmission} onChange={handleChange}>
                <option value="Manual">Manual</option>
                <option value="Automatic">Automático</option>
                <option value="Semi-Automatic">Semi-Automático</option>
              </select>
            </div>
          </div>

          <div className="input-group">
            <label>Quilometragem (Km)</label>
            <input type="number" name="Mileage" value={formData.Mileage} onChange={handleChange} required />
          </div>

          <button type="submit" disabled={loading} className="btn-submit">
            {loading ? 'Calculando...' : 'Calcular Preço'}
          </button>
        </form>

        <div className="card result-card">
          <h2>Resultado da Avaliação</h2>
          
          {resultado && (
            <div className="result-box success">
              <span>Valor Estimado:</span>
              <strong>$ {resultado}</strong>
            </div>
          )}

          {erro && (
            <div className="result-box error">
              <span>Erro:</span>
              <strong>{erro}</strong>
            </div>
          )}

          {!resultado && !erro && (
            <p className="placeholder-text">Preencha o formulário para ver a estimativa da IA.</p>
          )}
        </div>
      </div>
    </div>
  )
}

export default App