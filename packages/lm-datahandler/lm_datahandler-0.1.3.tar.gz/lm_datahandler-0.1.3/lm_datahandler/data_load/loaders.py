import numpy as np


def int_from_bytes_8bit(byte_arr):
    buffer = np.asarray(
        [1, 256, np.power(np.int64(256), 2), np.power(np.int64(256), 3), np.power(np.int64(256), 4),
         np.power(np.int64(256), 5), np.power(np.int64(256), 6), np.power(np.int64(256), 7)])

    res = byte_arr[0] * buffer[0] + byte_arr[1] * buffer[1] + byte_arr[2] * buffer[2] + byte_arr[3] * buffer[
        3] + \
          byte_arr[4] * buffer[4] + byte_arr[5] * buffer[5] + byte_arr[6] * buffer[6] + byte_arr[7] * buffer[7]
    return np.sum(res)


def int_from_bytes_4bit(byte_arr):
    buffer = np.asarray([1, 256, np.power(np.int64(256), 2), np.power(np.int64(256), 3)])

    res = byte_arr[0] * buffer[0] + byte_arr[1] * buffer[1] + byte_arr[2] * buffer[2] + byte_arr[3] * buffer[3]
    return np.sum(res)


class BaseLoader(object):
    def __init__(self):
        pass



    def load_data(self, data_path):
        DataTotal = []
        PackageIDs = []
        self.file_data = open(data_path, 'rb')

        self.file_data_len = len(self.file_data.read())
        self.file_data.seek(0, 0)
        self.data_type = self.file_data.read(3)

        self.file_data.seek(4, 0)
        self.device_type = int.from_bytes(self.file_data.read(4), byteorder='little', signed=False)

        self.file_data.seek(12, 0)
        self.package_count = int.from_bytes(self.file_data.read(4), byteorder='little', signed=False)
        self.file_data.seek(16, 0)
        self.resolution = int.from_bytes(self.file_data.read(1), byteorder='little', signed=False)

        self.file_data.seek(21, 0)
        self.sampleRate = int.from_bytes(self.file_data.read(4), byteorder='little', signed=False)
        self.file_data.seek(81, 0)
        self.channel_data_length = int.from_bytes(self.file_data.read(4), byteorder='little', signed=False)

        self.file_data.seek(90, 0)
        self.data_offSet = int.from_bytes(self.file_data.read(4), byteorder='little', signed=False)
        self.file_data.seek(0, 0)

    # def _read_time_range(self):
    #     self.file_data.seek(30, 0)
    #     ST_Y = int.from_bytes(self.file_data.read(2), byteorder='little', signed=False)
    #     ST_M = int.from_bytes(self.file_data.read(1), byteorder='little', signed=False)
    #     ST_D = int.from_bytes(self.file_data.read(1), byteorder='little', signed=False)
    #     ST_H = int.from_bytes(self.file_data.read(1), byteorder='little', signed=False)
    #     ST_Min = int.from_bytes(self.file_data.read(1), byteorder='little', signed=False)
    #     ST_S = int.from_bytes(self.file_data.read(1), byteorder='little', signed=False)
    #     ST_ms = int.from_bytes(self.file_data.read(2), byteorder='little', signed=False)
    #     ST_D_more = 0
    #     if ST_H >= 24:
    #         ST_H = ST_H - 24
    #         ST_D_more = 1
    #     st_datetime = datetime(ST_Y, ST_M, ST_D, ST_H, ST_Min, ST_S, ST_ms)
    #     st_datetime = st_datetime + timedelta(days=ST_D_more)
    #
    #     self.file_data.seek(40, 0)
    #     if is_crash:
    #         total_seconds = PackageCount * 0.1
    #         et_datetime = st_datetime + timedelta(seconds=total_seconds)
    #     else:
    #         ET_Y = int.from_bytes(self.file_data.read(2), byteorder='little', signed=False)
    #         ET_M = int.from_bytes(self.file_data.read(1), byteorder='little', signed=False)
    #         ET_D = int.from_bytes(self.file_data.read(1), byteorder='little', signed=False)
    #         ET_H = int.from_bytes(self.file_data.read(1), byteorder='little', signed=False)
    #         ET_Min = int.from_bytes(self.file_data.read(1), byteorder='little', signed=False)
    #         ET_S = int.from_bytes(self.file_data.read(1), byteorder='little', signed=False)
    #         ET_ms = int.from_bytes(self.file_data.read(2), byteorder='little', signed=False)
    #         ET_D_more = 0
    #         if ET_H >= 24:
    #             ET_H = ET_H - 24
    #             ET_D_more = 1
    #         et_datetime = datetime(ET_Y, ET_M, ET_D, ET_H, ET_Min, ET_S, ET_ms)
    #         et_datetime = et_datetime + timedelta(days=ET_D_more)
    #     total_time = (et_datetime - st_datetime).total_seconds()


