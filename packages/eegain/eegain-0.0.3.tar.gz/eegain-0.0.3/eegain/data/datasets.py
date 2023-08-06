import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

import mne
import numpy as np
import torch
from torch.utils.data import Dataset

from ..transforms import Construct


class EEGDatasetBase(Dataset):
    """
    Python dataset wrapper that takes tensors and implements dataset structure
    """

    def __init__(self, x_tensor: torch.Tensor, y_tensor: torch.Tensor):
        self.x = x_tensor
        self.y = y_tensor

        assert len(self.x) == len(self.y)

    def __getitem__(self, index: int) -> Tuple[torch.Tensor, torch.Tensor]:
        return self.x[index], self.y[index]

    def __len__(self) -> int:
        return len(self.y)


class EEGDataset(ABC):
    @abstractmethod
    def __get_subject_ids__(self) -> List[int]:
        raise NotImplementedError

    @abstractmethod
    def __get_subject__(
        self, subject_index: int
    ) -> Tuple[Dict[int, np.ndarray], Dict[int, int]]:
        raise NotImplementedError


class MAHNOB(EEGDataset):
    @staticmethod
    def _create_user_csv_mapping(data_path: Path) -> Dict[int, List[str]]:
        """
        this functions creates mapping dictionary {user_id: [all csv files names for this user_id]}
        """
        user_session_info: Dict[int, List[str]] = defaultdict(list)

        for xml_file_path in data_path.glob("**/*.xml"):
            with open(xml_file_path, "r") as f:
                data = f.read()
                root = ET.fromstring(data)
            subj_id = int(root.find("subject").attrib["id"])
            session_id = root.attrib["sessionId"]
            user_session_info[subj_id].append(session_id)

        return user_session_info

    def __init__(self, root: str, label_type: str, transform: Construct = None):
        self.root = Path(root)
        self.transform = transform
        self.mapping_list = MAHNOB._create_user_csv_mapping(self.root)
        self.label_type = label_type

    def __get_subject_ids__(self) -> List[int]:
        return list(self.mapping_list.keys())

    def __get_subject__(
        self, subject_index: int
    ) -> Tuple[Dict[int, np.ndarray], Dict[int, int]]:
        sessions = self.mapping_list[subject_index]

        data_array, label_array = {}, {}

        for session in sessions:
            xml_path = next((Path(self.root) / session).glob("*.xml"), None)
            bdf_path = next((Path(self.root) / session).glob("*.bdf"), None)
            if (xml_path is None) or (bdf_path is None):
                continue

            data = mne.io.read_raw_bdf(str(bdf_path), preload=True, verbose=False)

            if self.transform:
                data = self.transform(data)

            data_array[session] = data.get_data()

            with open(xml_path, "r") as f:
                data = f.read()
                root = ET.fromstring(data)
            felt_arousal = int(root.attrib["feltArsl"])
            felt_valence = int(root.attrib["feltVlnc"])
            label_array[session] = np.array([felt_arousal, felt_valence])

        # choose label and split into binary
        idx = 0 if self.label_type == "A" else 1
        for session_id, data in label_array.items():
            target_label = data[idx]
            target_label = 0 if target_label <= 5 else 1
            label_array[session_id] = target_label

        # expand dims
        data_array = {
            key: np.expand_dims(value, axis=-3) for key, value in data_array.items()
        }

        return data_array, label_array
