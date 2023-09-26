from opencopilot.repository.documents.document_store import WeaviateDocumentStore as WS


def test_index_name():
    assert "OPENCOPILOT" == WS.get_index_name()
    assert "OPENCOPILOT" == WS.get_index_name("OPENCOPILOT")

    assert "OPENCOPILOT" == WS.get_index_name("opencopilot")
    assert "OPENCOPILOT" == WS.get_index_name("Opencopilot")

    assert "COPILOT" == WS.get_index_name("copilot")
    assert "COPILOT" == WS.get_index_name("COPILOT")
    assert "COPILOT" == WS.get_index_name("CoPilot")

    assert "CUSTOMCOPILOT" == WS.get_index_name("Custom Copilot")
    assert "CUSTOMCOPILOT" == WS.get_index_name("CUSTOM CO PILOT1 2 ")

    assert "OPENCOPILOT" == WS.get_index_name("")
    assert "OPENCOPILOT" == WS.get_index_name("222")
    assert "OPENCOPILOT" == WS.get_index_name("222 -- 2313213121..,, ")
