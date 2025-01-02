import streamlit as st
import os
from dotenv import load_dotenv, find_dotenv

from openai import OpenAI

def enable_api_openai_api_key():
	_ = load_dotenv(find_dotenv())

	if not os.environ.get('OPENAI_API_KEY'):
		raise ValueError("Ensure your API key is set!")

def get_openai_models(client):
    models = client.models.list()
    return [model.id for model in models]

def create_chat(client, context, model_name): # por default generamos modelo con gpt-4o-mini
    
    completion = client.chat.completions.create(
		model=model_name,
		messages=[
			{"role": "system", "content": context},
		]
	)
    
    # retornamos un chat solo con el contexto
    return completion 

# habilitamos el API Key de OpenAI
enable_api_openai_api_key()

# creamos client de OpenAI para interactuar con la API
client = OpenAI()

st.title("✈️ SMARTito")
st.write('''
        ¡Hola! Soy SMARTito, tu asistente virtual especializado en datos de eCommerce de nuestra aerolínea.
        Estoy aquí para ayudarte a explorar y analizar las métricas de comportamiento de usuarios y transacciones 
        en nuestra plataforma. Aún estoy en construcción 👷🏻
     '''
)

models = get_openai_models(client)

option = st.selectbox(
    "Elige un modelo de OpenAI (default: gp4-4o-mini)",
    tuple(models),
    index=tuple(models).index('gpt-4o-mini'),
    placeholder="Selecciona un modelo de OpenAI",
)

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = option

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# reacciona al prompt del usuario
if prompt := st.chat_input("Escribe algo..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})