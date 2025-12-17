# == Third party import
import pytest
# == Local import
from models.film import Film

def test_film_initialization():
    """Test that Film is initialized correctly with all fields."""
    film = Film(name="Apollo 13", year=1995, rating=7.6, id="F1")

    assert film.name == "Apollo 13"
    assert film.year == 1995
    assert film.rating == 7.6
    assert film.id == "F1"
    assert film.cast == []


def test_film_with_cast():
    """Test that cast can be added to the Film object."""
    film = Film(name="Apollo 13", year=1995, rating=7.6, id="F1")
    film.cast.extend(["Tom Hanks", "Kevin Bacon", "Bill Paxton"])

    assert "Tom Hanks" in film.cast
    assert "Kevin Bacon" in film.cast
    assert "Bill Paxton" in film.cast
    assert len(film.cast) == 3


def test_cast_uniqueness():
    """Test adding duplicate actors to cast list."""
    film = Film(name="Apollo 13", year=1995, rating=7.6, id="F1")
    film.cast.extend(["Tom Hanks", "Tom Hanks"])

    # List allows duplicates, so both entries exist
    assert film.cast.count("Tom Hanks") == 2


def test_multiple_films_and_casts():
    """Test multiple Film instances with different casts."""
    film1 = Film(name="Apollo 13", year=1995, rating=7.6, id="F1",
                 cast=["Tom Hanks"])
    film2 = Film(name="Forrest Gump", year=1994, rating=8.8, id="F2",
                 cast=["Tom Hanks"])

    assert film1.name == "Apollo 13"
    assert film2.name == "Forrest Gump"
    assert film1.cast == ["Tom Hanks"]
    assert film2.cast == ["Tom Hanks"]
