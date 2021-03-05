from validator import GeoValidator
from rdflib import Namespace, Graph
from pyshacl import rdfutil
from datagraph import DataGraph
from utils import DATA, GEO, ArcGIS, PROCESS
import pytest

validator = GeoValidator()
# ontologies
qudt = '../../ont/QUDT ALL UNITS.ttl'
data = '../../ont/data.owl'
dcat = '../../ont/dcat2.ttl'
geo_file = '../../ont/geosparql_vocab_all.rdf'
sf_file = '../../ont/sf.rdf'
process_file = '../../ont/gis-process.owl'
geo = rdfutil.load_from_source(geo_file)
ont = validator.read_graphs(geo_file, data, sf_file, dcat, qudt)
ont2 = validator.read_graphs(data, dcat, process_file)

case_data = './pygeoc_data.ttl'
case_shape = './pygeoc_shapes.ttl'
dg = DataGraph()


class TestPyGeoc(object):
    d_graph = rdfutil.load_from_source(case_data)

    @pytest.mark.skip()
    def test_watershedDelineation(self):
        s_graph = rdfutil.load_from_source(case_shape)
        # not support rules
        conforms, results_graph, results_text = validator.validate_data(self.d_graph, s_graph, ont)
        print()
        print(conforms)
        print(results_text)
        dg.graph_2_file(results_graph, 'case3_report.ttl')
        print('DONE')

    case_rules = rdfutil.load_from_source('./pygeoc_rules.ttl')

    def test_rules(self):
        conforms, expanded_graph = validator.infer_with_extended_graph(self.d_graph, self.case_rules)
        print(conforms)
        dg.graph_2_file(expanded_graph, 'case3_rules_results.ttl')


if __name__ == "__main__":
    # pytest.main('[test_pygeoc::TestPyGeoc::test_watershedDelineation]')
    pytest.main('[test_pygeoc::TestPyGeoc::test_rules]')
