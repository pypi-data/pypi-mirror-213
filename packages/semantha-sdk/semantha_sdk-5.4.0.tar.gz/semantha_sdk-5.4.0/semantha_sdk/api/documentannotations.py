from io import IOBase
from semantha_sdk.api.semantha_endpoint import SemanthaAPIEndpoint
from semantha_sdk.model.document import Document, DocumentSchema
from semantha_sdk.rest.rest_client import MediaType
from semantha_sdk.rest.rest_client import RestClient


class DocumentannotationsEndpoint(SemanthaAPIEndpoint):
    """ author semantha, this is a generated class do not change manually! """

    @property
    def _endpoint(self) -> str:
        return self._parent_endpoint + "/documentannotations"

    def post(self
        , file: IOBase = None
        , document: Document = None
        , similaritythreshold: float = None
        , synonymousthreshold: float = None
        , marknomatch: bool = None
        , withreferencetext: bool = None
        ) -> IOBase:
        """
        Download the original input document with the referenced document/library matches as annotated comments
        Args:
            file (IOBase): Input document (left document).
            document (Document): 
            similaritythreshold (float): Threshold for the similarity score. semantha will not deliver results with a sentence score lower than the threshold.
        In general, the higher the threshold, the more precise the results.
            synonymousthreshold (float): Threshold for good matches.
            marknomatch (bool): Marks the paragraphs that have not matched
            withreferencetext (bool): Provide the reference text in the result JSON. If set to false, you have to query the library to resolve the references yourself.
            
        """
        q_params = {}
        response = self._session.post(
            url=self._endpoint,
            
            body={
            
                "file": file,
                "document": document,
                "similaritythreshold": similaritythreshold,
                "synonymousthreshold": synonymousthreshold,
                "marknomatch": marknomatch,
                "withreferencetext": withreferencetext
            },
            
            headers=RestClient.to_header(MediaType.XLSX),
            q_params=q_params
        )


    def __init__(self, session: RestClient, parent_endpoint: str) -> None:
        super().__init__(session, parent_endpoint)


