![](https://www.semantha.de/wp-content/uploads/semantha-inverted.svg)

# semantha® SDK

The semantha SDK is a high-level REST client to access the [semantha](http://semantha.ai) API.
The SDK is still under development.
An overview of the current progress (i.e. implemented and tested resources and endpoints) may be found at the end of
this document (State of Development).
The semantha SDK is compatible with python >= 3.8.

## Design guideline/idea
Every api call can easily be translated into a python sdk call:
`GET /api/info -> api.info.get()`
The SDK offers type hints and doc strings for services, parameters, input types and return types within your IDE.

### Disclaimer

**IMPORTANT:** The SDK is still under development and interfaces may change at any time without notice.
Use with caution and on own risk.

## Update Notes

### Version 5.4.0
Added **new** service: 
- **/api/domains/{domainname}/summarizations** which generations a summarization for a given list of texts and a given topic.

Added support for **existing** services: 
- /api/model/domains/{domainname}/boostwords/{id}
- /api/model/domains/{domainname}/namedentities
- /api/model/domains/{domainname}/namedentities/{id}
- /api/model/domains/{domainname}/stopwords
- /api/model/domains/{domainname}/stopwords/{id}
- /api/model/domains/{domainname}/synonyms/{id}

### Version 5.3.0

Added new service: **/api/domains/{domainid}/answers** with retrieval augemented answer generation based on your library entries.
Added new parameter on /modelinstances

### Version 5.2.0

The SDK is now automatically generated from our openapi.json specification. It covers 71/169 (=42%) of all available services. Many class names and package names have been changed.

### Version 4.5.0
Major restructuring of the SDK.
All sub-resources are directly accessible (instead of invoking getters).
That also means that (except for a few) all functions are plain get/post/delete/put/patch.
For example, in Versions < 4.5.0 a domain resource was fetched using `semantha_sdk.domains.get_one("domain_name")`.
Starting with 4.5.0 it is `semantha_sdk.domains("domain_name")`.
That also means that get/post/put/patch functions return semantha model objects (and never resources), which makes usage more consistent.

### Access

To access semantha's API you will need an API and a server url.
Both can be requested via [this contact form](https://www.semantha.de/request/).

## Example Usage

### Authentication with key

```python
import semantha_sdk
api = semantha_sdk.login(server_url="<semantha server URL>", key="<your key>")
print("Talking to semantha server: " + api.info.get().version)
```

### Authentication with key file

```python
import semantha_sdk
api = semantha_sdk.login(server_url="<semantha server URL>", key_file="<path to your key file (json format)>")
# end-points (resp. resources) can be used like objects
my_domain = api.domains("my_domain")
# they may have sub-resources, which can be retrieved as objects as well
reference_documents = my_domain.referencedocuments
# GET all reference documents
print("Library contains "+ len(reference_documents.get()) + " entries")
```

Example key file in json format:

```json
{ "API_Key" : "<your key>" }
```

### CRUD on End-points

```python
# CRUD operations are functions
domain_settings = my_domain.settings.get()
#Warning: this deletes ALL reference documents/library entries
my_domain.referencedocuments.delete() 
```

### Function Return Types & semantha Data Model

```python
# some functions only return None, e.g.
my_domain.referencedocuments.delete() # returns NoneType

# others return built in types, e.g
roles_list = currentuser.roles.get() # returns List[str]

# but most return objects of the semantha Data Model
# (all returned objects are instances of frozen dataclasses)
settings = my_domain.settings.get() # returns instance of Settings
# attributes can be accessed as properties, e.g.
settings.enable_tagging # returns true or false
# Data Model objects may be complex
document = my_domain.references.post(file=a, referencedocument=b) # returns instance of Document
# the following returns the similarity value of the first references of the first sentence of the
# the first paragraph on the first page of the document (if a reference was found for this sentence)
similarity = pages[0].contents[0].paragraphs[0].references[0].similarity # returns float
```

## State of Development

The following resources and end-points are fully functional and (partially) tested:

- [x] **/bulk** -> BulkEndpoint
- [x] **/bulk/domains** -> BulkDomainsEndpoint
- [x] **/bulk/domains/{domainname}** -> BulkdomainsDomainEndpoint
- [x] **/bulk/domains/{domainname}/documentclasses** -> BulkdomainsDocumentclassesEndpoint
    - [x] **GET** -> List[DocumentClassBulk]
    - [x] **POST** -> None
- [x] **/bulk/domains/{domainname}/referencedocuments** -> BulkdomainsReferencedocumentsEndpoint
    - [x] **GET** -> List[Document]
    - [x] **POST** -> None
    - [x] **DELETE** -> 
- [x] **/bulk/domains/{domainname}/references** -> BulkdomainsReferencesEndpoint
    - [x] **POST** -> List[Document]
- [x] **/bulk/model** -> BulkModelEndpoint
- [x] **/bulk/model/domains** -> BulkmodelDomainsEndpoint
- [x] **/bulk/model/domains/{domainname}** -> BulkmodelDomainEndpoint
- [x] **/bulk/model/domains/{domainname}/boostwords** -> BulkmodelBoostwordsEndpoint
    - [x] **POST** -> None
- [x] **/bulk/model/domains/{domainname}/classes** -> BulkmodelClassesEndpoint
    - [x] **GET** -> List[ClassBulk]
    - [x] **POST** -> None
- [x] **/bulk/model/domains/{domainname}/classes/{classid}** -> BulkmodelClassEndpoint
- [x] **/bulk/model/domains/{domainname}/classes/{classid}/instances** -> BulkmodelclassInstancesEndpoint
    - [x] **GET** -> List[Instance]
- [x] **/bulk/model/domains/{domainname}/dataproperties** -> BulkmodelDatapropertiesEndpoint
    - [x] **GET** -> List[DataProperty]
    - [x] **POST** -> None
- [x] **/bulk/model/domains/{domainname}/instances** -> BulkmodelInstancesEndpoint
    - [x] **GET** -> List[Instance]
    - [x] **POST** -> None
- [x] **/bulk/model/domains/{domainname}/metadata** -> BulkmodelMetadataEndpoint
    - [x] **GET** -> List[Metadata]
    - [x] **POST** -> None
- [x] **/bulk/model/domains/{domainname}/namedentities** -> BulkmodelNamedentitiesEndpoint
    - [x] **POST** -> None
- [ ] **/bulk/model/domains/{domainname}/rules** 
- [x] **/bulk/model/domains/{domainname}/stopwords** -> BulkmodelStopwordsEndpoint
    - [x] **POST** -> None
- [x] **/bulk/model/domains/{domainname}/synonyms** -> BulkmodelSynonymsEndpoint
    - [x] **POST** -> None
- [x] **/currentuser** -> CurrentuserEndpoint
    - [x] **GET** -> CurrentUser
- [x] **/currentuser/roles** -> RolesEndpoint
    - [x] **GET** -> List[str]
- [x] **/diff** -> DiffEndpoint
    - [x] **POST** -> List[Difference]
- [x] **/domains** -> DomainsEndpoint
    - [x] **GET** -> List[Domain]
- [x] **/domains/{domainname}** -> DomainEndpoint
    - [x] **GET** -> Domain
- [x] **/domains/{domainname}/answers** -> AnswersEndpoint
    - [x] **POST** -> Answer
- [x] **/domains/{domainname}/documentannotations** -> DocumentannotationsEndpoint
    - [x] **POST** -> IOBase
- [x] **/domains/{domainname}/documentclasses** -> DocumentclassesEndpoint
    - [x] **GET** -> List[DocumentClass]
    - [x] **POST** -> DocumentClass
    - [x] **DELETE** -> 
- [x] **/domains/{domainname}/documentclasses/{id}** -> DocumentclassEndpoint
    - [x] **GET** -> DocumentClass
    - [x] **DELETE** -> 
    - [x] **PUT** -> DocumentClass
- [ ] **/domains/{domainname}/documentclasses/{id}/documentclasses** 
- [ ] **/domains/{domainname}/documentclasses/{id}/referencedocuments** 
- [x] **/domains/{domainname}/documentcomparisons** -> DocumentcomparisonsEndpoint
    - [x] **POST** -> IOBase
- [x] **/domains/{domainname}/documents** -> DocumentsEndpoint
    - [x] **POST** -> List[Document]
- [x] **/domains/{domainname}/modelclasses** -> ModelclassesEndpoint
    - [x] **GET** -> List[ModelClass]
- [x] **/domains/{domainname}/modelinstances** -> ModelinstancesEndpoint
    - [x] **POST** -> SemanticModel
- [x] **/domains/{domainname}/referencedocuments** -> ReferencedocumentsEndpoint
    - [x] **GET** -> ReferenceDocumentsResponseContainer
    - [x] **POST** -> List[DocumentInformation]
    - [x] **DELETE** -> 
- [x] **/domains/{domainname}/referencedocuments/clusters** -> ClustersEndpoint
    - [x] **GET** -> SmartClusterResponseContainer
    - [x] **PUT** -> SmartClusterResponseContainer
- [x] **/domains/{domainname}/referencedocuments/namedentities** -> NamedentitiesEndpoint
    - [x] **GET** -> List[DocumentNamedEntity]
- [x] **/domains/{domainname}/referencedocuments/statistic** -> StatisticEndpoint
    - [x] **GET** -> Statistic
- [x] **/domains/{domainname}/referencedocuments/{documentid}** -> ReferencedocumentEndpoint
    - [x] **GET** -> Document
    - [x] **DELETE** -> 
    - [x] **PATCH** -> DocumentInformation
- [x] **/domains/{domainname}/referencedocuments/{documentid}/paragraphs** -> ParagraphsEndpoint
- [x] **/domains/{domainname}/referencedocuments/{documentid}/paragraphs/{id}** -> ParagraphEndpoint
    - [x] **GET** -> Paragraph
    - [x] **DELETE** -> 
    - [x] **PATCH** -> Paragraph
- [x] **/domains/{domainname}/referencedocuments/{documentid}/sentences** -> SentencesEndpoint
- [x] **/domains/{domainname}/referencedocuments/{documentid}/sentences/{id}** -> SentenceEndpoint
    - [x] **GET** -> Sentence
- [x] **/domains/{domainname}/references** -> ReferencesEndpoint
    - [x] **POST** -> Document
- [x] **/domains/{domainname}/settings** -> SettingsEndpoint
    - [x] **GET** -> Settings
    - [x] **PATCH** -> Settings
- [x] **/domains/{domainname}/similaritymatrix** -> SimilaritymatrixEndpoint
    - [x] **POST** -> List[MatrixRow]
- [x] **/domains/{domainname}/similaritymatrix/cluster** -> SimilaritymatrixClusterEndpoint
    - [x] **POST** -> List[MatrixRow]
- [x] **/domains/{domainname}/summarizations** -> SummarizationsEndpoint
    - [x] **POST** -> Any
- [x] **/domains/{domainname}/tags** -> TagsEndpoint
    - [x] **GET** -> List[str]
- [x] **/domains/{domainname}/tags/{tagname}** -> TagEndpoint
- [x] **/domains/{domainname}/tags/{tagname}/referencedocuments** -> TagReferencedocumentsEndpoint
    - [x] **GET** -> List[DocumentInformation]
    - [x] **DELETE** -> 
- [x] **/domains/{domainname}/validation** -> ValidationEndpoint
    - [x] **POST** -> SemanticModel
- [x] **/info** -> InfoEndpoint
    - [x] **GET** -> Info
- [x] **/languages** -> LanguagesEndpoint
    - [x] **POST** -> LanguageDetection
- [x] **/model** -> ModelEndpoint
- [x] **/model/datatypes** -> ModelDatatypesEndpoint
    - [x] **GET** -> List[str]
- [x] **/model/domains** -> ModelDomainsEndpoint
- [x] **/model/domains/{domainname}** -> ModelDomainEndpoint
    - [x] **GET** -> IOBase
    - [x] **PATCH** -> IOBase
- [ ] **/model/domains/{domainname}/attributes** 
- [ ] **/model/domains/{domainname}/backups** 
- [x] **/model/domains/{domainname}/boostwords** -> ModelBoostwordsEndpoint
    - [x] **GET** -> List[BoostWord]
    - [x] **POST** -> BoostWord
    - [x] **DELETE** -> 
- [x] **/model/domains/{domainname}/boostwords/{id}** -> ModelBoostwordEndpoint
    - [x] **GET** -> BoostWord
    - [x] **DELETE** -> 
    - [x] **PUT** -> BoostWord
- [ ] **/model/domains/{domainname}/classes** 
- [ ] **/model/domains/{domainname}/classes/{classid}** 
- [ ] **/model/domains/{domainname}/classes/{classid}/attributes** 
- [ ] **/model/domains/{domainname}/classes/{classid}/attributes/{id}** 
- [ ] **/model/domains/{domainname}/classes/{classid}/instances** 
- [ ] **/model/domains/{domainname}/dataproperties** 
- [ ] **/model/domains/{domainname}/dataproperties/{id}** 
- [ ] **/model/domains/{domainname}/extractorclasses** 
- [ ] **/model/domains/{domainname}/extractorclasses/{id}** 
- [ ] **/model/domains/{domainname}/extractorclasses/{id}/extractorclasses** 
- [ ] **/model/domains/{domainname}/extractors** 
- [ ] **/model/domains/{domainname}/extractortables** 
- [ ] **/model/domains/{domainname}/extractortables/{id}** 
- [ ] **/model/domains/{domainname}/formatters** 
- [ ] **/model/domains/{domainname}/instances** 
- [ ] **/model/domains/{domainname}/instances/{id}** 
- [ ] **/model/domains/{domainname}/metadata** 
- [ ] **/model/domains/{domainname}/metadata/{id}** 
- [x] **/model/domains/{domainname}/namedentities** -> ModelNamedentitiesEndpoint
    - [x] **GET** -> List[NamedEntity]
    - [x] **POST** -> NamedEntity
    - [x] **DELETE** -> 
- [x] **/model/domains/{domainname}/namedentities/{id}** -> ModelNamedentityEndpoint
    - [x] **GET** -> NamedEntity
    - [x] **DELETE** -> 
    - [x] **PUT** -> NamedEntity
- [ ] **/model/domains/{domainname}/objectproperties** 
- [ ] **/model/domains/{domainname}/regexes** 
- [ ] **/model/domains/{domainname}/regexes/{id}** 
- [ ] **/model/domains/{domainname}/relations** 
- [ ] **/model/domains/{domainname}/relations/{id}** 
- [ ] **/model/domains/{domainname}/rulefunctions** 
- [ ] **/model/domains/{domainname}/rules** 
- [ ] **/model/domains/{domainname}/rules/{id}** 
- [x] **/model/domains/{domainname}/stopwords** -> ModelStopwordsEndpoint
    - [x] **GET** -> List[StopWord]
    - [x] **POST** -> StopWord
    - [x] **DELETE** -> 
- [x] **/model/domains/{domainname}/stopwords/{id}** -> ModelStopwordEndpoint
    - [x] **GET** -> StopWord
    - [x] **DELETE** -> 
    - [x] **PUT** -> StopWord
- [x] **/model/domains/{domainname}/synonyms** -> ModelSynonymsEndpoint
    - [x] **GET** -> List[Synonym]
    - [x] **POST** -> Synonym
    - [x] **DELETE** -> 
- [x] **/model/domains/{domainname}/synonyms/{id}** -> ModelSynonymEndpoint
    - [x] **GET** -> Synonym
    - [x] **DELETE** -> 
    - [x] **PUT** -> Synonym
- [x] **/model/extractortypes** -> ModelExtractortypesEndpoint
    - [x] **GET** -> List[str]
- [x] **/model/metadatatypes** -> ModelMetadatatypesEndpoint
    - [x] **GET** -> List[str]
