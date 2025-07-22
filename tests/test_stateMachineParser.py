from Core.Definitions import InputState, UserActionType
from Core.dataAccess.dataService import getData
from Core.translation.fastEnterTranslation import transFastToProp_API
from QtUI.presenters.StateMachinePresenter import StateMachinePresenter


text = "114514CODE123"
wordbank = getData("Data/actionList.json")

def test_state_machine_presenter():
    # 准备
    SM = StateMachinePresenter(wordbank)
    SM.currentState = InputState.AWAIT_ACTION
    
    userAction = {
        "eventType":UserActionType.TEXT_INPUT,
        "text":"114514CODE123"
    }
    
    
    advice = SM.processEvent_API(userAction)
    
    assert isinstance(advice["data"]["action"],str)
    assert advice["data"]["action"] == "CODE"

def test_transFastToProp():
    data = transFastToProp_API(text,wordbank)
    
    assert data["action"] == "CODE"