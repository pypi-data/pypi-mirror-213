import numpy as np
from .loaders import EEGLoader, ACCLoader, BLELoader

def load_data(eeg_path, acc_path, ble_path, sf_send):
    raw_acc = raw_eeg = package_loss_rate = total_time = disconnections = disconnect_rate = None
    if acc_path is not None:
        acc_loader = ACCLoader(sf_send)
        raw_acc, acc_loss_rate, total_time = acc_loader.load_data(acc_path)
    if eeg_path is not None:
        eeg_loader = EEGLoader(sf_send)
        raw_eeg, eeg_loss_rate, total_time = eeg_loader.load_data(eeg_path)

    if raw_eeg is not None and raw_acc is not None:
        assert raw_eeg.shape[0] != raw_acc.shape[0]
    if eeg_loss_rate is not None and acc_loss_rate is not None:
        assert eeg_loss_rate == acc_loss_rate
        package_loss_rate = eeg_loss_rate

    if ble_path is not None:
        ble_loader = BLELoader()
        disconnections = ble_loader.load_data(ble_path)

        if disconnections is not None and disconnections.shape[0] == 0:
            disconnections = disconnections / 1000.0 / 1000.0
            time_gap = (disconnections[:, 1] - disconnections[:, 0])
            total_time = total_time + np.sum(time_gap)
            disconnect_rate = np.sum(time_gap) / total_time * 100
        else:
            disconnect_rate = 0

            # seg_gap = np.around(time_gap / 15).astype(np.int32)
            # disconnection_st = disconnections[:, 0]
            # disconnection_index = np.around((disconnection_st - st_time) / 15).astype(np.int32)
            #
            # disconnection_count = len(time_gap)

    return raw_eeg, raw_acc, disconnections, total_time, package_loss_rate, disconnect_rate
