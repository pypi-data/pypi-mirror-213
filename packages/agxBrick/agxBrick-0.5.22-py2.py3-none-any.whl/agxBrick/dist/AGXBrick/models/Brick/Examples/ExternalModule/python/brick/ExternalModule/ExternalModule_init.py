from brick.Core.ModelRegistry import deferredRegisterModel, ModelRegistration
from brick.Core.Path import Path

_isInitialized = False

def init():
  global _isInitialized

  if _isInitialized:
      return

  _isInitialized = True;

  

  # NOTE: Deferred registration to avoid startup latency
  def register_ExternalTest():
    from brick.ExternalModule.ExternalTest import ExternalTest

    return ModelRegistration(
      path=Path("ExternalModule.ExternalTest"),
      grpcMsgId=Path("brick.ExternalModule.ExternalTest"),
      modelClass=ExternalTest,
      model=ExternalTest.model,
      grpcClient=None,
    )

  deferredRegisterModel("ExternalModule.ExternalTest", "brick.ExternalModule.ExternalTest", register_ExternalTest)
