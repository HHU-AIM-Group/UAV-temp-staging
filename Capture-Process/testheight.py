import time
import math
import airsim
import cv2
import numpy as np

scenepath = "SceneImage/"
vehicle_name = ""
AirSim_client = airsim.MultirotorClient()
AirSim_client.confirmConnection()
AirSim_client.enableApiControl(True, vehicle_name)
AirSim_client.armDisarm(True, vehicle_name)
AirSim_client.takeoffAsync(vehicle_name=vehicle_name).join()

alpha = -math.pi / 36

for j in range(10):
    AirSim_client.moveByVelocityAsync(0, 0, -5, 1).join()
    AirSim_client.hoverAsync().join()
    time.sleep(3)

    height = (j + 1) * 5
    camera_rotation = 0.

    for i in range(19):
        print(height, camera_rotation)
        found1 = AirSim_client.simSetSegmentationObjectID("BP_SUV[\w]*", 197, True)
        found2 = AirSim_client.simSetSegmentationObjectID("BP_Sedan[\w]*", 104, True)
        found3 = AirSim_client.simSetSegmentationObjectID("BP_BoxTruck[\w]*", 233, True)
        found4 = AirSim_client.simSetSegmentationObjectID("BP_Campervan[\w]*", 252, True)

        AirSim_client.simSetCameraSegmentationObjectId("front_center", True)
        response = AirSim_client.simGetImages([airsim.ImageRequest("front_center", airsim.ImageType.Segmentation)])
        segmentation_image = np.frombuffer(response[0].image_data_uint8, dtype=np.uint8).reshape(response[0].height,
                                                                                                 response[0].width, 3)
        has_bp_suv = np.any(segmentation_image == 197)
        has_bp_Sedan = np.any(segmentation_image == 104)
        has_bp_BoxTruck = np.any(segmentation_image == 233)
        has_bp_Campervan = np.any(segmentation_image == 252)
        if not has_bp_suv and not has_bp_Sedan and not has_bp_BoxTruck and not has_bp_Campervan:
            continue
        responsed = AirSim_client.simGetImages(
            [airsim.ImageRequest("front_center", airsim.ImageType.Scene, False, False)])
        if responsed:
            # 获取第一个图像响应
            image_response = responsed[0]

            # 检查图像数据是否有效
            if image_response is not None and len(image_response.image_data_uint8) > 0:
                # 从返回的图像数据创建一个numpy数组
                img1d = np.frombuffer(image_response.image_data_uint8, dtype=np.uint8)

                # 将一维数组重塑为H X W X 3数组
                img_rgb = img1d.reshape(image_response.height, image_response.width, 3)

                # 保存图像
                cv2.imwrite(scenepath + "Scene" + str(j * 19 + i) + ".png", img_rgb)
            else:
                print("No Scene image data received.")
        else:
            print("Scene Image Failed to get.")

        camera_rotation += alpha
        if camera_rotation > 0:
            camera_rotation = 0
        if camera_rotation < - math.pi / 2:
            camera_rotation = - math.pi / 2
        camera_pose = airsim.Pose(airsim.Vector3r(0, 0, 0),
                                  airsim.to_quaternion(camera_rotation, 0, 0))
        AirSim_client.simSetCameraPose(0, camera_pose)

    camera_rotation = 0.
    camera_pose = airsim.Pose(airsim.Vector3r(0, 0, 0), airsim.to_quaternion(camera_rotation, 0, 0))
    AirSim_client.simSetCameraPose(0, camera_pose)

print("Caputure Done!")

AirSim_client.landAsync(vehicle_name=vehicle_name).join()
AirSim_client.armDisarm(False, vehicle_name)
AirSim_client.enableApiControl(False)
