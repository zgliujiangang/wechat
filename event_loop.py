# coding: utf-8



class EventLoop(object):

	event_pool = {}

	def register(self, productor, consumer):
		# 首先实现事件注册的功能
		# consumer也可以称callback，但是我这里把它称作consumer是因为consumer会使用productor的返回结果
		# 我的例子中也是使用了生产者和消费者来说明的
		# 这里使用了字典去保存这一对生产者和消费者
		self.event_pool[productor] = consumer
		pass

	def remove(self, productor):
		try:
			self.event_pool.pop(productor)
		except KeyError:
			pass
		except Exception:
			pass

	def run(self):
		while True:
			for productor in self.event_pool.keys():
				# 遍历事件池中的生产者
				if productor.is_ready():
					# 生产者已经准备好了
					# 拿到productor给的东西
					data = productor.get_data()
					# 把数据传给consumer, consume应该是一个callable的对象
					consumer(data)
					pass
				else:
					# 生产者未准备好
					pass
	pass


# 我是菜场管理员，一天有个顾客在摊贩那买菜，但是没货了，顾客不能一直等着摊贩去进菜，避免阻塞
# 所以摊贩和顾客到我这来注册了一下进菜事件，本子上记录下待做的事情：进菜，以及做完后应该：打电话通知
# 顾客来拿菜
# 第一种情况：我按照事件本上的事一件件的去问，你有没有做好，没有做好就跳过，做好了就执行下一步动作
# 这是一个典型的事件轮询
# 所以我要实现的一些功能有：1、我有个本子记录各种各样的事情；2、我要不断地循环去看看那些事是已经完成了的
# 3、完成了之后我要把返回的结果推送给顾客

class ProductorConsumer(object):
	# 对于每个人来讲他既可以是消费者也可以是生产者

	def is_ready(self):
		pass

	def get_data(self):
		pass

	def __call__(self, *args, **kwargs):
		pass
	pass



















# 第二种情况：摊贩进菜完了后告诉我已经做完了，我再按照事件本上的记录去通知客户拿菜，先不考虑这种情况