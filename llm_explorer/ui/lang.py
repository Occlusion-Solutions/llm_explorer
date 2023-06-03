from dataclasses import dataclass
from typing import List  # NOQA: UP035

AI_ROLE_OPTIONS_EN = [
    "helpful assistant",
    "code assistant",
    "code reviewer",
    "text improver",
    "cinema expert",
    "sport expert",
    "online games expert",
    "food recipes expert",
    "English grammar expert",
    "friendly and helpful teaching assistant",
    "laconic assistant",
    "helpful, pattern-following assistant",
    "translate corporate jargon into plain English",
]


AI_ROLE_OPTIONS_ES = [
    "asistente útil",
    "asistente de código",
    "revisor de código",
    "mejorador de texto",
    "experto en cine",
    "experto en deportes",
    "experto en juegos en línea",
    "experto en recetas de cocina",
    "experto en gramática inglesa",
    "asistente de enseñanza amable y servicial",
    "asistente lacónico",
    "asistente útil y siguiendo patrones",
    "traductor de jerga corporativa a español claro",
]


REPO_URL: str = "https://github.com/Occlusion-Solutions/occlussion_llm_explorer.git"
README_URL: str = f"{REPO_URL}#readme"
BUG_REPORT_URL: str = f"{REPO_URL}/issues"
LLM_EXPLORER_URL: str = "https://llm_explorer.streamlit.app/"


@dataclass
class Locale:
    ai_role_options: List[str]
    ai_role_prefix: str
    ai_role_postfix: str
    title: str
    language: str
    lang_code: str
    donates: str
    donates1: str
    donates2: str
    chat_placeholder: str
    chat_run_btn: str
    chat_clear_btn: str
    chat_save_btn: str
    speak_btn: str
    input_kind: str
    input_kind_1: str
    input_kind_2: str
    select_placeholder1: str
    select_placeholder2: str
    select_placeholder3: str
    radio_placeholder: str
    radio_text1: str
    radio_text2: str
    stt_placeholder: str
    footer_title: str
    footer_option0: str
    footer_option1: str
    footer_option2: str
    footer_chat: str
    footer_channel: str
    responsibility_denial: str
    donates_info: str
    tokens_count: str
    message_cost: str
    total_cost: str
    empty_api_handler: str


# --- LOCALE SETTINGS ---
en = Locale(
    ai_role_options=AI_ROLE_OPTIONS_EN,
    ai_role_prefix="You are a female",
    ai_role_postfix="Answer as concisely as possible.",
    title="LLM Explorer",
    language="English",
    lang_code="en",
    donates="Donates",
    donates1="Russia",
    donates2="World",
    chat_placeholder="Start Your Conversation With AI:",
    chat_run_btn="Ask",
    chat_clear_btn="Clear",
    chat_save_btn="Save",
    speak_btn="Push to Speak",
    input_kind="Input Kind",
    input_kind_1="Text",
    input_kind_2="Voice [test mode]",
    select_placeholder1="Select Model",
    select_placeholder2="Select Role",
    select_placeholder3="Create Role",
    radio_placeholder="Role Interaction",
    radio_text1="Select",
    radio_text2="Create",
    stt_placeholder="To Hear The Voice Of AI Press Play",
    footer_title="Support & Feedback",
    footer_option0="Chat",
    footer_option1="Info",
    footer_option2="Donate",
    footer_chat="LLM Explorer Chat",
    footer_channel="LLM Explorer Channel",
    responsibility_denial="""
        `LLM Explorer` uses the `Open AI` API to interact with `ChatGPT`, an AI that generates information.
        Please note that neural network responses may not be reliable, inaccurate or irrelevant.
        We are not responsible for any consequences associated with the use or reliance on the information provided.
        Use the received data at your discretion.
    """,
    donates_info="""
        `LLM Explorer` collects donations solely for the purpose of paying for the `Open AI` API.
        This allows you to provide access to communication with AI for all users.
        Support us for joint development and interaction with the intelligence of the future!
    """,
    tokens_count="Tokens count: ",
    message_cost="Message cost: ",
    total_cost="Total cost of conversation: ",
    empty_api_handler=f"""
        API key not found. Create `.streamlit/secrets.toml` with your API key.
        See [README.md]({README_URL}) for instructions or use the original [LLM Explorer]({LLM_EXPLORER_URL}).
    """,
)


es = Locale(
    ai_role_options=AI_ROLE_OPTIONS_ES,
    ai_role_prefix="Eres una asistente femenina",
    ai_role_postfix="Responde de manera concisa.",
    title="LLM Explorer",
    language="Español",
    lang_code="es",
    donates="Donaciones",
    donates1="Rusia",
    donates2="Mundo",
    chat_placeholder="Comienza tu conversación con AI:",
    chat_run_btn="Preguntar",
    chat_clear_btn="Borrar",
    chat_save_btn="Guardar",
    speak_btn="Presiona para hablar",
    input_kind="Tipo de entrada",
    input_kind_1="Texto",
    input_kind_2="Voz [modo de prueba]",
    select_placeholder1="Seleccionar modelo",
    select_placeholder2="Seleccionar rol",
    select_placeholder3="Crear rol",
    radio_placeholder="Interacción del rol",
    radio_text1="Seleccionar",
    radio_text2="Crear",
    stt_placeholder="Para escuchar la voz de AI, presiona Reproducir",
    footer_title="Soporte y comentarios",
    footer_option0="Chat",
    footer_option1="Información",
    footer_option2="Donar",
    footer_chat="Chat de LLM Explorer",
    footer_channel="Canal de LLM Explorer",
    responsibility_denial="""
        `LLM Explorer` utiliza la API de `Open AI` para interactuar con `ChatGPT`, una IA que genera información.
        Ten en cuenta que las respuestas de la red neuronal pueden no ser confiables, precisas o relevantes.
        No somos responsables de las consecuencias asociadas con el uso o la dependencia de la información proporcionada.
        Utiliza los datos recibidos a tu discreción.
    """,
    donates_info="""
        `LLM Explorer` recopila donaciones exclusivamente con el propósito de pagar por la API de `Open AI`.
        Esto te permite proporcionar acceso a la comunicación con AI para todos los usuarios.
        ¡Apóyanos para el desarrollo conjunto e interacción con la inteligencia del futuro!
    """,
    tokens_count="Cantidad de tokens: ",
    message_cost="Costo por mensaje: ",
    total_cost="Costo total de la conversación: ",
    empty_api_handler="""
        No se encontró la clave de API. Crea un archivo `.streamlit/secrets.toml` con tu clave de API.
        Consulta el [README.md]({README_URL}) para obtener instrucciones o utiliza el [LLM Explorer original]({LLM_EXPLORER_URL}).
    """,
)
