import streamlit as st

# Inicialização de dados
if "usuarios" not in st.session_state:
    st.session_state.usuarios = {}
if "feed" not in st.session_state:
    st.session_state.feed = []
if "usuario_logado" not in st.session_state:
    st.session_state.usuario_logado = None

# Funções
def criar_usuario():
    with st.form("Criar usuário"):
        nome = st.text_input("Nome completo")
        usuario = st.text_input("Nome de usuário (@)")
        idade = st.number_input("Idade", min_value=1, max_value=120, step=1)
        signo = st.selectbox("Signo", [
            "Áries", "Touro", "Gêmeos", "Câncer", "Leão", "Virgem",
            "Libra", "Escorpião", "Sagitário", "Capricórnio", "Aquário", "Peixes"
        ])
        bio = st.text_area("Bio")
        gostos = st.text_area("Gostos (separados por vírgula)")
        amigos = st.multiselect("Adicionar @ de amigos", list(st.session_state.usuarios.keys()))
        senha = st.text_input("Crie uma senha (mínimo 8 caracteres)", type="password")
        enviado = st.form_submit_button("Criar conta")

        if enviado:
            if len(senha) < 8:
                st.error("A senha deve ter no mínimo 8 caracteres.")
            elif usuario in st.session_state.usuarios:
                st.error("Esse nome de usuário já existe.")
            else:
                st.session_state.usuarios[usuario] = {
                    "nome": nome,
                    "idade": idade,
                    "signo": signo,
                    "bio": bio,
                    "gostos": [g.strip() for g in gostos.split(",") if g.strip()],
                    "amigos": amigos,
                    "mensagens": [],
                    "senha": senha
                }
                st.success(f"Usuário '{usuario}' criado com sucesso!")

def login():
    if not st.session_state.usuarios:
        st.info("Nenhum usuário cadastrado ainda.")
        return
    usuario = st.selectbox("Escolha seu usuário", list(st.session_state.usuarios.keys()))
    senha = st.text_input("Digite sua senha", type="password")
    if st.button("Entrar"):
        if st.session_state.usuarios[usuario]["senha"] == senha:
            st.session_state.usuario_logado = usuario
            st.success(f"Bem-vindo, {st.session_state.usuarios[usuario]['nome']}!")
        else:
            st.error("Senha incorreta.")

def ver_perfil():
    perfil = st.session_state.usuarios[st.session_state.usuario_logado]
    st.header("Perfil")
    st.write(f"**Nome:** {perfil['nome']}")
    st.write(f"**Idade:** {perfil['idade']}")
    st.write(f"**Signo:** {perfil['signo']}")
    st.write(f"**Bio:** {perfil['bio']}")
    st.write(f"**Gostos:** {', '.join(perfil['gostos']) if perfil['gostos'] else 'Nenhum'}")
    st.write(f"**Amigos:** {', '.join(perfil['amigos']) if perfil['amigos'] else 'Nenhum'}")

def postar():
    st.header("Nova Postagem")
    texto = st.text_area("Escreva sua postagem")
    imagem = st.file_uploader("Imagem (opcional)", type=["png", "jpg", "jpeg"])
    video = st.file_uploader("Vídeo (opcional)", type=["mp4", "mov"])
    link = st.text_input("Link externo (opcional)")
    modo_cf = st.checkbox("Postar apenas para amigos (CF)")

    if st.button("Publicar"):
        nome = st.session_state.usuarios[st.session_state.usuario_logado]["nome"]
        postagem = {
            "autor": nome,
            "usuario": st.session_state.usuario_logado,
            "texto": texto,
            "imagem": imagem,
            "video": video,
            "link": link,
            "cf": modo_cf
        }
        st.session_state.feed.append(postagem)
        st.success("Postagem publicada!")

