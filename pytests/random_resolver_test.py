import pytest
from unittest.mock import MagicMock, patch
import resolvers
import grid
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

possible_starters: list[grid.Intersection] = [
            grid.Line(grid.Intersection(-4, 3), 1, 0), grid.Line(grid.Intersection(-4, 3), 0, 1),
            grid.Line(grid.Intersection(-4, 4), 1, -1), grid.Line(grid.Intersection(-4, 5), 1, 1),
            grid.Line(grid.Intersection(-4, 6), 1, 0), grid.Line(grid.Intersection(-4, 6), 0, -1),
            grid.Line(grid.Intersection(-1, 0), 1, 0), grid.Line(grid.Intersection(-1, 0), 0, 1),
            grid.Line(grid.Intersection(-5, 3), 1, 0), grid.Line(grid.Intersection(-1, -1), 1, 0),
            grid.Line(grid.Intersection(-5, 6), 1, 0), grid.Line(grid.Intersection(-1, 6), 0, 1),
            grid.Line(grid.Intersection(-1, 9), 1, 0), grid.Line(grid.Intersection(-1, 5), 0, -1),
            grid.Line(grid.Intersection(1, 0), 1, 1), grid.Line(grid.Intersection(1, 9), 1, -1),
            grid.Line(grid.Intersection(2, 0), 0, 1), grid.Line(grid.Intersection(-2, 0), 1, 0),
            grid.Line(grid.Intersection(2, 3), 1, 0), grid.Line(grid.Intersection(-1, 2), 0, 1),
            grid.Line(grid.Intersection(2, 6), 1, 0), grid.Line(grid.Intersection(2, 6), 0, 1),
            grid.Line(grid.Intersection(-2, 9), 1, 0), grid.Line(grid.Intersection(2, 5), 0, 1),
            grid.Line(grid.Intersection(1, 3), 1, 0), grid.Line(grid.Intersection(5, 3), 0, 1),
            grid.Line(grid.Intersection(1, 6), 1, 0), grid.Line(grid.Intersection(5, 2), 0, 1)
        ]

@pytest.mark.timeout(2)
def test_add_a_line():
    gridi = grid.Grid()

    with patch("resolvers.Grid") as MockGrid:
        mock_grid_instance = MagicMock()
        mock_grid = MagicMock(spec=grid.Grid)
        mock_grid.get_intersections.return_value = gridi.get_intersections()

        mock_view = MagicMock(spec=view.View)

        resolver = resolvers.RandomResolver()
        resolver.set_view(mock_view)

        resolver.add_a_line()

        # mock_grid.add_line_to_grid.assert_any_call(grid.Line(grid.Intersection(-4, 3), 1, 0))

        added_lines = [call.args[0] for call in mock_grid.add_line_to_grid.call_args_list]
        assert len(added_lines) == 1, "Should have added one line."
        assert added_lines[0] in possible_starters, f"Invalid line {added_lines[0]} added."

        #        self.game_grid.add_line_to_grid(line)


