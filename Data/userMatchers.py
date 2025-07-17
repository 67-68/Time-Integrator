from Core.Definitions import YESTERDAY,ActionType
from Core.analysis.matchers import matchAll,date_is, action_type_is, property_is


YESTERDAY_WORK_MATCHER = matchAll(
    date_is(YESTERDAY),
    action_type_is(ActionType.WORK.value)
)

any_matcher = property_is("action")