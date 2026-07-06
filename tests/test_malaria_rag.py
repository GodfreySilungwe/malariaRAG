import sys
import types
import unittest


class Document:
    def __init__(self, page_content, metadata=None):
        self.page_content = page_content
        self.metadata = metadata or {}


class Message:
    def __init__(self, content):
        self.content = content


langchain_core = types.ModuleType("langchain_core")
documents_module = types.ModuleType("langchain_core.documents")
documents_module.Document = Document
messages_module = types.ModuleType("langchain_core.messages")
messages_module.HumanMessage = lambda content: Message(content)
messages_module.SystemMessage = lambda content: Message(content)
langchain_core.documents = documents_module
langchain_core.messages = messages_module
sys.modules["langchain_core"] = langchain_core
sys.modules["langchain_core.documents"] = documents_module
sys.modules["langchain_core.messages"] = messages_module

sys.modules.setdefault("context", types.SimpleNamespace(get_vector_store=lambda: None))
sys.modules.setdefault("model", types.SimpleNamespace(get_model=lambda: None))

import malaria_rag


class FormatSourcesTests(unittest.TestCase):
    def test_page_numbers_are_included_in_sources(self):
        doc = Document(page_content="Example content", metadata={"source": "policy.pdf", "page": 3})

        sources = malaria_rag.format_sources([doc])

        self.assertEqual(sources[0]["source"], "policy.pdf (page 3)")
        self.assertEqual(sources[0]["page_number"], 3)


if __name__ == "__main__":
    unittest.main()
