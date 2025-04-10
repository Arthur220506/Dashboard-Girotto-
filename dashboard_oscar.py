import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as pl

st.set_page_config(layout="wide")

df = pd.read_csv('the_oscar_award.csv') 

st.title("🏆 Dashboard de Premiações do Oscar")

st.sidebar.header("Filtros")

categorias = df['canon_category'].dropna().unique()
categoria_escolhida = st.sidebar.selectbox("🎭 Categoria", sorted(categorias))

ano_min = int(df['year_film'].min())
ano_max = int(df['year_film'].max())
anos = st.sidebar.slider("📅 Ano do Filme", ano_min, ano_max, (ano_min, ano_max))

df_filtrado = df[
    (df['canon_category'] == categoria_escolhida) &
    (df['year_film'] >= anos[0]) & (df['year_film'] <= anos[1])
]

st.subheader(f"🎬 Dados da categoria '{categoria_escolhida}' entre {anos[0]} e {anos[1]}")
st.dataframe(df_filtrado[['year_film', 'name', 'film', 'winner']])

st.subheader("📈 Número de indicações por ano")
indicacoes_por_ano = df_filtrado['year_film'].value_counts().sort_index()

fig, ax = plt.subplots()
sns.lineplot(x=indicacoes_por_ano.index, y=indicacoes_por_ano.values, ax=ax)
ax.set_xlabel("Ano do Filme")
ax.set_ylabel("Número de Indicações")
st.pyplot(fig)

st.subheader("🥇 Proporção de Vencedores vs. Indicados")
contagem_vencedores = df_filtrado['winner'].value_counts()
labels = ['Indicado', 'Vencedor']
fig2, ax2 = plt.subplots()
ax2.pie(contagem_vencedores, labels=labels, autopct='%1.1f%%', startangle=90)
ax2.axis('equal')
st.pyplot(fig2)

st.subheader("👤 Top 10 mais indicados")
top_indicados = df_filtrado['name'].value_counts().head(10)
fig3, ax3 = plt.subplots()
sns.barplot(x=top_indicados.values, y=top_indicados.index, ax=ax3)
ax3.set_xlabel("Número de Indicações")
ax3.set_ylabel("Nome")
st.pyplot(fig3)

st.subheader("🏆 Apenas os vencedores")
vencedores = df_filtrado[df_filtrado['winner'] == True]
st.dataframe(vencedores[['year_film', 'name', 'film']])

csv = df_filtrado.to_csv(index=False).encode('utf-8')
st.download_button("⬇️ Baixar dados filtrados (CSV)", data=csv, file_name="oscar_filtrado.csv", mime='text/csv')

