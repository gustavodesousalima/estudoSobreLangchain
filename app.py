import os
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory

os.environ["OPENAI_API_KEY"] = 'api_key'

llm = ChatOpenAI(model="gpt-4o-mini")

memoria = ConversationBufferMemory()

informacoes_usuario = {
    "nome": None,
    "email": None,
    "cpf": None
}

def filtrar_resposta(tipo, resposta_usuario):
    mensagem = [{
        "role": "user", 
        "content": f"Por favor, extraia apenas o {tipo} da seguinte resposta: '{resposta_usuario}'. responda somente a infromação solicitada e não diga nada além disso."
    }]
    resposta_filtrada = llm.invoke(mensagem)
    return resposta_filtrada.content.strip()

def fazer_pergunta(tipo):
    
    mensagem = [{
        "role": "user", 
        "content": f"Crie uma pergunta humanizada para coletar o {tipo}. Responda somente a pergunta que você gerar e não diga nada além disso."
    }]

    pergunta_ia = llm.invoke(mensagem)

    print(f"Chatbot: {pergunta_ia.content}")
    
    resposta_usuario = input("Você: ")
    
    resposta_filtrada = filtrar_resposta(tipo, resposta_usuario)
   
    informacoes_usuario[tipo] = resposta_filtrada
    
    memoria.save_context({"input": pergunta_ia.content}, {"output": resposta_usuario})

def iniciar_atendimento():
    tipos = ["nome", "email", "cpf"]
    
    for tipo in tipos:
        fazer_pergunta(tipo)
    
    print("\nMuito obrigado! Você pode perguntar o que quiser.\n")
    
    while True:
        pergunta_usuario = input("Você: ")

        if pergunta_usuario.lower() in ["sair", "exit"]:
            print("\nChatbot: Obrigado pelo atendimento! Até logo!\n")
            break
        
        if "nome" in pergunta_usuario.lower():
            resposta = f"Seu nome é {informacoes_usuario['nome']}."
        elif "email" in pergunta_usuario.lower():
            resposta = f"Seu e-mail é {informacoes_usuario['email']}."
        elif "cpf" in pergunta_usuario.lower():
            resposta = f"Seu CPF é {informacoes_usuario['cpf']}."
        else:
            mensagem_usuario = [{"role": "user", "content": pergunta_usuario}]
            resposta_ia = llm.invoke(mensagem_usuario)
            resposta = resposta_ia.content
        
        print(f"\nChatbot: {resposta}\n")

iniciar_atendimento()