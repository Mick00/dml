import unittest

from src.base.states.state import State


class StateTest(unittest.TestCase):

    def test_get_state(self):
        state = State()
        module_name_0 = "mod0"
        module_name_1 = "mod1"
        self.assertEqual(state.get_module_state(module_name_0), {})
        self.assertEqual(state.get_module_state(module_name_1), {})
        change_mod_0 = {"foo": "bar", "hello": "world"}
        state.update_module(module_name_0, change_mod_0)
        self.assertEqual(state.get_module_state(module_name_0), change_mod_0)
        self.assertEqual(state.get_module_state(module_name_1), {})
        change_mod_1 = {"this": 123}
        state.update_module(module_name_1, change_mod_1)
        self.assertEqual(state.get_module_state(module_name_0), change_mod_0)
        self.assertEqual(state.get_module_state(module_name_1), change_mod_1)
        change_mod_2 = {"lol": "hi", "hello": "you"}
        state.update_module(module_name_0, change_mod_2)
        self.assertEqual(state.get_module_state(module_name_0), change_mod_0 | change_mod_2)
        self.assertEqual(state.get_module_state(module_name_1), change_mod_1)

    def test_mutation_are_impossible(self):
        state = State()
        module_name = "mod0"
        change_mod = {"foo": "bar", "hello": "world"}
        state.update_module(module_name, change_mod)
        self.assertEqual(state.get_module_state(module_name), change_mod)
        og_module = change_mod.copy()
        change_mod["new"] = "key"
        self.assertEqual(state.get_module_state(module_name), og_module)
        state.get_module_state(module_name)["new"] = "key"
        self.assertEqual(state.get_module_state(module_name), og_module)

    @unittest.skip
    def test_deep_update(self):
        state = State()
        module_name = "mod0"
        init_state = {"foo": {"bar": "hello"}}
        state.update_module(module_name, init_state)
        mod_state = {"foo": {"test": "hoho"}}
        state.update_module(module_name, mod_state)
        self.assertEqual(state.get_module_state(module_name), {"foo": {"bar": "hello", "test": "hoho"}})

if __name__ == '__main__':
    unittest.main()