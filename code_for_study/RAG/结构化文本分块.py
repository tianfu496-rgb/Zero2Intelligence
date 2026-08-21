from jupyter_client.session import msg_header
from langchain_text_splitters import MarkdownHeaderTextSplitter

#makrdown格式文本
markdown_text = ""

headers_to_split_on = [
    ("#","Header 1"),
    ("##","Header 2")
]

text_splitter = MarkdownHeaderTextSplitter(
headers_to_split_on = headers_to_split_on,
)
msg_header_splits = text_splitter(markdown_text)

print(msg_header_splits)