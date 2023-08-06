from io import IOBase
from semantha_sdk.api.semantha_endpoint import SemanthaAPIEndpoint
from semantha_sdk.model.semantic_model import SemanticModel, SemanticModelSchema
from semantha_sdk.rest.rest_client import MediaType
from semantha_sdk.rest.rest_client import RestClient


class ModelinstancesEndpoint(SemanthaAPIEndpoint):
    """ author semantha, this is a generated class do not change manually! """

    @property
    def _endpoint(self) -> str:
        return self._parent_endpoint + "/modelinstances"

    def post(self
        , file: IOBase = None
        , documentextractor: str = None
        , applymatchersfordocumentextractor: bool = None
        , withimages: bool = None
        , withdocument: bool = None
        , withadditionalroots: bool = None
        , documenttype: str = None
        , uilanguage: str = None
        ) -> SemanticModel:
        """
        Extract semantic model for a list of documents
        Args:
            file (IOBase): Input document (left document).
            documentextractor (str): The document extractor you want to be considered.
            applymatchersfordocumentextractor (bool): 
            
        """
        q_params = {}
        if withimages is not None:
            q_params["withimages"] = withimages
        if withdocument is not None:
            q_params["withdocument"] = withdocument
        if withadditionalroots is not None:
            q_params["withadditionalroots"] = withadditionalroots
        if documenttype is not None:
            q_params["documenttype"] = documenttype
        if uilanguage is not None:
            q_params["uilanguage"] = uilanguage
        response = self._session.post(
            url=self._endpoint,
            
            body={
            
                "file": file,
                "documentextractor": documentextractor,
                "applymatchersfordocumentextractor": applymatchersfordocumentextractor
            },
            
            headers=RestClient.to_header(MediaType.JSON),
            q_params=q_params
        ).execute()
        return response.to(SemanticModelSchema)


    def __init__(self, session: RestClient, parent_endpoint: str) -> None:
        super().__init__(session, parent_endpoint)


