from looqbox.flows.base_flow import BaseFlow
from looqbox.integration.integration_links import _test_connection


class TestConnectionFlow(BaseFlow):
    def test_connection(self) -> None:

        conn_name = self.data.get("connectionName",  next(iter(self.data)))
        is_connection_working = _test_connection(conn_name)
        with open(self.output_json_file, "w") as result_file:
            result_file.write(is_connection_working)
            result_file.close()
        
    def run(self):
        steps = [
            self.read_response_parameters,
            self.response_enricher,
            self.define_global_variables,
            self.test_connection
        ]
        self.run_steps(steps)
