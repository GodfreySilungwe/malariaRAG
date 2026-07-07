import sys
import types
import unittest
import json
import os
from unittest.mock import patch, MagicMock


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
import malaria_client


class FormatSourcesTests(unittest.TestCase):
    """Tests for malaria_rag.format_sources function."""
    
    def test_page_numbers_are_included_in_sources(self):
        """Test that page numbers are properly formatted in sources."""
        doc = Document(
            page_content="Example content",
            metadata={"source": "policy.pdf", "page": 3}
        )
        sources = malaria_rag.format_sources([doc])
        
        self.assertEqual(sources[0]["source"], "policy.pdf (page 3)")
        self.assertEqual(sources[0]["page_number"], 3)
    
    def test_empty_sources_list(self):
        """Test handling of empty sources list."""
        sources = malaria_rag.format_sources([])
        self.assertEqual(len(sources), 0)

    def test_source_metadata_is_exposed_for_frontend_display(self):
        """Test that source metadata is exposed with document/page fields for the UI."""
        doc = Document(
            page_content="Example content",
            metadata={"source": "Revised Malaria Treatment Guidelines", "page": 14}
        )
        sources = malaria_rag.format_sources([doc])

        self.assertEqual(sources[0]["document"], "Revised Malaria Treatment Guidelines")
        self.assertEqual(sources[0]["page"], 14)
        self.assertEqual(sources[0]["page_number"], 14)
        self.assertIn("Revised Malaria Treatment Guidelines", sources[0]["citation"])
    
    def test_sources_without_metadata(self):
        """Test handling of documents without metadata."""
        doc = Document(page_content="Content without metadata")
        sources = malaria_rag.format_sources([doc])
        
        self.assertEqual(len(sources), 1)
        self.assertIn("source", sources[0])


class StreamlitClientTests(unittest.TestCase):
    """Tests for the Streamlit chat display helper."""

    def test_prepare_streamlit_display_includes_sources_and_snippets(self):
        """Test that the Streamlit formatter exposes citation data for the chat UI."""
        response = {
            "answer": "Answer text",
            "sources": [{"id": 1, "document": "policy.pdf", "citation": "policy.pdf (page 3)"}],
            "snippets": ["Snippet one"],
        }

        display = malaria_client.prepare_streamlit_display(response)

        self.assertEqual(display["answer"], "Answer text")
        self.assertEqual(display["citations"][0]["id"], 1)
        self.assertEqual(display["citations"][0]["citation"], "policy.pdf (page 3)")
        self.assertEqual(display["citations"][0]["snippet"], "Snippet one")


class MalariaRAGTests(unittest.TestCase):
    """Tests for core RAG functionality."""

    @patch('malaria_rag.retrieve_docs_with_scores')
    def test_answer_and_sources_returns_fields_in_requested_order(self, mock_retrieve):
        """Test that the API payload is ordered as answer, snippets, sources, latency_ms."""
        doc = Document(page_content="Example content", metadata={"source": "policy.pdf", "page": 3})
        mock_retrieve.return_value = [(doc, 0.9)]

        with patch('malaria_rag.model_module.get_model', return_value=MagicMock(invoke=lambda messages: Message("answer"))):
            result = malaria_rag.answer_and_sources("What is malaria?")

        self.assertEqual(list(result.keys()), ["answer", "snippets", "sources", "latency_ms"])

    @patch('malaria_rag.retrieve_docs_with_scores')
    def test_clean_answer_text_preserves_citation_markers(self, mock_retrieve):
        """Test that answer text keeps inline citation markers in the main paragraph."""
        doc = Document(page_content="Example content", metadata={"source": "policy.pdf", "page": 3})
        mock_retrieve.return_value = [(doc, 0.9)]

        with patch('malaria_rag.model_module.get_model', return_value=MagicMock(invoke=lambda messages: Message("Answer [1] with citations."))):
            result = malaria_rag.answer_and_sources("What is malaria?")

        self.assertEqual(result["answer"], "Answer [1] with citations.")
    
    def test_extract_page_number_with_page_key(self):
        """Test page number extraction with 'page' metadata key."""
        doc = Document(
            page_content="test",
            metadata={"page": 5}
        )
        page_num = malaria_rag._extract_page_number(doc)
        self.assertEqual(page_num, 5)
    
    def test_extract_page_number_with_page_number_key(self):
        """Tests page number extraction with 'page_number' metadata key."""
        doc = Document(
            page_content="test",
            metadata={"page_number": 10}
        )
        page_num = malaria_rag._extract_page_number(doc)
        self.assertEqual(page_num, 10)
    
    def test_extract_page_number_returns_none_when_missing(self):
        """Test that None is returned when page number is not found."""
        doc = Document(page_content="test", metadata={})
        page_num = malaria_rag._extract_page_number(doc)
        self.assertIsNone(page_num)


class APITests(unittest.TestCase):
    """Tests for Flask API endpoints."""
    
    def setUp(self):
        """Set up Flask test client."""
        # Import Flask app
        from app import app
        self.app = app
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
    
    def tearDown(self):
        """Clean up after tests."""
        self.app_context.pop()
    
    def test_health_endpoint(self):
        """Test the /health endpoint."""
        response = self.client.get("/health")
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["status"], "ok")
    
    def test_index_endpoint(self):
        """Test the / endpoint."""
        response = self.client.get("/")
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("message", data)
    
    def test_chat_endpoint_missing_question(self):
        """Test /chat endpoint with missing question."""
        response = self.client.post(
            "/chat",
            data=json.dumps({}),
            content_type="application/json"
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("error", data)
    
    @patch('malaria_rag.answer_and_sources')
    def test_chat_endpoint_with_question(self, mock_answer):
        """Test /chat endpoint with valid question."""
        mock_answer.return_value = {
            "answer": "Test answer",
            "sources": [{"document": "test.pdf", "page": 1}]
        }
        
        response = self.client.post(
            "/chat",
            data=json.dumps({"question": "What is malaria?"}),
            content_type="application/json"
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("answer", data)
        self.assertIn("sources", data)


class IntegrationTests(unittest.TestCase):
    """Integration tests for the complete system."""
    
    def test_refusal_template_exists(self):
        """Test that refusal template is defined."""
        self.assertIsNotNone(malaria_rag.REFUSE_TEMPLATE)
        self.assertIn("policy documents", malaria_rag.REFUSE_TEMPLATE)
    
    def test_top_k_configuration(self):
        """Test that TOP_K configuration is set."""
        self.assertIsNotNone(malaria_rag.TOP_K)
        self.assertGreater(malaria_rag.TOP_K, 0)
        self.assertLessEqual(malaria_rag.TOP_K, 10)


if __name__ == "__main__":
    unittest.main()
