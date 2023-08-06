import urllib

from meili_ros_lib.offline import OfflineAgent
from sentry_sdk import capture_exception, capture_message


class Connection:
    def __init__(
            self,
            agent_node,
            handlers,
            vehicle_list,
            disconnection_buffer=5

    ):
        self.offline_flag = agent_node.offline_flag
        self.log_info = agent_node.log_info
        self.log_error = agent_node.log_error
        self.handlers = handlers
        self.vehicle_list = vehicle_list

        self.client = None
        self.internet_down = 0
        self.offline_agent = OfflineAgent(vehicle_list, handlers, self.log_info, self.log_error)

        self.disconnection_buffer = disconnection_buffer

        self.log_info("[OfflineAgent] Initialized agent connection")

    def no_internet(self, ws_open):
        # The internet must be done disc_buffer (disc_buffer) times consecutive in a row
        # This avoids confusion with short internet disconnections
        try:
            if self.internet_down != self.disconnection_buffer:
                self.internet_down += 1
                self.log_info(
                    f"[OfflineAgent] Agent disconnected {self.internet_down}/{self.disconnection_buffer}")
            else:
                self.offline_agent.offline = True

                if ws_open:
                    # self.close_ws()
                    ws_open = False

                if self.offline_flag:
                    if self.offline_agent.offline_tasks is None:
                        self.offline_agent.offline_tasks = self.offline_agent.config_offlinetasks()
                    else:
                        self.offline_agent.activate_offline_agent()
        except Exception as e:
            self.log_info(f"ERROR >> {e}")
        return ws_open

    def check_internet_connection(self, ws_open, host='https://demo.meilirobots.com'):

        try:
            # CHECK FOR INTERNET CONNECTION
            urllib.request.urlopen(host, timeout=5)  # nosec
            self.offline_agent.offline = False
            self.internet_down = 0

            if ws_open is not True:
                self.open_ws()
                ws_open = True
            else:
                # IF WS IS ALREADY OPEN SEND OFFLINE LOG
                pass
                # TODO Send Offline Log in SDK
                # if self.ws.send_offlinelog():
                #    rospy.loginfo("[OfflineAgent] Offline Log Task file sent")
            return ws_open

        except Exception as e:
            ws_open = self.no_internet(ws_open)

            return ws_open

    def open_ws(self):
        self.log_info("[OfflineAgent] Internet Connected")
        # START WS IF IT IS NOT ALREADY OPEN
        try:
            self.client = self.handlers.sdk_setup()
            for index in self.vehicle_list:
                try:
                    self.client.add_vehicle(index)
                except Exception as e:
                    if e == "Vehicle already exists":
                        continue
            self.client.run_in_thread()

        except Exception as e:
            capture_exception(e)
            capture_message(f"[OfflineAgent] Error configuring ws: {e}")
            self.log_error(f"[OfflineAgent] Error configuring ws: {e}")
