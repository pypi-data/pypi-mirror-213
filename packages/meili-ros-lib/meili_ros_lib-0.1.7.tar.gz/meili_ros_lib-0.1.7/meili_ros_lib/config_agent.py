import copy
import json
import os
from os.path import join

import yaml
from sentry_sdk import capture_exception


class ConfigAgent():
    """
    Class to configure the initial values of the meili_agent
    """

    def __init__(self, log_info, log_error, file_name_vehicles, file_name_topics ):
        # Logging
        self.log_info = log_info
        self.log_error = log_error


        # config agent by reading and storing config files about
        # number of vehicles, prefixes and topics
        self.file_name_vehicles = file_name_vehicles
        self.file_name_topics = file_name_topics
        self.cfg_file_path = os.path.join(os.path.expanduser("~"), ".meili", "cfg.yaml")

        self.data = None
        self.topics = None
        self.cfg = None

    def check_empty(self, variable, name):
        if not variable:
            self.log_error("[Config] %s is empty" % (name,))
            capture_exception(AssertionError)
            raise AssertionError("[Config] Empty", name)

    def open_yaml(self, filename):
        try:
            with open(filename, "r", encoding="utf-8") as config:
                return yaml.safe_load(config)
        except OSError:
            self.log_error("[Config] %s does not exist" % (filename,))
            capture_exception(OSError)
            raise

    def open_json(self, filename):
        try:
            with open(filename, "r", encoding="utf-8") as t:
                return json.load(t)
        except OSError:
            self.log_error("[Config] %s does not exist" % (filename,))
            capture_exception(OSError)
            raise


    def open_files(self):
        # Parse Mode, number of vehicles and tokens from config files passed as arguments
        self.topics = self.open_json(self.file_name_topics)
        self.data = self.open_yaml(self.file_name_vehicles)
        self.cfg = self.open_yaml(self.cfg_file_path)

        self.check_empty(self.topics, "Topics file")
        self.check_empty(self.data, "Data file")
        self.check_empty(self.cfg, "Config file")

    def config_var(self):
        try:
            setup_token = self.cfg["token"]
            server_instance = self.cfg["site"]
            token = self.data["fleet"]

            mqtt_id = self.data["mqtt_id"]

            fleet = True
        except KeyError as e:
            self.log_error(
                "[Config] Configuration of variable %s error" % (e,)
            )
            capture_exception(e)
            raise

        self.check_empty(setup_token, "Config file, token")
        self.check_empty(server_instance, "Config file, server_instance")
        self.check_empty(token, "Data file, fleet")
        self.check_empty(mqtt_id, "Data file, mqtt_id")

        mode = "Fleet"
        self.log_info("[Config] Fleet mode is : %s" % (mode,))

        return setup_token, server_instance, token, mqtt_id, fleet

    def set_vehicles_topics(self, vehicles):
        try:
            for vehicle in vehicles:
                t = copy.deepcopy(self.topics.get("topics", {}))
                t.update(vehicle.get("topics", {}))
                for topic in t:
                    if (vehicle["prefix"]) is not None:
                        t[topic]["topic"] = "{}{}".format(
                            vehicle["prefix"], t[topic]["topic"]
                        )
                    else:
                        t[topic]["topic"] = "{}".format(t[topic]["topic"])

                vehicle["topics"] = t
            return vehicles

        except TypeError:
            self.log_error("[Config] Error setting the vehicles topics")
            capture_exception(TypeError)
            raise

    def config_vehicles(self):

        self.check_empty(self.data["vehicles"], "Data file, vehicles")
        vehicles = self.set_vehicles_topics(self.data["vehicles"])

        vehicle_list = []
        vehicle_tokens = []
        vehicle_names = []

        try:
            # creating sublist of vehicles and tokens
            for vehicle in vehicles:
                vehicle_list.append(vehicle["uuid"])
                vehicle_tokens.append(vehicle["token"])
                vehicle_name = vehicle["token"].split(" ")[0]
                vehicle_names.append(vehicle_name)

        except KeyError as error:
            self.log_error(
                "[Config] Configuration of variable %s error" % (error,)
            )
            capture_exception(error)
            raise

        return vehicle_list, vehicles, vehicle_tokens, vehicle_names
