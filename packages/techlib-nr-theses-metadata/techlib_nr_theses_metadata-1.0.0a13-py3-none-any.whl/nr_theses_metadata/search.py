from nr_common_metadata.search import NRRecordsSearch


class ThesisRecordSearch(NRRecordsSearch):
    LIST_SOURCE_FIELDS = [
        'control_number', 'oarepo:validity.valid', 'oarepo:draft',
        'title', 'dateIssued', 'creator', 'resourceType',
        'contributor', 'keywords', 'subject', 'abstract', 'state', 'accessRights',
        'language',
        '_administration.primaryCommunity',
        '_administration.communities',
        '$schema'
    ]
    HIGHLIGHT_FIELDS = {
        'title.cs': None,
        'title._': None,
        'title.en': None
    }
