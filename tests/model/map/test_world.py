from model.world import World


class TestWorld:
    def test_initialization(self, mock_sample):
        world = World(width=5, height=5, sample=mock_sample)
        assert world.width == 5
        assert world.height == 5

    def test_regions_count(self, mock_sample):
        world = World(width=3, height=4, sample=mock_sample)
        regions = list(world.regions)
        assert len(regions) == 12

    def test_neighbors_connected(self, mock_sample):
        world = World(width=3, height=3, sample=mock_sample)
        center_region = world.region_at(1, 1)
        assert len(center_region.neighbors) == 4

    def test_corner_has_2_neighbors(self, mock_sample):
        world = World(width=3, height=3, sample=mock_sample)
        corner_region = world.region_at(0, 0)
        assert len(corner_region.neighbors) == 2

    def test_edge_has_3_neighbors(self, mock_sample):
        world = World(width=3, height=3, sample=mock_sample)
        edge_region = world.region_at(0, 1)
        assert len(edge_region.neighbors) == 3
