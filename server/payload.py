import time
from multiprocessing import Process, Pipe

class AnyPayload():

    # Хранение данных
    sum = int()
    duration = float()

    # Полезная нагрузка
    def sum_payload(self, conn):
        time_start = time.time()
        self.sum = 0

        for i in range(20_000_000):
            self.sum += i

        self.duration = time.time() - time_start
        
        conn.send((self.sum, self.duration))
        conn.close()

# Для тестов
if __name__ == '__main__':
    any_payload = AnyPayload()

    output_c, input_c = Pipe() # Соединение (труба) по которому идёт обмен данными

    proc = Process(target=any_payload.sum_payload, args=(input_c,))
    proc.start() # Запуск процесса
    while output_c.poll() == False:
        time.sleep(0.1)
    print(output_c.recv()) # Берём данные из него
    output_c.close()
    print(output_c.closed)