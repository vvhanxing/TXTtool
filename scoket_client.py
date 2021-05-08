#/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import time
import select
import socket
import requests
import threading
from http_client import DownAGV
from socket_client import UpAGV
from xyz_robot import XYZRobot
from http_backend import SimpleHTTPHandler, WCSHTTPServer
from wcs_define import GEEK_HTTP_ADDR, GEEK_SOCK_ADDR, WCS_HTTP_ADDR, GEEK_RECALL, ROBOT_RECALL, WCS_CONTROL, get_logger_obj, UP_AGV_POS_MAP, DOWN_AGV_POS_MAP
from wcs_define import wcs_log as log

FAIL = -1
INVALID = 1
SCCUESS = 0


# TODO deal with close [http error]
# TODO HTTP Error
# TODO pull WCS ERROR to HMI
class WorkFlow(object):
    def __init__(self, producer, consumer, distributor):
        self.producer = producer
        self.consumer = consumer
        self.distributor = distributor
        self.running = True
        # self.closed = True

    def call_forth(self):
        log.info("[Main] call forth")
        is_ready = self.ready_for_pull([self.producer, self.consumer])
        res = is_ready()
        log.info("[Main][Forth] producer and consumer ready? *%s*" % str(res))
        if res:
            p = self.call_producer_forth()
            c = self.call_consumer_forth()
            if p == SCCUESS or c == SCCUESS:
                return SCCUESS
            else:
                return INVALID
        else:
            return FAIL

    def call_back(self):
        log.info("[Main] call back")
        is_ready = self.make_sure_done([self.distributor], None)
        res = is_ready()
        log.info("[Main][Back] producer and consumer ready? *%s*" % str(res))
        if res:
            p = self.call_producer_back()
            c = self.call_consumer_back()
            if p == SCCUESS or c == SCCUESS:
                return SCCUESS
            else:
                return INVALID
        else:
            return FAIL

    def call_producer_forth(self):
        """
        Returns:
            Bool, true if success.
        """
        try:
            ret = self.producer.pull()  # pull agv
        except Exception:
            log.error("[CALL FORTH] up agv error", exc_info=True)
            return FAIL
        if ret:
            return SCCUESS
        else:
            return INVALID

    def call_producer_back(self):
        """
        Returns:
            Bool, true if success.
        """
        try:
            ret = self.producer.push()  # push agv

        except Exception:
            log.error("[CALL BACK] up agv error", exc_info=True)
            return FAIL
        if ret:
            return SCCUESS
        else:
            return INVALID

    def call_consumer_forth(self):
        """
        Returns:
            Bool, true if success.
        """
        try:
            self.consumer.pull()  # pull agv
        except Exception:
            log.error("[CALL FORTH] down agv error", exc_info=True)
            return False
        return True

    def call_consumer_back(self):
        """
        Returns:
            Bool, true if success.
        """
        try:
            self.consumer.push()  # push agv
        except requests.ConnectTimeout:
            log.error("[CALL BACK] down agv server is timeout")
            self.distributor.send_msg_to_hmi
        except requests.ConnectionError:
            log.error("[CALL BACK] down agv server is off")
        except Exception:
            log.error("[CALL BACK] down agv error", exc_info=True)
            return False
        return True

    def call_distributor(self):
        log.info("[Main][Distributor] call distributor")

        is_ready = self.ready_for_sort([self.producer, self.consumer])
        res = is_ready()
        log.info("[Main][Distributor] producer and consumer ready? *%s*" %
                 str(res))
        if res:
            self.distributor.pull()
            return SCCUESS
        else:
            return FAIL

    def ready_for_pull(self, obj_list):
        return self.make_sure_done(obj_list, before=False)

    def ready_for_sort(self, obj_list):
        return self.make_sure_done(obj_list, before=True)

    def make_sure_done(self, obj_list, before):
        def is_ready(obj_list=obj_list, before=before):
            for obj in obj_list:
                if not obj.is_ready(before=before):
                    return False
            return True

        return is_ready

    def drive_loop(self):
        loop = [
            self.call_forth,  # call agv to fill all empty space
            # self.ready_for_sort([self.producer, self.consumer]), # each of producer and consumer have at leat one AGV is ready
            self.call_distributor,  # call robot to work
            # self.make_sure_done([self.distributor], None),       # make sure robot is done
            self.call_back,
            # if UP AGV is on and NUM is 0, call back    if DOWN AGV is on and NUM is MAX_NUM, call back
            # self.ready_for_pull([self.producer, self.consumer])  # make sure all AGV is in off or on status
        ]
        length = len(loop)
        while 1:
            i = 0
            while i < length:
                log.info("[Main][STEP] try next step")
                if not self.running:
                    self.close()  # init
                    # TODO 如果货物没有被清理完, 就让来料AGV返回会如何
                    i = 0
                    yield

                result = loop[i]()
                print("loop result:%d" % result)
                # input("enter to continue")
                if result == SCCUESS:
                    i += 1
                elif result == INVALID:
                    i += 1
                    continue
                else:
                    pass
                yield
            log.info("[Main][STEP] A loop ends")

    def update_status(self, data):
        """Start or stop workflow.
        Args:
            data: dict

        Exceptions:
            AssertError
        """
        cmd = data.get("cmd")
        assert cmd in (0, 1)
        self.running = bool(cmd)
        # if self.running:
        #     self.closed = False

    def close(self):
        # if not self.closed:
        #     ret = self.consumer.init_agv()
        #     self.closed = True
        ret = self.consumer.init()  # It's ok to call it repeatly
        log.info("[CLOSE] withdraw down AGV: %s" % ' '.join(ret))
        ret = self.producer.init()
        log.info("[CLOSE] withdraw up AGV: %s" % ' '.join(ret))

    def auto_drive(self):

        log.info("[Main][auto driver] http request starts")
        threading.Thread(target=self._auto_drive).start()

    def _auto_drive(self):
        url = "http://127.0.0.1:%s/" % WCS_HTTP_ADDR[-1]
        ret = requests.get(url=url)
        log.info("[Main][auto driver] http request ends, status code %d" %
                 ret.status_code)


