
md5_path = "./md5.text"

# Chroma
collection_name="rag"
persist_directory="./chroma_db"

# spliter
chunk_size= 1000
chunk_overlap= 100
separators =["\n\n","\n",".","!","?","。","！","？"," ",""]

max_spliter_char_number= 1000  # 文本分割阈值

# 相似度K值
similarity_threshold =1     # 检索返回匹配的文档数量

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()

embed = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
model = ChatGroq(model="llama-3.3-70b-versatile")

#
session_config = {
    "configurable": {
        "session_id": "user_001",
    }
}