# 1. 导入IBurpExtender类,这是每一个Burp扩展工具时必须使用的类
from burp import IBurpExtender
from burp import IIntruderPayloadGeneratorFactory
from burp import IIntruderPayloadGenerator
from java.util import List, ArrayList
import random


# 2. 定义自己的BurpExtender类
class BurpExtender(IBurpExtender, IIntruderPayloadGeneratorFactory):
  def registerExtenderCallbacks(self, callbacks):
    self._callbacks = callbacks
    self._helpers = callbacks.getHelpers()
    callbacks.setExtensionName("web_fuzz")
    # 3. 使用registerIntruderPayloadGeneratorFactory 函数注册BurpExtender类，
    # 这样Intruder工具才能生成攻击载荷。
    callbacks.registerIntruderPayloadGeneratorFactory(self)
    return

  # 4. getGeneratorName函数,让它返回载荷生成器的名称。
  def getGeneratorName(self):
    return "web_fuzz"
  # 5. createNewInstance函数接收攻击相关的参数，
  # 返回IIntruderPayloadGenerator类型的实例，我们将它命名为BHPFuzzer。
  def createNewInstance(self, attack):
    return BHPFuzzer(self, attack)

#  6. 扩展继承IIntruderPayloadGenerator类
class BHPFuzzer(IIntruderPayloadGenerator):
  def __init__(self, extender, attack):
    self._extender = extender
    self._helpers  = extender._helpers
    self._attack   = attack
    print "web_fuzz"
    # 7. 设置计数器
    self.max_payloads = 1000
    self.num_payloads = 0
 
    return
 
  # 8. 检查模糊测试时迭代的数量是否到达上限
  def hasMorePayloads(self):
    print "hasMorePayloads called."
    if self.num_payloads == self.max_payloads:
      print "No more payloads."
      return False
    else:
      print "More payloads. Continuing."
      return True
 
  # 9. 负责接收原始的HTTP载荷，这里就是进行模糊测试的地方。
  def getNextPayload(self,current_payload):
    # 10. current_payload变量是数组格式，我们需要将它转换成字符串
    payload = "".join(chr(x) for x in current_payload)
    # 11. 传递给模糊测试的函数mutate_payload
    payload = self.mutate_payload(payload)
    # 12. 将num_payloads变量的值增加
    self.num_payloads += 1
    return payload
 
  def reset(self):
    self.num_payloads = 0
    return

  # 模糊测试函数
  def mutate_payload(self,original_payload):
    picker = random.randint(1,3)
    offset  = random.randint(0,len(original_payload)-1)
    payload = original_payload[:offset]
 
    if picker == 1:
      payload += "'"
 
    if picker == 2:
      payload += "<script>alert('xss');</script>";
 
    if picker == 3:
      chunk_length = random.randint(len(payload[offset:]),len(payload)-1)
      repeater     = random.randint(1,10)
 
      for i in range(repeater):
        payload += original_payload[offset:offset+chunk_length]
 
    payload += original_payload[offset:]
    return payload
 