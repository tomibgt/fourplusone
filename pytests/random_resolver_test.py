import pytest
from unittest.mock import MagicMock, patch
import resolvers
from grid import *
import view

def tet_runner_communication():
    # Create a mock InputOutput
    mock_io = MagicMock(spec=InputOutput)
    
    # Set up mock behavior
    mock_io.receive.return_value = "hello"

    # Inject the mock into Runner
    runner = Runner(mock_io)
    runner.run()

    # Assertions: check communication
    mock_io.send.assert_any_call("Start")
    mock_io.receive.assert_called_once()
    mock_io.send.assert_any_call("Received: hello")
        
    expected_calls = [
        patch.call.send("Start"),
        patch.call.receive(),
        patch.call.send("Received: hello"),
    ]
    mock_io.assert_has_calls(expected_calls)

def tet2_runner_communication():
    with patch("runner.InputOutput") as MockIO:
        mock_io_instance = MagicMock()
        mock_io_instance.receive.return_value = "test input"
        MockIO.return_value = mock_io_instance  # patch constructor

        runner = Runner()
        runner.run()

        mock_io_instance.send.assert_any_call("Start")
        mock_io_instance.receive.assert_called_once()
        mock_io_instance.send.assert_any_call("Received: test input")

initial_intersections: list[Intersection] = [
            Intersection(-4, 3), Intersection(-4, 4), Intersection(-4, 5), Intersection(-4, 6), 
            Intersection(-3, 3), Intersection(-3, 6),
            Intersection(-2, 3), Intersection(-2, 6),
            Intersection(-1, 0), Intersection(-1, 1), Intersection(-1, 2), Intersection(-1, 3),
            Intersection(-1, 6), Intersection(-1, 7), Intersection(-1, 8), Intersection(-1, 9), 
            Intersection(0, 0), Intersection(0, 9),
            Intersection(1, 0), Intersection(1, 9),
            Intersection(2, 0), Intersection(2, 1), Intersection(2, 2), Intersection(2, 3),
            Intersection(2, 6), Intersection(2, 7), Intersection(2, 8), Intersection(2, 9), 
            Intersection(3, 3), Intersection(3, 6),
            Intersection(4, 3), Intersection(4, 6),
            Intersection(5, 3), Intersection(5, 4), Intersection(5, 5), Intersection(5, 6)
        ]

possible_starters: list[Line] = [
            Line(Intersection(-4, 3), 1, 0), Line(Intersection(-4, 3), 0, 1),
            Line(Intersection(-4, 4), 1, -1), Line(Intersection(-4, 5), 1, 1),
            Line(Intersection(-4, 6), 1, 0), Line(Intersection(-4, 6), 0, -1),
            Line(Intersection(-1, 0), 1, 0), Line(Intersection(-1, 0), 0, 1),
            Line(Intersection(-5, 3), 1, 0), Line(Intersection(-1, -1), 1, 0),
            Line(Intersection(-5, 6), 1, 0), Line(Intersection(-1, 6), 0, 1),
            Line(Intersection(-1, 9), 1, 0), Line(Intersection(-1, 5), 0, -1),
            Line(Intersection(1, 0), 1, 1), Line(Intersection(1, 9), 1, -1),
            Line(Intersection(2, 0), 0, 1), Line(Intersection(-2, 0), 1, 0),
            Line(Intersection(2, 3), 1, 0), Line(Intersection(-1, 2), 0, 1),
            Line(Intersection(2, 6), 1, 0), Line(Intersection(2, 6), 0, 1),
            Line(Intersection(-2, 9), 1, 0), Line(Intersection(2, 5), 0, 1),
            Line(Intersection(1, 3), 1, 0), Line(Intersection(5, 3), 0, 1),
            Line(Intersection(1, 6), 1, 0), Line(Intersection(5, 2), 0, 1)
        ]

def is_in_possible_starters(line: Line):
    return line in possible_starters

@pytest.mark.timeout(2)
def test_add_a_line():
    #gridi = Grid()

    with patch("resolvers.Grid") as MockGrid:
        mock_grid_instance = MagicMock()
        MockGrid.return_value = mock_grid_instance
        MockGrid.x_min = -10
        MockGrid.x_max = 10
        MockGrid.y_min = -10
        MockGrid.y_max = 10
        #mock_grid = MagicMock(spec=Grid)
        mock_grid_instance.get_intersections.return_value = initial_intersections
        #mock_grid_instance.is_valid_line.return_value = True
        mock_grid_instance.is_valid_line.side_effect = is_in_possible_starters

        mock_view = MagicMock(spec=view.View)

        resolver = resolvers.RandomResolver()
        resolver.set_view(mock_view)

        output = resolver.add_a_line()

        mock_grid_instance.is_valid_line.assert_any_call, "The resolver is not checking any possible lines."

        added_lines = [call.args[0] for call in mock_grid_instance.add_line_to_grid.call_args_list]
        assert len(added_lines) == 1, "Should have added one line."
        assert added_lines[0] in possible_starters, f"Invalid line {added_lines[0]} added."
        assert output, "The resolver cannot find a possible line."
        #        self.game_grid.add_line_to_grid(line)


