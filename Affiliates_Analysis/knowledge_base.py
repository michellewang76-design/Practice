import os
import docx
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings

class VectorDBManager:
    def __init__(self, persist_directory="./chroma_db"):
        """初始化向量数据库和 Embedding 模型"""
        self.persist_directory = persist_directory
        self.embedding_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vector_store = Chroma(
            persist_directory=self.persist_directory, 
            embedding_function=self.embedding_model
        )

    def _extract_text(self, file):
        """内部方法：从不同格式的文件中提取纯文本"""
        if file.name.endswith('.docx'):
            doc = docx.Document(file)
            return '\n'.join([para.text for para in doc.paragraphs if para.text.strip()])
        else:
            return file.read().decode('utf-8')

    def add_documents(self, uploaded_files):
        """处理上传的文件，使用【文件名】进行查重"""
        total_chunks = 0
        skipped_files = []
        added_files = []

        for file in uploaded_files:
            file_name = file.name
            
            # 1. 查重：在 ChromaDB 中查询是否已经存在该文件名的记录
            existing_docs = self.vector_store.get(where={"source": file_name})
            
            if existing_docs and len(existing_docs.get('ids', [])) > 0:
                # 如果已经存在，记录到跳过列表，直接处理下一个文件
                skipped_files.append(file_name)
                continue

            # 2. 提取文本并分块
            file.seek(0)
            text = self._extract_text(file)
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            chunks = text_splitter.split_text(text)
            
            # 3. 组装 Metadata 并存入数据库
            if chunks:
                # 为该文件的每一个 chunk 贴上包含文件名的标签
                metadatas = [{"source": file_name} for _ in chunks]
                self.vector_store.add_texts(texts=chunks, metadatas=metadatas)
                total_chunks += len(chunks)
                added_files.append(file_name)
                
        # 返回详细的处理结果报告
        return {
            "chunks_saved": total_chunks,
            "added_files": added_files,
            "skipped_files": skipped_files
        }
        
    def get_all_uploaded_filenames(self):
        """获取数据库中所有已上传文件的名称列表"""
        try:
            # 获取数据库中所有的 metadata
            all_data = self.vector_store.get()
            metadatas = all_data.get('metadatas', [])
            
            # 提取唯一的文件名
            unique_files = set()
            for meta in metadatas:
                if meta and 'source' in meta:
                    unique_files.add(meta['source'])
            
            # 返回按字母排序的文件列表
            return sorted(list(unique_files))
        except Exception:
            return []

    def search_similar_context(self, query, top_k=3):
        """为后续 RAG 预留的检索方法"""
        results = self.vector_store.similarity_search(query, k=top_k)
        return [doc.page_content for doc in results]