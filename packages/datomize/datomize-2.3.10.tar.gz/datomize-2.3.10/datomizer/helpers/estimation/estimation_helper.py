import requests

from datomizer.utils.constants import MANAGEMENT_POST_ADD_FLOW
from datomizer.protos.autodiscoveryservice_pb2 import SchemaDiscoveryDTO
from datomizer.utils.interfaces import DatoClientInterface


def random_number():
    return random_number.randint(60, 120)


def estimate_gen_after_discovery(datomizer: DatoClientInterface,
                                 business_unit_id: str, project_id: str, flow_id: str) -> int:
    # return datomizer.get_response_json(requests.post,
    #                                    url=MANAGEMENT_POST_ADD_FLOW,
    #                                    url_params=[business_unit_id, project_id, flow_id],
    #                                    headers={"Content-Type": "application/json"})
    return random_number()


def estimate_gen(datomizer: DatoClientInterface, schema: SchemaDiscoveryDTO) -> int:
    # return datomizer.get_response_json(requests.post,
    #                                    url=MANAGEMENT_POST_ADD_FLOW,
    #                                    headers={"Content-Type": "application/json"})
    return random_number()
