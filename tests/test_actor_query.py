# == Third party import
import pytest
# == Local import
from models.actor import Actor
from processor.actorQuery import ActorQuery, PathSegment, generate_actors_path, \
    generate_complete_path


@pytest.fixture
def sample_actor_dict():
    """
    Create a small actor graph for testing:
    - Tom Hanks acted with Kevin Bacon in Apollo 13
    - Kevin Bacon acted with Bill Paxton in Apollo 13
    - Tom Hanks acted with Bill Paxton in Apollo 13
    """
    tom = Actor(name="Tom Hanks", id="A1", films=["Apollo 13"])
    kevin = Actor(name="Kevin Bacon", id="A2", films=["Apollo 13"])
    bill = Actor(name="Bill Paxton", id="A3", films=["Apollo 13"])

    # Populate costars
    tom.costars.update(["Kevin Bacon", "Bill Paxton"])
    kevin.costars.update(["Tom Hanks", "Bill Paxton"])
    bill.costars.update(["Tom Hanks", "Kevin Bacon"])

    return {
        "Tom Hanks": tom,
        "Kevin Bacon": kevin,
        "Bill Paxton": bill
    }


def test_run_bfs_shortest_path(sample_actor_dict):
    """Test BFS finds the shortest path and correct Bacon number."""
    query = ActorQuery("Tom Hanks", "Bill Paxton")
    query.run_bfs(sample_actor_dict)

    # Bacon number should be 1 since they are direct co-stars
    assert query.bacon_number == 1

    # Check that complete_path contains correct PathSegment
    assert len(query.complete_path) == 1
    segment = query.complete_path[0]
    assert isinstance(segment, PathSegment)
    assert segment.actor1 == "Tom Hanks"
    assert segment.actor2 == "Bill Paxton"
    assert segment.shared_films == ["Apollo 13"]


def test_run_bfs_multiple_hops(sample_actor_dict):
    """Test BFS finds shortest path when multiple hops exist."""
    # Add an extra actor to force multi-hop
    chris = Actor(name="Chris Pratt", id="A4", films=["Guardians"])
    chris.costars.update(["Bill Paxton"])
    sample_actor_dict["Bill Paxton"].costars.add("Chris Pratt")
    sample_actor_dict["Chris Pratt"] = chris

    query = ActorQuery("Tom Hanks", "Chris Pratt")
    query.run_bfs(sample_actor_dict)

    # Should find path via Bill Paxton
    assert query.bacon_number == 2
    path_actors = [seg.actor1 for seg in query.complete_path.values()] + [
        query.complete_path[max(query.complete_path.keys())].actor2]
    assert path_actors[0] == "Tom Hanks"
    assert path_actors[-1] == "Chris Pratt"


def test_run_bfs_same_actor(sample_actor_dict):
    """Test BFS when origin and destination are the same."""
    query = ActorQuery("Tom Hanks", "Tom Hanks")
    query.run_bfs(sample_actor_dict)

    assert query.bacon_number == 0
    assert query.complete_path == {}


def test_run_bfs_missing_actor(sample_actor_dict, capsys):
    """Test BFS when one actor is missing."""
    query = ActorQuery("Tom Hanks", "Unknown Actor")
    query.run_bfs(sample_actor_dict)

    captured = capsys.readouterr()
    assert "Second actor Unknown Actor not found." in captured.out
    assert query.bacon_number == float("inf")
    assert query.complete_path == {}


def test_get_path_strings_returns_correct_format(sample_actor_dict):
    """Test _get_path_strings returns formatted output."""
    query = ActorQuery("Tom Hanks", "Kevin Bacon")
    query.run_bfs(sample_actor_dict)

    strings = query._get_path_strings()
    assert isinstance(strings, list)
    assert strings[0].startswith("Kevin Bacon has a Bacon number of")
    assert any(
        "Tom Hanks and Kevin Bacon starred together in Apollo 13" in s for s in
        strings)


def test_generate_actors_path_and_complete_path(sample_actor_dict):
    """Test the helper functions directly."""
    prev = {"Kevin Bacon": "Tom Hanks", "Bill Paxton": "Kevin Bacon"}
    path = generate_actors_path("Tom Hanks", "Bill Paxton", prev)
    assert path == ["Tom Hanks", "Kevin Bacon", "Bill Paxton"]

    complete_path = generate_complete_path(sample_actor_dict, path)
    assert len(complete_path) == 2
    segment0 = complete_path[0]
    assert segment0.actor1 == "Tom Hanks"
    assert segment0.actor2 == "Kevin Bacon"
    assert segment0.shared_films == ["Apollo 13"]