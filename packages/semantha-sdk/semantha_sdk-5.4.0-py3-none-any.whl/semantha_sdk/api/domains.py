from semantha_sdk.api.domain import DomainEndpoint
from semantha_sdk.api.semantha_endpoint import SemanthaAPIEndpoint
from semantha_sdk.model.domain import Domain, DomainSchema
from semantha_sdk.rest.rest_client import RestClient
from typing import List


class DomainsEndpoint(SemanthaAPIEndpoint):
    """ author semantha, this is a generated class do not change manually! """

    @property
    def _endpoint(self) -> str:
        return self._parent_endpoint + "/domains"

    def get(self
        ) -> List[Domain]:
        """
        Get all domains 
        Args:
            
        """
        q_params = {}
        return self._session.get(self._endpoint, q_params=q_params).execute().to(DomainSchema)


    def __init__(self, session: RestClient, parent_endpoint: str) -> None:
        super().__init__(session, parent_endpoint)



    def __call__(self, domainname: str) -> DomainEndpoint:
        return DomainEndpoint(self._session, self._endpoint, domainname)


