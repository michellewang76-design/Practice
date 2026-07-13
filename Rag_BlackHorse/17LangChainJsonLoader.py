from langchain_community.document_loaders import JSONLoader

loader = JSONLoader(
    file_path="./data/stu.json",
    jq_schema=".",
    text_content=False,         # 告知JSONLoader 我抽取的内容不是字符串
)

document = loader.load()
print(document)

########################################

loader = JSONLoader(
    file_path="./data/stus.json",
    jq_schema=".[].name",
    text_content=False,         # 告知JSONLoader 我抽取的内容不是字符串
)

document = loader.load()
print(document)

########################################

loader = JSONLoader(
    file_path="./data/stu_json_lines.json",
    jq_schema=".name",
    text_content=False,      # 告知JSONLoader 我抽取的内容不是字符串
    json_lines=True         # 告知JSONLoader 这是一个JSON LINES文件，每一行都是一个JSON文件
)

document = loader.load()
print(document)