'''
    @author: Aman Sharma
    date: 12th June, 2022
    statement: We are a file with large number of data of riders in json format,
                and we need to convert that data to a structured format (given)
'''

import json
import os
import re
import csv

class JsonConversion:
    '''
        Class containing two methods:
            one for json structure conversion, and
            second to create csv file.
    '''
    def __init__(self):
        self.json_rider_data = ""
        self.csv_data = []

        self.rider_data = {
            "export_data":{
                "annotations": {
                    "frames": {}
                },
                "number of annotations": 0
            }
        }


    def json_conversion(self, json_file):
        '''
            This function will take the file name as argument
            and extract all the details and convert it into required
            structured format.
        '''
        # rider_data = {
        #     "export_data":{
        #         "annotations": {
        #             "frames": {}
        #         },
        #         "number of annotations": 0
        #     }
        # }

        riders_details = {}
        rider_id = ""

        with open(json_file, 'r', encoding = 'utf-8') as j_file:
            load_json = json.load(j_file)

            all_frame_ids = load_json["rider_info"].keys()
            frames = {}

            for frame_id in all_frame_ids:
                rider_id = load_json["rider_info"][frame_id]["rider_id"]

                for maker_res in load_json["maker_response"]["video2d"]["data"]["annotations"]:

                    riders_details["_id"] = maker_res["frames"][frame_id]["_id"]
                    riders_details["type"] = maker_res["frames"][frame_id]["type"]
                    riders_details["label"] = maker_res["frames"][frame_id]["label"]
                    riders_details["point_x"] = maker_res["frames"][frame_id]["points"]["p1"]["x"]
                    riders_details["point_y"] = maker_res["frames"][frame_id]["points"]["p1"]["y"]
                    riders_details["point_label"] = maker_res["frames"][frame_id] \
                                                        ["points"]["p1"]["label"]
                    riders_details["wearing_mask"] = maker_res["frames"][frame_id] \
                                                        ["attributes"]["waering_mask"]["value"]
                    riders_details["wearing_shirt"] = maker_res["frames"][frame_id]["attributes"] \
                                                        ["wearing_shirt"]["value"]
                    riders_details["selfie_validity"] = maker_res["frames"][frame_id] \
                                                        ["attributes"]["selfie_validity"]["value"]
                    riders_details["rider_id"] = rider_id
                    riders_details["tracker_id"] = maker_res["_id"]

                    self.csv_data.append(
                        [
                            frame_id,
                            maker_res["_id"],
                            maker_res["frames"][frame_id]["label"]
                        ]
                    )

                frames[frame_id] = [riders_details]

        self.rider_data['export_data']['annotations']['frames'] = frames
        self.rider_data["export_data"]["number of annotations"] = len(frames)

        self.json_rider_data = json.dumps(self.rider_data)
        return self.json_rider_data

    def json_to_csv(self):
        '''
            Method to convert json data to csv file for required headers.
        '''
        header = ["frame_id", "tracking_id", "label"]
        try:

            with open('tracker_wise.csv', 'w', encoding='UTF8', newline='') as csv_frame:
                writer = csv.writer(csv_frame)

                # write the header
                writer.writerow(header)

                # write multiple rows
                writer.writerows(self.csv_data)
            print("CSV file created!!")
        except Exception as excep:
            print(f"Something went wrong with error: {excep}")


if __name__ == '__main__':

    current_dir = os.getcwd() # get present working directory where input file should available

    # this will take the input_tracker.json file.
    # So, we need to use/change the input data file with
    # the name starts with "input" and ends with "json"
    input_json_path = [json_file for json_file in os.listdir(current_dir) \
                        if re.match(r'^input.*json$', json_file)][0]

    convert_obj = JsonConversion()
    print(convert_obj.json_conversion(input_json_path))

    convert_obj.json_to_csv()
