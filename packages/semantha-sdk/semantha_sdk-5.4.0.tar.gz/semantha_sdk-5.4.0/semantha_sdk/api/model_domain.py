from io import IOBase
from semantha_sdk.api.model_boostwords import ModelBoostwordsEndpoint
from semantha_sdk.api.model_namedentities import ModelNamedentitiesEndpoint
from semantha_sdk.api.model_stopwords import ModelStopwordsEndpoint
from semantha_sdk.api.model_synonyms import ModelSynonymsEndpoint
from semantha_sdk.api.semantha_endpoint import SemanthaAPIEndpoint
from semantha_sdk.rest.rest_client import RestClient


class ModelDomainEndpoint(SemanthaAPIEndpoint):
    """ author semantha, this is a generated class do not change manually! """

    @property
    def _endpoint(self) -> str:
        return self._parent_endpoint + f"/{self._domainname}"

    def get(self
        ) -> IOBase:
        """
        Get a domain by domainname 
        Args:
            
        """
        q_params = {}
        return self._session.get(self._endpoint, q_params=q_params)

    def patch(self, iobase: IOBase) -> IOBase:
        """
        Update a domain by domainname
        """
        return self._session.patch(
            url=self._endpoint,
            json=iobase
        )


    def __init__(self, session: RestClient, parent_endpoint: str, domainname: str) -> None:
        super().__init__(session, parent_endpoint)
        self._domainname=domainname
        self.__boostwords = ModelBoostwordsEndpoint(session, self._endpoint)
        self.__namedentities = ModelNamedentitiesEndpoint(session, self._endpoint)
        self.__stopwords = ModelStopwordsEndpoint(session, self._endpoint)
        self.__synonyms = ModelSynonymsEndpoint(session, self._endpoint)


    @property
    def boostwords(self) -> ModelBoostwordsEndpoint:
        return self.__boostwords


    @property
    def namedentities(self) -> ModelNamedentitiesEndpoint:
        return self.__namedentities


    @property
    def stopwords(self) -> ModelStopwordsEndpoint:
        return self.__stopwords


    @property
    def synonyms(self) -> ModelSynonymsEndpoint:
        return self.__synonyms

