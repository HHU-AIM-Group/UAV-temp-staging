# 拍摄数据集
def image_capture(picture_num):
    # 拍摄未压缩的Scene图像
    responsed = AirSim_client.simGetImages([airsim.ImageRequest("front_center", airsim.ImageType.Scene, False, False)])

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
            cv2.imwrite(scenepath + "Scene" + str(picture_nums + picture_num) + ".png", img_rgb)
        else:
            print("No Scene image data received.")
    else:
        print("Scene Image Failed to get.")

    # model = {
    #     "SUV": [178, 221, 213],
    #     "Sedan": [160, 113, 101],
    #     "BoxTruck": [177, 106, 230],
    #     "Campervan": [130, 56, 55]
    # }
    #       SUV RGB设置为[178, 221, 213]
    #     Sedan RGB设置为[160, 113, 101]
    #  BoxTruck RGB设置为[177, 106, 230]
    # Campervan RGB设置为[130,  56,  55]
    found = AirSim_client.simSetSegmentationObjectID("BP_SUV[\w]*", 197, True)
    found = AirSim_client.simSetSegmentationObjectID("BP_Sedan[\w]*", 104, True)
    found = AirSim_client.simSetSegmentationObjectID("BP_BoxTruck[\w]*", 233, True)
    found = AirSim_client.simSetSegmentationObjectID("BP_Campervan[\w]*", 252, True)

    # 拍摄未压缩的Segmentation图像
    responses = AirSim_client.simGetImages(
        [airsim.ImageRequest("front_center", airsim.ImageType.Segmentation, False, False)])

    if responses:
        # 因为返回是一个列表，我们只请求了一张图片，取第一个元素
        response = responses[0]

        # 检查是否有图像数据
        if response is not None and len(response.image_data_uint8) > 0:
            # 从返回的图像数据创建一个numpy数组
            img1d = np.frombuffer(response.image_data_uint8, dtype=np.uint8)

            # 将一维数组重塑为H X W X 4数组
            img_rgb = img1d.reshape(response.height, response.width, 3)

            # 保存图像
            cv2.imwrite(segmentationpath + "Segmentation" + str(picture_nums + picture_num) + ".png", img_rgb)

        else:
            print("No Segmentation image data received.")
    else:
        print("Segmentation Image Failed to get.")