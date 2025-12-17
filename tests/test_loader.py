# == Third party import
import pytest
import pandas as pd
# == Local import
from models.actor import Actor
from utils.loader import Loader

# Sample DataFrame to mock CSV input
sample_data = pd.DataFrame({
    "Actor": ["Tom Hanks", "Kevin Bacon", "Bill Paxton", "Tom Hanks"],
    "ActorID": ["A1", "A2", "A3", "A1"],
    "Film": ["Apollo 13", "Apollo 13", "Apollo 13", "Forrest Gump"]
})

@pytest.fixture
def mock_inputs(monkeypatch):
    """Mock user input for two actors."""
    monkeypatch.setattr("builtins.input", lambda prompt: "Tom Hanks" if "first" in prompt else "Kevin Bacon")

@pytest.fixture
def loader_instance(monkeypatch, mock_inputs):
    """Create a Loader instance with mocked CSV reading and user input."""
    monkeypatch.setattr("pandas.read_csv", lambda filepath, dtype: sample_data)
    return Loader("dummy_path.csv")

def test_loader_initialization(loader_instance):
    """Test Loader initialization and actor_dict creation."""
    loader = loader_instance
    # Check that user-provided actors are stored
    assert loader.actor_1 == "Tom Hanks"
    assert loader.actor_2 == "Kevin Bacon"
    # Check that actor_dict is populated
    assert isinstance(loader.actor_dict, dict)
    assert "Tom Hanks" in loader.actor_dict
    assert "Kevin Bacon" in loader.actor_dict

def test_actor_graph_population(loader_instance):
    """Test that Actor objects have correct films and costars."""
    actor_dict = loader_instance.actor_dict
    tom_hanks = actor_dict["Tom Hanks"]
    kevin_bacon = actor_dict["Kevin Bacon"]

    # Tom Hanks films
    assert set(tom_hanks.films) == {"Apollo 13", "Forrest Gump"}
    # Kevin Bacon films
    assert kevin_bacon.films == ["Apollo 13"]
    # Costars
    assert "Kevin Bacon" in tom_hanks.costars
    assert "Tom Hanks" in kevin_bacon.costars
    assert "Bill Paxton" in tom_hanks.costars

def test_load_dataframe_method(monkeypatch, mock_inputs):
    """Test _load_dataframe returns the correct DataFrame."""
    monkeypatch.setattr("pandas.read_csv", lambda filepath, dtype: sample_data)
    loader = Loader("dummy_path.csv")
    df = loader._load_dataframe()
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["Actor", "ActorID", "Film"]

def test_load_data_method(monkeypatch, mock_inputs):
    """Test _load_data returns a dictionary of Actor objects."""
    monkeypatch.setattr("pandas.read_csv", lambda filepath, dtype: sample_data)
    loader = Loader("dummy_path.csv")
    actor_dict = loader._load_data()
    assert isinstance(actor_dict, dict)
    for actor in actor_dict.values():
        assert isinstance(actor, Actor)
        assert isinstance(actor.films, list)
        assert isinstance(actor.costars, set)
