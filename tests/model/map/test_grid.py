from model.map.grid import Grid


class TestGrid:
    def test_initialization(self, mock_sampler):
        grid = Grid(sampler=mock_sampler, width=5, height=5)
        assert grid._width == 5
        assert grid._height == 5

    def test_regions_count(self, mock_sampler):
        grid = Grid(sampler=mock_sampler, width=3, height=4)
        regions = list(grid.regions)
        assert len(regions) == 12

    def test_neighbors_connected(self, mock_sampler):
        grid = Grid(sampler=mock_sampler, width=3, height=3)
        center_region = grid._data[1][1]
        assert len(center_region.neighbors) == 4

    def test_corner_has_2_neighbors(self, mock_sampler):
        grid = Grid(sampler=mock_sampler, width=3, height=3)
        corner_region = grid._data[0][0]
        assert len(corner_region.neighbors) == 2

    def test_edge_has_3_neighbors(self, mock_sampler):
        grid = Grid(sampler=mock_sampler, width=3, height=3)
        edge_region = grid._data[0][1]
        assert len(edge_region.neighbors) == 3
