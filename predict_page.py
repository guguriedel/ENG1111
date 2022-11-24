import streamlit as st
import pickle
import numpy as np


def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data
#Função para ler o arquivo no qual gravamos os dados

data = load_model()

regressor = data["model"]
le_country = data["le_country"]
le_education = data["le_education"]
#Pegamos os modelos de dado

def show_predict_page(): #Purpurina pro site
    st.title("Previsão do Salário de um Desenvolvedor")

    st.write("""### Precisaremos de algumas informações""")

    countries = (
        "United States",
        "India",
        "United Kingdom",
        "Germany",
        "Canada",
        "Brazil",
        "France",
        "Spain",
        "Australia",
        "Netherlands",
        "Poland",
        "Italy",
        "Russian Federation",
        "Sweden",
    )

    education = (
        "Sou um estudante",
        "Bacharelado",
        "Mestrado",
        "Pós Doc",
    )

    country = st.selectbox("Pais", countries) #As caixas que selecionam
    education = st.selectbox("Nivel Educaional", education)

    if education == "Sou um estudante":
        education = 'Less than a Bachelors'
    elif education == "Bacharelado":
        education = "Bachelor’s degree"
    elif education == "Mestrado":
        education = "Master’s degree"
    else:
        education = "Post grad"

    expericence = st.slider("Experiência", 0, 50, 3)
    #Aqui fica a barra de deslizar do site


    if st.button("Calcular Salário"):
        X = np.array([[country, education, expericence ]]) #Cria a array (q nem no teste que fizemos no programa)
        X[:, 0] = le_country.transform(X[:,0])
        X[:, 1] = le_education.transform(X[:,1])
        X = X.astype(float) #Transforma tudo em numero

        salary = regressor.predict(X) #Calcula a previsão
        salary_month = salary[0] / 12 #Lembrando q o x eh uma array do np
        st.subheader(f"O Seu salario anual estimado é de US${salary[0]:.2f}")
        st.write(f"""#### (US${salary_month:.2f} por mês)""")
       # st.subheader(f"""#### (US${salary_month:.2f} por mês)""")

        #Oi joao, tem algumas coisas q eu queria resolver nesse codigo ainda se possivel
        #Primeiro, teria como eu traduzir o nome dos paises quando eles aparecem na barra?
        #Tem como eu ajustar o cambio da moeda me baseando na moeda a qual o pais escolhido usa?
        #Tipo, se eu escolher brasil o programa pega um cambio e ja coloca o valor em reais
        #N sei se seria um cambio arbitrario médio ou se daria pra ele atualizar o cambio toda vez q roda...