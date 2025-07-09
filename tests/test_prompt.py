from app.prompt import validate_query
import pytest

def test_generate_prompt():
    """
    Test the generate_prompt function to ensure it returns a non-empty string.
    """
    query = "What are the best hotels in Paris?"
    prompt = validate_query(query)
    
    assert isinstance(prompt, str), "Prompt should be a string"
    assert len(prompt) > 0, "Prompt should not be empty"
    assert "Paris" in prompt, "Prompt should contain the query term 'Paris'"

def test_generate_prompt_censored():
    """
    Test that generate_prompt censors inappropriate queries related to gambling.
    """
    with pytest.raises(ValueError) as excinfo:
        validate_query("I want a holiday of endless gambling. Suggest top casinos.")
    assert "Censored topic" in str(excinfo.value)

def test_generate_prompt_case_insensitive_gambling():
    """
    Test that generate_prompt censors 'gambling' regardless of case.
    """
    with pytest.raises(ValueError):
        validate_query("Tell me about gambling resorts in Las Vegas.")
