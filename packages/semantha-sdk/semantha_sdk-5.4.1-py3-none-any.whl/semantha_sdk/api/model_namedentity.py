from semantha_sdk.api.semantha_endpoint import SemanthaAPIEndpoint
from semantha_sdk.model.named_entity import NamedEntity, NamedEntitySchema
from semantha_sdk.rest.rest_client import RestClient


class ModelNamedentityEndpoint(SemanthaAPIEndpoint):
    """ author semantha, this is a generated class do not change manually! """

    @property
    def _endpoint(self) -> str:
        return self._parent_endpoint + f"/{self._id}"

    def get(self
        ) -> NamedEntity:
        """
        Get a custom entity by id 
        Args:
            
        """
        q_params = {}
        return self._session.get(self._endpoint, q_params=q_params).execute().to(NamedEntitySchema)

    def put(self, namedentity: NamedEntity) -> NamedEntity:
        """
        Update a custom entity by id
        """
        return self._session.put(
            url=self._endpoint,
            json=NamedEntitySchema().dump(namedentity)
        ).execute().to(NamedEntitySchema)


    def delete(self) -> None:
        """
        Delete a custom entity by id
        """
        self._session.delete(self._endpoint).execute()

    def __init__(self, session: RestClient, parent_endpoint: str, id: str) -> None:
        super().__init__(session, parent_endpoint)
        self._id=id

