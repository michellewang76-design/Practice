from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.document_loaders import CSVLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
import os
from langchain_groq import ChatGroq
from langchain_chroma import Chroma
import chromadb

embed = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

# 把内存存储改掉
# vector_store = InMemoryVectorStore(
#     embedding=embed
# )

# 改成外部永久存储
vector_store = Chroma(
    collection_name="test",           # 当前向量存储起个名字，类似数据库的表名称
    embedding_function=embed,         # 嵌入模型 (注意：在 Chroma 中这个参数叫 embedding_function 或 embedding 都可以)
    persist_directory="./chroma_db"   # 指定数据存放的文件夹
)

loader = CSVLoader(
    file_path="./data/info.csv",
    encoding="utf-8",
    source_column="source",       # 指定本条数据的来源是哪里
)

documents = loader.load()

# id1 id2 id3 id4 ...
# 向量存储的 新增、删除、检索
vector_store.add_documents(
    documents=documents,            # 被添加的文档，类型：list[Document]
    ids=["id"+str(i) for i in range(1, len(documents)+1)] # 给添加的文档提供id（字符串） list[str]
)

# 删除  传入[id, id...]
vector_store.delete(["id1", "id2"])

# 检索 返回类型list[Document]
result = vector_store.similarity_search(
    "Is Python easy to learn?",
    k=3             # 检索的结果要几个
)

print(result)