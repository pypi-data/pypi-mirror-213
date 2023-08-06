import time
from typing import Dict, List, Any

import freezegun
from pydantic import ValidationError

from openmodule.models.base import Gate
from openmodule.models.settings import SettingsChangedMessage
from openmodule.rpc import RPCServer, RPCClient
from openmodule.utils.settings import SettingsProvider
from openmodule_test.core import OpenModuleCoreTestMixin
from openmodule_test.rpc import RPCServerTestMixin
from openmodule_test.settings import SettingsRPCMocker


class TestSettings(OpenModuleCoreTestMixin, RPCServerTestMixin):
    def setUp(self) -> None:
        super().setUp()

        self.settings = SettingsProvider(rpc_timeout=0.5)
        self.rpc_server = RPCServer(self.zmq_context())
        self.settings_mocker = SettingsRPCMocker(self.rpc_server, {"gate/scope": Gate(gate="1", name="2"),
                                                                   "test/scope": [{"data": Gate(gate="1", name="2")}]})
        self.rpc_server.run_as_thread()
        self.wait_for_rpc_server(self.rpc_server)

    def tearDown(self):
        self.rpc_server.shutdown()
        super().tearDown()

    def test_get(self):
        res = self.settings.get(Gate, "gate", "scope")
        self.assertEqual(self.settings_mocker.settings["gate/scope"], res)
        res = self.settings.get(Dict, "gate", "scope")
        self.assertEqual(self.settings_mocker.settings["gate/scope"].dict(), res)
        res = self.settings.get(List[Dict[str, Gate]], "test", "scope")
        self.assertEqual(self.settings_mocker.settings["test/scope"], res)

    def test_get_errors(self):
        with self.assertRaises(ValidationError):
            res = self.settings.get(List, "gate", "scope")

        self.settings_mocker.result_mode = SettingsRPCMocker.ResultMode.fail
        res = self.settings.get(Gate, "gate", "scope")
        self.assertIsNone(res)

        self.settings_mocker.result_mode = SettingsRPCMocker.ResultMode.error
        with self.assertRaises(RPCClient.ServerHandlerError):
            res = self.settings.get(Gate, "gate", "scope")
        self.settings_mocker.result_mode = SettingsRPCMocker.ResultMode.timeout
        with self.assertRaises(TimeoutError):
            res = self.settings.get(Gate, "gate", "scope")

    def test_get_cache(self):
        with freezegun.freeze_time("2020-01-01 00:00"):
            res = self.settings.get(Gate, "gate", "scope")
            self.assertEqual(self.settings_mocker.settings["gate/scope"], res)

            res = self.settings.get(List[Dict[str, Gate]], "test", "scope")
            self.assertEqual(self.settings_mocker.settings["test/scope"], res)

            old_res_gate = self.settings_mocker.settings["gate/scope"]
            old_res_test = self.settings_mocker.settings["test/scope"]
            self.settings_mocker.settings["gate/scope"] = Gate(gate="3", name="4")
            self.settings_mocker.settings["test/scope"] = [{"data": Gate(gate="3", name="4")}]
            res = self.settings.get(Gate, "gate", "scope")
            self.assertEqual(old_res_gate, res)  # should use from cache

            self.core.messages.dispatch("settings", SettingsChangedMessage(changed_keys=["gate/scope"]))  # clear cache
            res = self.settings.get(Gate, "gate", "scope")
            self.assertEqual(self.settings_mocker.settings["gate/scope"], res)

            # key2 cache should not be cleared
            res = self.settings.get(List[Dict[str, Gate]], "test", "scope")
            self.assertEqual(old_res_test, res)

        old_res_gate = self.settings_mocker.settings["gate/scope"]
        self.settings_mocker.settings["gate/scope"] = Gate(gate="5", name="6")
        with freezegun.freeze_time("2020-01-01 00:04"):
            # cache should not be expired yet
            res = self.settings.get(Gate, "gate", "scope")
            self.assertEqual(old_res_gate, res)  # should use from cache

        with freezegun.freeze_time("2020-01-01 00:06"):
            res = self.settings.get(Gate, "gate", "scope")
            self.assertEqual(self.settings_mocker.settings["gate/scope"], res)

            self.settings_mocker.settings["gate/scope"] = ["test"]
            res = self.settings.get(List[str], "gate", "scope")
            self.assertEqual(["test"], res)

    def test_get_no_exception(self):
        res = self.settings.get_no_exception(Gate, "gate", "scope")
        self.assertEqual(self.settings_mocker.settings["gate/scope"], res)

        self.assertIsNone(self.settings.get_no_exception(List, "key", "scope"))

        self.core.messages.dispatch("settings", SettingsChangedMessage(changed_keys=["gate/scope"]))  # clear cache
        self.settings_mocker.settings["gate/scope"] = None
        self.assertEqual(self.settings.get_no_exception(Any, "gate", "scope", "test"), "test")

        self.settings_mocker.settings["gate/scope"] = Gate(gate="1", name="2")
        self.settings_mocker.result_mode = SettingsRPCMocker.ResultMode.fail
        self.assertIsNone(self.settings.get_no_exception(Gate, "gate", "scope"))

        self.settings_mocker.result_mode = SettingsRPCMocker.ResultMode.error
        self.assertIsNone(self.settings.get_no_exception(Gate, "gate", "scope"))

        self.settings_mocker.result_mode = SettingsRPCMocker.ResultMode.timeout
        res = self.settings.get_no_exception(Gate, "gate", "scope", fallback={"fall": "back"})
        self.assertEqual({"fall": "back"}, res)

    def test_get_many(self):
        res = self.settings.get_many({"gate": Gate, "test": List[Dict[str, Gate]]}, "scope")
        self.assertEqual(self.settings_mocker.settings["gate/scope"], res["gate"])
        self.assertEqual(self.settings_mocker.settings["test/scope"], res["test"])

    def test_get_many_errors(self):
        self.settings_mocker.result_mode = SettingsRPCMocker.ResultMode.first_fail
        res = self.settings.get_many({"gate": Gate, "test": List[Dict[str, Gate]]}, "scope")
        self.assertEqual(None, res["gate"])
        self.assertEqual(self.settings_mocker.settings["test/scope"], res["test"])

        self.settings_mocker.result_mode = SettingsRPCMocker.ResultMode.error
        with self.assertRaises(RPCClient.ServerHandlerError):
            res = self.settings.get_many({"gate": Gate, "test": List[Dict[str, Gate]]}, "scope")
        self.settings_mocker.result_mode = SettingsRPCMocker.ResultMode.timeout
        with self.assertRaises(TimeoutError):
            res = self.settings.get_many({"gate": Gate, "test": List[Dict[str, Gate]]}, "scope")

    def test_get_many_cache(self):
        self.settings_mocker.settings.update({"gate/scope2": Gate(gate="1", name="2"),
                                              "test/scope2": [{"data": Gate(gate="1", name="2")}]})
        with freezegun.freeze_time("2020-01-01 00:00"):
            res = self.settings.get_many({"gate": Gate, "test": List[Dict[str, Gate]]}, "scope")
            res = self.settings.get_many({"gate": Gate, "test": List[Dict[str, Gate]]}, "scope2")

            # from cache
            old_settings = self.settings_mocker.settings.copy()
            self.settings_mocker.settings.update({"gate/scope": Gate(gate="3", name="4"),
                                                  "test/scope": [{"data": Gate(gate="3", name="4")}]})
            self.settings_mocker.settings.update({"gate/scope2": Gate(gate="3", name="4"),
                                                  "test/scope2": [{"data": Gate(gate="3", name="4")}]})
            res = self.settings.get_many({"gate": Gate, "test": List[Dict[str, Gate]]}, "scope")
            self.assertEqual(old_settings["gate/scope"], res["gate"])
            self.assertEqual(old_settings["test/scope"], res["test"])

            self.core.messages.dispatch("settings", SettingsChangedMessage(changed_keys=["test/scope"]))  # clear cache
            # gate still from cache
            res = self.settings.get_many({"gate": Gate}, "scope")
            self.assertEqual(old_settings["gate/scope"], res["gate"])
            # scope2 still from cache
            res = self.settings.get_many({"gate": Gate, "test": List[Dict[str, Gate]]}, "scope2")
            self.assertEqual(old_settings["gate/scope2"], res["gate"])
            self.assertEqual(old_settings["test/scope2"], res["test"])
            # scope "scope": all field new
            res = self.settings.get_many({"gate": Gate, "test": List[Dict[str, Gate]]}, "scope")
            self.assertEqual(self.settings_mocker.settings["gate/scope"], res["gate"])
            self.assertEqual(self.settings_mocker.settings["test/scope"], res["test"])

        old_settings = self.settings_mocker.settings.copy()
        self.settings_mocker.settings.update({"gate/scope": Gate(gate="5", name="6"),
                                              "test/scope": [{"data": Gate(gate="5", name="6")}]})
        with freezegun.freeze_time("2020-01-01 00:04"):
            # cache should not be expired yet
            res = self.settings.get_many({"gate": Gate, "test": List[Dict[str, Gate]]}, "scope")
            self.assertEqual(old_settings["gate/scope"], res["gate"])
            self.assertEqual(old_settings["test/scope"], res["test"])
            self.settings._cached_values["gate/scope"].expires_at = time.time() + 1000

        with freezegun.freeze_time("2020-01-01 00:06"):
            # cache should not be expired for req
            res = self.settings.get_many({"gate": Gate}, "scope")
            self.assertEqual(old_settings["gate/scope"], res["gate"])

            # cache should be expired
            res = self.settings.get_many({"gate": Gate, "test": List[Dict[str, Gate]]}, "scope")
            self.assertEqual(self.settings_mocker.settings["gate/scope"], res["gate"])
            self.assertEqual(self.settings_mocker.settings["test/scope"], res["test"])

    def test_get_many_no_exception(self):
        res = self.settings.get_many_no_exception({"gate": Gate, "test": List[Dict[str, Gate]]}, "scope")
        self.assertEqual(self.settings_mocker.settings["gate/scope"], res["gate"])
        self.assertEqual(self.settings_mocker.settings["test/scope"], res["test"])
        
        self.assertEqual(self.settings.get_many_no_exception({"gate": List, "test": int}, "scope", {"test": 1}),
                         {"gate": None, "test": 1})
        self.settings_mocker.result_mode = SettingsRPCMocker.ResultMode.fail
        self.assertEqual(self.settings.get_many_no_exception({"gate": int, "test": int}, "scope", {"gate": 1}),
                         {"gate": 1, "test": None})

        self.res = "error"
        self.assertEqual(self.settings.get_many_no_exception({"gate": int, "test": int}, "scope"),
                         {"gate": None, "test": None})
        self.res = "wrong"
        self.assertEqual(self.settings.get_many_no_exception({"gate": int, "test": int}, "scope"),
                         {"gate": None, "test": None})
        self.res = "timeout"
        self.assertEqual(self.settings.get_many_no_exception({"gate": int, "test": int}, "scope",
                                                             {"test": 1, "bull": "shit"}), {"gate": None, "test": 1})
