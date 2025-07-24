

from ti.core.analysis.matchers import action_type_is, date_is, matchAll, property_is
from ti.core.definitions import YESTERDAY, ActionType


YESTERDAY_WORK_MATCHER = matchAll(
    date_is(YESTERDAY),
    action_type_is(ActionType.WORK.value)
)

any_matcher = property_is("action")