# == Standard Library import
from math import inf
# == Third party import
import pytest
# == Local import
from models.actor import Actor


def test_actor_initialization():
    """Test that Actor is initialized correctly with all fields."""
    actor = Actor(name="Tom Hanks", id="A1",
                  films=["Apollo 13", "Forrest Gump"])

    assert actor.name == "Tom Hanks"
    assert actor.id == "A1"
    assert actor.films == ["Apollo 13", "Forrest Gump"]
    assert actor.costars == set()
    assert actor.explored is False
    assert actor.bacon_number == inf


def test_restore_default_resets_explored():
    """Test that restore_default sets explored back to False."""
    actor = Actor(name="Tom Hanks", id="A1", films=["Apollo 13"])
    actor.explored = True
    actor.restore_default()
    assert actor.explored is False


def test_add_costars():
    """Test that co-stars can be added to the Actor object."""
    actor = Actor(name="Tom Hanks", id="A1", films=["Apollo 13"])
    actor.costars.update(["Kevin Bacon", "Bill Paxton"])

    assert "Kevin Bacon" in actor.costars
    assert "Bill Paxton" in actor.costars
    assert len(actor.costars) == 2


def test_bacon_number_assignment():
    """Test that bacon_number can be updated."""
    actor = Actor(name="Tom Hanks", id="A1", films=["Apollo 13"])
    actor.bacon_number = 2
    assert actor.bacon_number == 2


def test_multiple_films_and_costars():
    """Test that multiple films and co-stars are handled correctly."""
    actor = Actor(name="Tom Hanks", id="A1",
                  films=["Apollo 13", "Forrest Gump"])
    actor.costars.update(["Kevin Bacon", "Gary Sinise"])

    assert set(actor.films) == {"Apollo 13", "Forrest Gump"}
    assert actor.costars == {"Kevin Bacon", "Gary Sinise"}
