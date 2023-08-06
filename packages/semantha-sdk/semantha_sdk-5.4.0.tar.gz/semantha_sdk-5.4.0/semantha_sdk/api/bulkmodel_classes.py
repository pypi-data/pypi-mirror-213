from semantha_sdk.api.bulkmodel_class import BulkmodelClassEndpoint
from semantha_sdk.api.semantha_endpoint import SemanthaAPIEndpoint
from semantha_sdk.model.class_bulk import ClassBulk, ClassBulkSchema
from semantha_sdk.rest.rest_client import MediaType
from semantha_sdk.rest.rest_client import RestClient
from typing import List


class BulkmodelClassesEndpoint(SemanthaAPIEndpoint):
    """ author semantha, this is a generated class do not change manually! """

    @property
    def _endpoint(self) -> str:
        return self._parent_endpoint + "/classes"

    def get(self
        ) -> List[ClassBulk]:
        """
        Get all classes
        This is the quiet version of  'get /api/domains/{domainname}/classes' 
        Args:
            
        """
        q_params = {}
        return self._session.get(self._endpoint, q_params=q_params).execute().to(ClassBulkSchema)

    def post(self
        , body: List[ClassBulk] = None
        ) -> None:
        """
        Create one or more classes
        This is the quiet version of  'post /api/domains/{domainname}/classes'
        Args:
            body (List[ClassBulk]): 
            
        """
        q_params = {}
        response = self._session.post(
            url=self._endpoint,
            json=ClassBulkSchema().dump(body),
            headers=RestClient.to_header(MediaType.JSON),
            q_params=q_params
        )


    def __init__(self, session: RestClient, parent_endpoint: str) -> None:
        super().__init__(session, parent_endpoint)



    def __call__(self, classid: str) -> BulkmodelClassEndpoint:
        return BulkmodelClassEndpoint(self._session, self._endpoint, classid)