class EEGLoader(BaseLoader):
    def __init__(self, sf_send=10):
        super().__init__()
        if sf_send == 10:
            self.package_length = 208
            self.package_std_time_interval = [100 - 20, 100, 100 + 20]
        elif sf_send == 50:
            self.package_length = 48
            self.package_std_time_interval = [20-10, 20, 20+10]

    def load_data(self, data_path):
        super(EEGLoader, self).load_data(data_path)

        # if self.device_type == 44:
        #     pass
        # else:
        #     self.package_std_time_interval = [70 - 20, 70, 70 + 20]
        self.file_data.seek(self.data_offSet, 0)
        all_packages = np.array(list(self.file_data.read(self.package_count * self.package_length))).reshape(
            [-1, self.package_length])
        all_package_data = all_packages[:, 8:]

        all_package_ids = all_packages[:, 0:8]
        all_package_ids = np.apply_along_axis(int_from_bytes_8bit, 1, all_package_ids)
        package_time_intervals = all_package_ids[1:] - all_package_ids[0:-1]

        package_time_intervals = np.round(package_time_intervals / self.package_std_time_interval[1])
        package_time_intervals = np.insert(package_time_intervals, 0, [1])

        package_repeats = package_time_intervals.astype(np.int32)
        package_repeats[package_repeats <= 0] = 1

        self.time_length = np.sum(package_repeats)*0.1
        self.package_loss = (np.sum(package_repeats) - package_repeats.__len__()) / np.sum(package_repeats) * 100

        all_package_ids = np.repeat(all_package_ids, package_repeats, axis=0)
        all_package_data = np.repeat(all_package_data, package_repeats, axis=0)
        all_package_data = all_package_data.reshape([-1, self.resolution])

        # package_loss_new = all_package_ids.shape[0] / total_time*10

        all_package_data = all_package_data[:, 0] + all_package_data[:, 1] * 256
        all_package_data = np.squeeze(all_package_data)

        data_total = all_package_data
        data_total = data_total[0:len(data_total) // 2 * 2]
        data_total_T = data_total.reshape(-1, 2)
        self.data_total = []
        self.data_total.append(data_total_T[:, 0])
        self.data_total.append(data_total_T[:, 1])
        self.data_total = np.asarray(self.data_total)

        return self.data_total, self.package_loss, self.time_length


class ACCLoader(BaseLoader):
    def __init__(self, sf_send):
        super().__init__()
        if sf_send == 10:
            self.package_length = 38
            self.package_std_time_interval = [100 - 20, 100, 100 + 20]
        elif sf_send == 50:
            self.package_length = 14
            self.package_std_time_interval = [20-10, 20, 20+10]

    def load_data(self, data_path):
        super(ACCLoader, self).load_data(data_path)
        # if self.device_type == 44:
        #     pass
        # else:
        #     self.package_std_time_interval = [70 - 20, 70, 70 + 20]
        self.file_data.seek(self.data_offSet, 0)
        all_packages = np.array(list(self.file_data.read(self.package_count * self.package_length))).reshape(
            [-1, self.package_length])
        all_package_data = all_packages[:, 8:]

        all_package_ids = all_packages[:, 0:8]
        all_package_ids = np.apply_along_axis(int_from_bytes_8bit, 1, all_package_ids)
        package_time_intervals = all_package_ids[1:] - all_package_ids[0:-1]

        package_time_intervals = np.round(package_time_intervals / self.package_std_time_interval[1])
        package_time_intervals = np.insert(package_time_intervals, 0, [1])

        package_repeats = package_time_intervals.astype(np.int32)
        package_repeats[package_repeats <= 0] = 1

        self.time_length = np.sum(package_repeats)*0.1
        self.package_loss = (np.sum(package_repeats) - package_repeats.__len__()) / np.sum(package_repeats) * 100

        all_package_ids = np.repeat(all_package_ids, package_repeats, axis=0)
        all_package_data = np.repeat(all_package_data, package_repeats, axis=0)
        all_package_data = all_package_data.reshape([-1, self.resolution])

        # package_loss_new = all_package_ids.shape[0] / total_time*10

        all_package_data = all_package_data[:, 0] + all_package_data[:, 1] * 256
        all_package_data = np.squeeze(all_package_data)

        data_total = all_package_data
        data_total = data_total[0:len(data_total) // 3 * 3]
        data_total_T = data_total.reshape(-1, 3)
        self.data_total = []
        self.data_total.append(data_total_T[:, 0])
        self.data_total.append(data_total_T[:, 1])
        self.data_total.append(data_total_T[:, 2])
        self.data_total = np.asarray(self.data_total)

        return self.data_total, self.package_loss, self.time_length



class BLELoader(BaseLoader):
    def __init__(self):
        super().__init__()


    def load_data(self, data_path):
        super(BLELoader, self).load_data(data_path)

        total_length = len(self.file_data.read())
        self.file_data.seek(90, 0)
        offset = int.from_bytes(self.file_data.read(4), byteorder='little', signed=False)
        self.file_data.seek(offset, 0)
        ble_data = np.array(list(self.file_data.read(total_length - offset)))
        if ble_data.shape[0] == 0:
            return None

        ble_data = ble_data.reshape(-1, 16)
        status = ble_data[:, 0:4]
        status = np.apply_along_axis(int_from_bytes_4bit, 1, status)

        package_id = ble_data[:, 4:8]
        package_id = np.apply_along_axis(int_from_bytes_4bit, 1, package_id)

        sys_time = ble_data[:, 8:16]
        sys_time = np.apply_along_axis(int_from_bytes_8bit, 1, sys_time)

        disconnections = sys_time[0: sys_time.shape[0] // 2 * 2].reshape([-1, 2])
        drop_index = np.asarray([])
        for i in range(disconnections.shape[0]):
            if disconnections[i][1] - disconnections[i][0] > 12 * 24 * 3600 * 10000000:
                drop_index = np.append(drop_index, i).astype(np.int32)
        if drop_index.shape[0] != 0:
            disconnections = np.delete(disconnections, drop_index, axis=0)

        return disconnections
