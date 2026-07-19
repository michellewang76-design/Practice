from abc import ABC, abstractmethod
from typing import Optional
from utils.config_handler_3 import rag_conf
from dotenv import load_dotenv
load_dotenv()

# from langchain_core.embeddings import Embeddings
# from langchain_community.chat_models.tongyi import BaseChatModel
# from langchain_community.embeddings import DashScopeEmbeddings
# from langchain_community.chat_models.tongyi import ChatTongyi

# 保留底层核心的类型标注
from langchain_core.embeddings import Embeddings
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_groq import ChatGroq


class BaseModelFactory(ABC):
    @abstractmethod
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        pass


class ChatModelFactory(BaseModelFactory):
    def generator(self)->Optional[Embeddings | BaseChatModel]:
        return ChatGroq(model=rag_conf["chat_model_name"])


class EmbeddingsFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        return GoogleGenerativeAIEmbeddings(model=rag_conf["embedding_model_name"])


chat_model = ChatModelFactory().generator()

embed_model = EmbeddingsFactory().generator()
