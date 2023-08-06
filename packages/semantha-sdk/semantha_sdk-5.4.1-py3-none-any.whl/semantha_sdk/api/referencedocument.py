from semantha_sdk.api.paragraphs import ParagraphsEndpoint
from semantha_sdk.api.semantha_endpoint import SemanthaAPIEndpoint
from semantha_sdk.api.sentences import SentencesEndpoint
from semantha_sdk.model.document import Document, DocumentSchema
from semantha_sdk.model.document_information import DocumentInformation, DocumentInformationSchema
from semantha_sdk.rest.rest_client import RestClient


class ReferencedocumentEndpoint(SemanthaAPIEndpoint):
    """ author semantha, this is a generated class do not change manually! """

    @property
    def _endpoint(self) -> str:
        return self._parent_endpoint + f"/{self._documentid}"

    def get(self
        , querybyname: bool = None
        ) -> Document:
        """
         
        Args:
            querybyname (bool): Select if you want forward a name instead of an ID.
            
        """
        q_params = {}
        if querybyname is not None:
            q_params["querybyname"] = querybyname
        return self._session.get(self._endpoint, q_params=q_params).execute().to(DocumentSchema)

    def patch(self, documentinformation: DocumentInformation) -> DocumentInformation:
        """
        
        """
        return self._session.patch(
            url=self._endpoint,
            json=DocumentInformationSchema().dump(documentinformation)
        ).execute().to(DocumentInformationSchema)


    def delete(self) -> None:
        """
        
        """
        self._session.delete(self._endpoint).execute()

    def __init__(self, session: RestClient, parent_endpoint: str, documentid: str) -> None:
        super().__init__(session, parent_endpoint)
        self._documentid=documentid
        self.__paragraphs = ParagraphsEndpoint(session, self._endpoint)
        self.__sentences = SentencesEndpoint(session, self._endpoint)


    @property
    def paragraphs(self) -> ParagraphsEndpoint:
        return self.__paragraphs


    @property
    def sentences(self) -> SentencesEndpoint:
        return self.__sentences

