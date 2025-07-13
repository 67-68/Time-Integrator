from Core.Definitions import TODAY,ActionType
from Core.analysis.matchers import matchAll,date_is, action_type_is


TODAY_WORK_MATCHER = matchAll(
    date_is(TODAY),
    action_type_is(ActionType.WORK.value)
)