def run_wcs():
    epoll = select.epoll()
    socket_map = {}

    # send_queue_map = {}

    def register(sock_obj, epoll=epoll, socket_map=socket_map):
        fd = sock_obj.fileno()
        epoll.register(fd)
        socket_map[fd] = sock_obj
        return fd

    def unregister(fd, epoll=epoll, socket_map=socket_map):
        epoll.unregister(fd)
        del socket_map[fd]

    def connect():
        sock_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_client.connect(GEEK_SOCK_ADDR)
        sock_client.setblocking(False)
        return sock_client

    def reconnect(fd, upAgv):
        unregister(fd)
        sock_client = connect()
        register(sock_client)
        upAgv.connect(sock_client)
        return sock_client

    def recv_msg(socket_obj, handler):
        data = ''
        while True:
            new_data = socket_obj.recv(2048).decode()
            if not new_data:
                return False
            data += new_data
            log.info("[Raw Msg] %s" % data)

            splits = data.split("\r\n")
            for _ in range(len(splits) - 1):
                handler(splits.pop(0))
            if not splits[0]:
                log.info("finish recv")
                break

            else:
                data = splits[0]
                log.info("[Raw Msg] remain incomplete data: %s" % data)

        return True

    sock_client = connect()

    downAgvHandler = DownAGV(*GEEK_HTTP_ADDR)
    http_server = WCSHTTPServer(WCS_HTTP_ADDR, SimpleHTTPHandler)
    upAgvHandler = UpAGV(sock_client)
    xyz_robot = XYZRobot()
    http_server_fd = http_server.fileno()
    log.info("http server fd is %d" % http_server_fd)
    sock_client_fd = sock_client.fileno()
    log.info("socket client fd is %d" % sock_client_fd)

    socket_map[http_server_fd] = http_server.socket
    socket_map[sock_client_fd] = sock_client

    http_server_fd = register(http_server.socket)
    sock_client_fd = register(sock_client)
    # send_queue_map[http_server_fd] = []
    # send_queue_map[sock_client_fd] = []

    wtf = WorkFlow(upAgvHandler, downAgvHandler, xyz_robot)

    http_server.route_map[GEEK_RECALL] = (downAgvHandler.update_pos_status, )
    http_server.route_map[ROBOT_RECALL] = (downAgvHandler.update_num_status,
                                           xyz_robot.update_status,
                                           upAgvHandler.update_num_status)
    http_server.route_map[WCS_CONTROL] = (wtf.update_status, )

    wtf_loop = wtf.drive_loop()

    while True:
        events = epoll.poll(20)
        log.info("******%s******" % str(events))
        if not events:
            upAgvHandler.heart_beat()
            print("***%s alive***" % str(int(time.time())))
        for fd, event in events:
            if fd == http_server_fd:
                if event & select.EPOLLIN:
                    conn, addr = socket_map[fd].accept()
                    #from ipdb import set_trace; set_trace()
                    http_server.process_request(conn, addr)
                else:
                    raise Exception("http server error")
                # if communicate with socket server, there is no need to heart beat
                upAgvHandler.heart_beat()

            else:  # fd == sock_client_fd:
                if event & select.EPOLLIN:
                    print("ready to recv data***")
                    ret = recv_msg(socket_map[fd],
                                   upAgvHandler.update_pos_status)
                    print("recv return %s******" % ret)
                elif event & select.EPOLLOUT:
                    epoll.modify(fd, select.EPOLLIN)
                elif event & select.EPOLLHUP:
                    print("upAgv connection break")
                    reconnect(fd, upAgvHandler)
                    continue
                else:
                    print("upAgv connection break for reason: %d" % event)
                    reconnect(fd, upAgvHandler)
                    continue

            next(wtf_loop)


if __name__ == "__main__":
    run_wcs()
