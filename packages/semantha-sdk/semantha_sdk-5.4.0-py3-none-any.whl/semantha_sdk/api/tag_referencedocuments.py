from semantha_sdk.api.semantha_endpoint import SemanthaAPIEndpoint
from semantha_sdk.model.document_information import DocumentInformation, DocumentInformationSchema
from semantha_sdk.rest.rest_client import RestClient
from typing import List


class TagReferencedocumentsEndpoint(SemanthaAPIEndpoint):
    """ author semantha, this is a generated class do not change manually! """

    @property
    def _endpoint(self) -> str:
        return self._parent_endpoint + "/referencedocuments"

    def get(self
        ) -> List[DocumentInformation]:
        """
        Get all reference documents with a specific tag 
        Args:
            
        """
        q_params = {}
        return self._session.get(self._endpoint, q_params=q_params).execute().to(DocumentInformationSchema)


    def delete(self) -> None:
        """
        Delete reference documents with a specific tag
        """
        self._session.delete(self._endpoint).execute()

    def __init__(self, session: RestClient, parent_endpoint: str) -> None:
        super().__init__(session, parent_endpoint)