def ver_feed():
    st.header("Feed Público e CF")
    if not st.session_state.feed:
        st.info("Nenhuma postagem ainda.")
    for i, post in reversed(list(enumerate(st.session_state.feed))):
        visivel = not post["cf"] or st.session_state.usuario_logado in st.session_state.usuarios[post["usuario"]]["amigos"] or post["usuario"] == st.session_state.usuario_logado
        if visivel:
            st.subheader(post["autor"])
            st.write(post["texto"])
            if post["imagem"]:
                st.image(post["imagem"])
            if post["video"]:
                st.video(post["video"])
            if post["link"]:
                st.markdown(f"[🔗 Link externo]({post['link']})")
            if post["usuario"] == st.session_state.usuario_logado:
                if st.button(f"🗑️ Apagar postagem {i}", key=f"del_post_{i}"):
                    st.session_state.feed.pop(i)
                    st.success("Postagem apagada.")
                    st.experimental_rerun()
            st.markdown("---")

def enviar_mensagem():
    st.header("Mensagem Privada")
    destino = st.selectbox("Enviar para", list(st.session_state.usuarios.keys()))
    texto = st.text_area("Mensagem")
    imagem = st.file_uploader("Imagem (opcional)", type=["png", "jpg", "jpeg"], key="msg_img")
    video = st.file_uploader("Vídeo (opcional)", type=["mp4", "mov"], key="msg_vid")
    link = st.text_input("Link externo (opcional)", key="msg_link")

    if st.button("Enviar mensagem"):
        nome = st.session_state.usuarios[st.session_state.usuario_logado]["nome"]
        mensagem = {
            "autor": nome,
            "texto": texto,
            "imagem": imagem,
            "video": video,
            "link": link
        }
        st.session_state.usuarios[destino]["mensagens"].append(mensagem)
        st.success("Mensagem enviada!")

def ver_mensagens():
    st.header("Mensagens Recebidas")
    msgs = st.session_state.usuarios[st.session_state.usuario_logado]["mensagens"]
    if not msgs:
        st.info("Nenhuma mensagem recebida.")
    for i, msg in reversed(list(enumerate(msgs))):
        st.subheader(msg["autor"])
        st.write(msg["texto"])
        if msg["imagem"]:
            st.image(msg["imagem"])
        if msg["video"]:
            st.video(msg["video"])
        if msg["link"]:
            st.markdown(f"[🔗 Link externo]({msg['link']})")
        if st.button(f"🗑️ Apagar mensagem {i}", key=f"del_msg_{i}"):
            msgs.pop(i)
            st.success("Mensagem apagada.")
            st.experimental_rerun()
        st.markdown("---")

def sair_da_conta():
    st.session_state.usuario_logado = None
    st.success("Você saiu da conta.")

def desativar_conta():
    usuario = st.session_state.usuario_logado
    if st.button("Confirmar desativação da conta"):
        del st.session_state.usuarios[usuario]
        st.session_state.usuario_logado = None
        st.warning("Sua conta foi desativada com sucesso.")

# Interface principal
st.title("🌐 Mini Rede Social Interativa")
st.markdown("Explore perfis, publique no feed, envie mensagens e conecte-se com amigos!")

menu = st.sidebar.radio("Menu", [
    "Criar Conta", "Login", "Perfil", "Postar", "Feed",
    "Mensagens", "Enviar Mensagem", "Sair da Conta", "Desativar Conta"
])

if menu == "Criar Conta":
    criar_usuario()
elif menu == "Login":
    login()
elif st.session_state.usuario_logado:
    if menu == "Perfil":
        ver_perfil()
    elif menu == "Postar":
        postar()
    elif menu == "Feed":
        ver_feed()
    elif menu == "Mensagens":
        ver_mensagens()
    elif menu == "Enviar Mensagem":
        enviar_mensagem()
    elif menu == "Sair da Conta":
        sair_da_conta()
    elif menu == "Desativar Conta":
        desativar_conta()
else:
    if menu not in ["Criar Conta", "Login"]:
        st.warning("Você precisa fazer login para acessar essa seção.")
