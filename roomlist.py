import requests

payUrl = 'http://pay.bjfu.edu.cn/'
buildingAction = 'queryBuildingList'
floorAction = 'queryFloorList'
roomAction = 'queryRoomList'

class building:
    def __init__(self):
        self.building_id= {}
        self.building_name= {}

    def get_buildings(self):
        r = requests.get()
