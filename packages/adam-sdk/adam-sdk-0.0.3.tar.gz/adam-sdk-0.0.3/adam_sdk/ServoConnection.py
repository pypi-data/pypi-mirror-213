from typing import List
from servo_serial.connection import Connection
from scservo_sdk import GroupSyncWrite, SCS_LOBYTE, SCS_HIBYTE

class ServoConnection:
    def __init__(self):
        self.__doubleBuffer = []

    def append_command_buffer(self, command: tuple[int, int, float]):
        # Добавляет команду в буфер двойной буферизации
        self.__doubleBuffer.append(command)

    def execute_command_servo(self):
        self.sync_write_servos()

    def sync_write_servos(self):
        ADDR_STS_GOAL_POSITION = 42  # Адрес для задания целевой позиции
        ADDR_STS_GOAL_SPEED = 46  # Адрес для задания целевой скорости

        portHandler = Connection().getPortHandler()  # Инициализация объекта для обработки порта
        packetHandler = Connection().getPacketHandler()  # Инициализация объекта для обработки пакетов
        groupSyncWrite = GroupSyncWrite(portHandler, packetHandler, ADDR_STS_GOAL_POSITION, 2)  # Создание объекта для синхронной записи

        scs_comm_result = []  # Результаты коммуникации
        scs_error = []  # Ошибки коммуникации
        scs_add_param_result = []  # Результаты добавления параметров

        for servoId, servoSpeed, goalPos in self.__doubleBuffer:
            scs_comm_result.append(packetHandler.write2ByteTxRx(portHandler, servoId,
                                                                ADDR_STS_GOAL_SPEED, servoSpeed))  # Запись целевой скорости

            param_goal_position = [SCS_LOBYTE(int(goalPos)), SCS_HIBYTE(int(goalPos))]
            scs_add_param_result.append(groupSyncWrite.addParam(servoId, param_goal_position))  # Добавление параметров целевой позиции

        scs_comm_result.append(groupSyncWrite.txPacket())  # Отправка пакета синхронной записи

        self.__doubleBuffer.clear()  # Очистка двойного буфера
        groupSyncWrite.clearParam()  # Очистка параметров синхронной записи

        return scs_comm_result, scs_error, scs_add_param_result