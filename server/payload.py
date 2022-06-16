import time
from multiprocessing import Process, Pipe
from asyncio import *

class AnyPayload():

    # Хранение данных
    sum = int()
    duration = float()
    out_c = None
    in_c = None

    proc = None

    channel = None

    async def start(self):
        self.out_c, self.in_c = Pipe()

        self.proc = Process(target=self.sum_payload, args=(self.in_c,))
        self.proc.start()

    # Полезная нагрузка
    def sum_payload(self, in_c):
        time_start = time.time()
        self.sum = 0

        for i in range(30_000_000):
            self.sum += i

        self.duration = time.time() - time_start

        in_c.send((self.sum, self.duration))
        in_c.close()
    
    async def result(self):
        success = False
        if not self.out_c.closed: # Если труба не закрыта
            if self.out_c.poll(): # Если пришёл ответ в трубу
                self.sum, self.duration = self.out_c.recv() # получаем значения из трубы
                print(self.sum, self.duration) # выводим на экран
                self.out_c.close() # закрываем трубу
                await self.close() # удаляем этот объект
                success = True
        return success
                

    async def close(self):
        del self
        

# Для тестов
if __name__ == '__main__':
    global prcs
    prcs = list()
    
    for i in range(10):

        any_payload = AnyPayload()

        any_payload.start()

        prcs.append(any_payload)

    def has_alive(): # ищет живые процессы, вернёт False, если все мертвы
        alive = False
        for prc in prcs:
            if prc.proc.is_alive():
                alive = True
        return alive


    while prcs:
        for prc in prcs:
            if not prc.proc.is_alive():
                prc.result()
                prcs.remove(prc)

    print(prcs)
#----------------------------------------------------
    # output_c, input_c = Pipe() # Соединение (труба) по которому идёт обмен данными

    # proc = Process(target=any_payload.sum_payload, args=(input_c,))
    # proc.start() # Запуск процесса
    # while output_c.poll() == False:
    #     time.sleep(0.1)
    # print(output_c.recv()) # Берём данные из него
    # output_c.close()