from model.agent.action import Action


class TestAction:
    def test_action_values(self):
        assert Action.EAT.value == 0
        assert Action.MIGRATE.value == 1
        assert Action.REPRODUCE.value == 2

    def test_action_count(self):
        assert len(Action) == 3
