
def get_time_from_str(time):
    return int(time.split(":")[0]) * 60 + int(time.split(":")[1])


class Matcher:
    def __init__(self):
        pass
    """
    它们检查一个au内基本的属性(一个record内的field)
    这是一些基本的条件函数，它们会返回匹配器（条件）
    也就是函数，但是是只会返回true/false, 可以被当作条件用的函数
    """
    def action_is(self,intend_action):
        """_summary_
        这个函数接收一个目标行动，
        """
        def matcher(au):
            action = au["action"]
            if action == intend_action:
                return True
            return False
        return matcher

    def start_later_than(self,start):
        """_summary_
        这个函数会把一个时间点和给定的时间对比
        如果给定时间比输入时间晚，输出True
        反之，输出False
        输入标准时间格式hh:mm
        """
        def matcher(au):
            time = au["start"]
            startSpan = get_time_from_str(start)
            timeSpan = get_time_from_str(time)
            if startSpan > timeSpan: 
                return True
            return False
        return matcher
        
    def end_later_than(self,end):
        """_summary_
        exactly the same to above
        """
        def matcher(au):
            time = au["end"]
            endSpan = get_time_from_str(end)
            timeSpan = get_time_from_str(time)
            if endSpan > timeSpan: 
                return True
            return False
        return matcher

    def action_type_is(self,intended_at):
        def matcher(au):
            at = au["action_type"]
            if intended_at == at:
                return True
            return False
        return matcher

    def duration_is_greater_than(self,duration):
        def matcher(au):
            timeSpan = au["timeSpan"]
            if duration > timeSpan:
                return True
            return False
        return matcher

    def date_is(self,intended_date):
        def matcher(au):
            date = au.get("date")
            if date == intended_date:
                return True
            return False
        return matcher

    def property_is(self,intend_property):
        """
        这个matcher返回存在某种属性的au
        简单来说，我拿它作为一个“所有都需要”的占位符
        """
        def matcher(au):
            return True
        return matcher


    """
    这些函数进行条件间的组合
    """
    def matchAll(self,*matchers):
        def combindedMatcher(actionUnit):
            return all(m(actionUnit) for m in matchers)
        return combindedMatcher

    def matchAny(self,*matchers):
        def combindedMatcher(actionUnit):
            return any(m(actionUnit) for m in matchers)
        return combindedMatcher