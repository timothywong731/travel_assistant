from app.prompt import generate_prompt

def test_generate_prompt():
    """
    Test the generate_prompt function to ensure it returns a non-empty string.
    """
    query = "What are the best hotels in Paris?"
    prompt = generate_prompt(query)
    
    assert isinstance(prompt, str), "Prompt should be a string"
    assert len(prompt) > 0, "Prompt should not be empty"
    assert "Paris" in prompt, "Prompt should contain the query term 'Paris'"