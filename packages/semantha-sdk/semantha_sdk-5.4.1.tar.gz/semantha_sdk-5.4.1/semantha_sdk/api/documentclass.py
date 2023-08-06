from semantha_sdk.api.semantha_endpoint import SemanthaAPIEndpoint
from semantha_sdk.model.document_class import DocumentClass, DocumentClassSchema
from semantha_sdk.rest.rest_client import RestClient


class DocumentclassEndpoint(SemanthaAPIEndpoint):
    """ author semantha, this is a generated class do not change manually! """

    @property
    def _endpoint(self) -> str:
        return self._parent_endpoint + f"/{self._id}"

    def get(self
        ) -> DocumentClass:
        """
        Get a class identified by id and all its subclasses 
        Args:
            
        """
        q_params = {}
        return self._session.get(self._endpoint, q_params=q_params).execute().to(DocumentClassSchema)

    def put(self, documentclass: DocumentClass) -> DocumentClass:
        """
        Rename a document class identified by its id
        """
        return self._session.put(
            url=self._endpoint,
            json=DocumentClassSchema().dump(documentclass)
        ).execute().to(DocumentClassSchema)


    def delete(self) -> None:
        """
        Delete a document class identified by id
        """
        self._session.delete(self._endpoint).execute()

    def __init__(self, session: RestClient, parent_endpoint: str, id: str) -> None:
        super().__init__(session, parent_endpoint)
        self._id=id

