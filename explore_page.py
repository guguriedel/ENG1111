#Pagina explore

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

#Para fazer uma pagina que contenha todos os dados vamos precisar limpar o df do mesmo
#jeito que fizemos no cod, por isso importamos as funções q usamos

def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map


def clean_experience(x):
    if x ==  'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)


def clean_education(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x or 'Other doctoral' in x:
        return 'Post grad'
    return 'Less than a Bachelors'


@st.cache #Isso eh uma dica do st - Guardamos essa info no cache do site para diminuir processamento
def load_data(): #Aplicando TODAS as transformacoes feitas no df
    df = pd.read_csv("survey_results_public.csv")
    df = df[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedComp"]]
    df = df[df["ConvertedComp"].notnull()]
    df = df.dropna()
    df = df[df["Employment"] == "Employed full-time"]
    df = df.drop("Employment", axis=1)

    country_map = shorten_categories(df.Country.value_counts(), 400)
    df["Country"] = df["Country"].map(country_map)
    df = df[df["ConvertedComp"] <= 250000]
    df = df[df["ConvertedComp"] >= 10000]
    df = df[df["Country"] != "Other"]

    df["YearsCodePro"] = df["YearsCodePro"].apply(clean_experience)
    df["EdLevel"] = df["EdLevel"].apply(clean_education)
    df = df.rename({"ConvertedComp": "Salary"}, axis=1)
    return df

df = load_data()

#Agr sim começamos o que vamos exibir
def show_explore_page():
    st.title("Explore Salarios de Engenheiros de Software")

    st.write(
        """
    ### Dados do Stack Overflow 2022
    """
    )

    data = df["Country"].value_counts()

    fig1, ax1 = plt.subplots() #Plotando grafico de pizza
    ax1.pie(data, labels=data.index, autopct="%1.1f%%", shadow=True, startangle=90)
    ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.

    st.write("""#### Quantidade de dados por pais""")

    st.pyplot(fig1)
    
    st.write(
        """
    #### Média do Salário por pais
    """
    )

    data = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(data) #Grafico de Barras (mais bonitinho que o plt)

    st.write(
        """
    #### Média do Salário baseado em Experiência
    """
    )

    data = df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(data)