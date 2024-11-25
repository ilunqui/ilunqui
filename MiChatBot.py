#Clase 6 ------------------------------------------------------------------------------------

import streamlit as st
from groq import Groq


st.set_page_config(page_title="Mi chat de IA", page_icon="🫐", layout="centered")

st.title("Que tengas un lindo dia <3")

nombre = st.text_input("Ingrese su nombre")

if st.button("Saludar"):
    st.write(f"¡Hola, {nombre}! que bueno verte de nuevo por aqui", divider="rainbow", anchor=False)

MODELOS = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768'] #Clase 7

# st.title("Que tengas un lindo dia <3")

def configurar_pagina():
# Agregamos un título principal a nuestra página
    st.title("¿Quieres hablar?")
    st.sidebar.title("Configuración de la IA") # Creamos un sidebar con un título.
    elegirModelo =  st.sidebar.selectbox('Elegí un modelo', options=MODELOS, index=0)
    return elegirModelo

# Clase 7 ------------------------------------------------------------------------------------

def crear_usuario_groq():
    clave_secreta = st.secrets["Clave_api"]
    return Groq(api_key=clave_secreta)


def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    return cliente.chat.completions.create(
    model=modelo,
    messages=[{"role": "user", "content": mensajeDeEntrada}],
    stream=True
    )

clienteUsuario = crear_usuario_groq()

def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

# Clase 8 -------------------------------------------------- funciona

def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role": rol, "content": contenido, "avatar":avatar})

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]):
            st.markdown(mensaje["content"])


def area_chat():
# Generamos un container que va a guardar el historial del chat
    contenedorDelChat = st.container(height=400,border=True)
# Abrimos el contenedor del chat y mostramos el historial.
    with contenedorDelChat:
        mostrar_historial()

# Clase 9 y 10 --------------------------------------------------------------------------------------------------------------

#"Rellena la cadena de caracteres"
def generar_respuesta(chat_completo):
      respuesta_completa = ""
      for frase in chat_completo:
          if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
      return respuesta_completa

def main():
    modelo = configurar_pagina()
    clienteUsuario = crear_usuario_groq()
    inicializar_estado()

    mensaje = st.chat_input("Escribí tu mensaje:")
    
    area_chat()
   
    if mensaje:
        actualizar_historial("user", mensaje, "🧑‍💻")
        chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje)

        if chat_completo:
            with st.chat_message("assistant"):
                respuesta_completa = st.write_stream(generar_respuesta(chat_completo))
                actualizar_historial("assistant", respuesta_completa,"🤖")
        st.rerun()

if __name__ == "__main__":
    main()