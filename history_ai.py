import os
from langchain_google_genai import ChatGoogleGenerativeAI # type: ignore
from langchain.chains import ConversationChain # type: ignore
from langchain.memory import ConversationBufferMemory # type: ignore
from langchain.prompts import ( # type: ignore
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
    MessagesPlaceholder,
)
from dotenv import load_dotenv # type: ignore


# Cargar variables de entorno desde el archivo .env
load_dotenv()
print("GOOGLE_API_KEY:", os.getenv("GOOGLE_API_KEY"))

class HistoryAI:
    """
    IA experta en psicología implementada con LangChain y Google Gemini.
    Mantiene memoria de la conversación para proporcionar respuestas
    contextualizadas.
    """
    
    def __init__(self):
        """Inicializa la IA con el modelo, la memoria y el prompt personalizado."""
        # Inicializar el modelo de lenguaje Gemini
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",  # Usar el modelo Gemini Pro
            temperature=0.7,
            verbose=True
        )
        
        # Inicializar la memoria de conversacion
        self.memory = ConversationBufferMemory(
            return_messages=True,
            memory_key="chat_history"
        )
        
        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(
                """
                Dado que eres un experto en literatura y creación de historias, quiero que crees una historia, para crearla debes  tener en cuenta las siguientes reglas para crear una buena historia:
                1. Usa el genero que se te indique en los requerimientos, debes ceñirte muy bien a las características de dicho genero para crear la historia, es decir, los cuentos se caracterizan por tener introducción, nudo y desenlace, por lo que debes estructurar la historia de la manera correcta, si el género no es especificado, debes tener en cuenta los demás requerimientos para escoger un género con el fin de crear una historia interesante, puedes tener en cuenta aspectos como ambientación, personajes, sentimiento deseado a transmitir, etc.
                2. Ten presente la extensión que se pide para crear la historia, si esta no es especificada, crea la historia con un rango de 300 a 800 palabras.
                3. Asegúrate de mantener coherencia narrativa y estructural entre los hechos de la historia, conversaciones, personajes y demás.
                4. Debes tener en cuenta los personajes que se piden en la historia, recuerda crearlos con respecto a su personalidad, cualidadades y caracteristicas establecidas desde el inicio, estas no deben cambiar a no ser de que la historia lo requiera, por ejemplo, en caso de que un personaje requiera un desarrollo o un cambio debido a los hechos ocurridos. si  no se especifican los personajes o parte de sus caracteristicas, crea personajes coherentes con los demás aspectos de la historia, adicionalmente asegúrate de crear conversaciones coherentes con la historia, características y personalidades de los personajes.
                5. Con respecto al escenario, comienza a generar la historia a partir del escenario pedido, en caso de no ser pedido usa el escenario que mejor se acomode a la historia.
                6. Ten en cuenta los elementos de la trama pedidos como: Tipo de conflicto, obstáculos, estilo de resolución, ya que esto es importante para que estructures la historia, especialmente con la extensión de esta para que se puedan incluir y desarrollarse todos los elementos de la manera correcta.
                7. Toma en cuenta el tono y el sentimiento que se quiere conseguir con la historia, es decir, si  se pide que la historia tenga tono humorístico, dramático o satírico, debes incluirlo en la historia al igual que el sentimiento que se quiere expresar.
                Solo responde con el título y la historia creada, en caso de que se pida una conclusión o moraleja también puedes darla, solo danos el texto plano sin caracteres extraños como para especificar negritas tipo (** **), dado esto genera un JSON con los siguientes campos {{"titulo", "historia"}}.

                los requerimientos para la historia son los siguientes:
                """
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{input}")
        ])
        
        # Crear la cadena de conversacion
        self.conversation = ConversationChain(
            llm=self.llm,
            memory=self.memory,
            prompt=prompt,
            verbose=True
        )
    
    def process_message(self, message):
        """
        Procesa un mensaje del usuario y devuelve la respuesta de la IA.
        
        Args:
            message (str): El mensaje del usuario
            
        Returns:
            str: La respuesta de la IA
        """
        response = self.conversation.predict(input=message)
        return response
    
    def reset_memory(self):
        """Reinicia la memoria de la conversación."""
        self.memory.clear()

# Instancia singleton para usar en toda la aplicacion
history_ai = HistoryAI()