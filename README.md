# Projeto 1: Análise de Performance de Marketing e Dashboard Interativo

Neste projeto, mergulhei nos dados de campanhas de marketing de um e-commerce para descobrir como otimizar o orçamento e aumentar a lucratividade. O resultado final é um dashboard interativo onde você pode explorar os insights que encontrei.

## 🚀 Explore o Dashboard Ao Vivo!

Você pode acessar e interagir com o dashboard final através deste link:
**https://dwngi5xu9ceprbjnkesbax.streamlit.app/**

![Screenshot do Dashboard](https://i.imgur.com/x8g06N5.png) 

---

## 1. O Desafio de Negócio

O ponto de partida foi um desafio clássico: uma empresa investia em múltiplos canais de marketing — Email, Mídias Sociais e Anúncios Pagos — mas não tinha uma visão clara de qual deles realmente trazia o melhor resultado financeiro. Meu objetivo foi usar os dados para responder à pergunta: "Onde devemos focar nosso investimento para ter o maior retorno?".

## 2. Minha Solução e Principais Descobertas

Para solucionar este problema, construí um processo de análise do zero, desde a geração e limpeza dos dados até a criação de um dashboard interativo. Através da análise, cheguei a algumas conclusões surpreendentes:

* **Eficiência Inesperada:** Descobri que **Mídias Sociais** era o canal com o menor Custo por Aquisição (CPA) de **R$4,88**, se mostrando a forma mais barata de trazer novos clientes.
* **O Paradoxo da Lucratividade:** O insight mais interessante foi que o **Email Marketing**, mesmo tendo um custo por aquisição mais alto, era de longe o canal mais lucrativo, com um ROI extraordinário de mais de **13.000%**, graças à sua altíssima taxa de conversão.
* **Oportunidade Estratégica:** A conclusão clara é que a empresa tem uma grande oportunidade de aumentar seu lucro ao realocar o orçamento, investindo mais nos canais que provaram ser mais eficientes e lucrativos.

## 3. Tecnologias que Utilizei
* **Linguagem:** Python
* **Análise de Dados:** Pandas, NumPy
* **Visualização de Dados:** Matplotlib, Seaborn, Plotly Express
* **Dashboard Interativo:** Streamlit
* **Versionamento:** Git e GitHub

## 4. Como Executar o Projeto Localmente
1.  Clone o repositório: `git clone https://github.com/JessicaRocha-dados/dashboard-analise-marketing.git`
2.  Navegue até a pasta do projeto: `cd dashboard-analise-marketing`
3.  Crie e ative um ambiente virtual:
    ```
    python -m venv venv
    .\venv\Scripts\activate
    ```
4.  Instale as dependências: `pip install -r requirements.txt`
5.  Gere o dataset consistente: `python src/01_generate_dataset.py`
6.  Execute o dashboard: `streamlit run dashboard.py`
