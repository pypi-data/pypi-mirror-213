import os
import numpy as np
import natsort


class Single_audio_motion_synch(object):
    def __init__(
        self, audio_folder, bvh_folder, dst_bvh_folder=None, dst_audio_folder=None
    ):
        self._audio_folder = audio_folder
        self._bvh_folder = bvh_folder
        if dst_bvh_folder is None:
            self._dst_bvh_folder = "data/motion/Gesture_Synched"
        else:
            self._dst_bvh_folder = dst_bvh_folder
        if dst_audio_folder is None:
            self._dst_audio_folder = "data/audio/Gesture_Synched"
        else:
            self._dst_audio_folder = dst_audio_folder

    def change_dst_bvh(self, dst_bvh_folder):
        self._dst_bvh_folder = dst_bvh_folder

    def change_dst_audio(self, dst_audio_folder):
        self._dst_audio_folder = dst_audio_folder

    def synch_crop(
        self,
    ):
        bvh_names = natsort.natsorted(os.listdir(self._bvh_folder))
        audio_names = natsort.natsorted(os.listdir(self._audio_folder))
        init_motion_file = os.path.join(self._bvh_folder, bvh_names[0])

        from core.skeleton import Skeleton, Motion

        skeleton = Skeleton(name="skel")
        skeleton.load_hierarchy_from_bvh(init_motion_file)

        for idx in range(len(bvh_names)):
            cur_bvh = os.path.join(self._bvh_folder, bvh_names[idx])
            dst_bvh = os.path.join(self._dst_bvh_folder, bvh_names[idx])
            audio_name = bvh_names[idx][:-4] + ".wav"
            cur_audio = os.path.join(self._audio_folder, audio_name)
            dst_audio = os.path.join(self._dst_audio_folder, audio_name)
            cur_motion = Motion(skeleton, file_path=cur_bvh)
            cur_motion.load_data()
            if audio_name not in audio_names:
                self.generate_zero_sound(
                    len(cur_motion) * cur_motion.frame_time, cur_audio
                )

            synched_audio, motion, cut_idx, samplerate = self.synch(
                cur_audio, cur_motion
            )
            cut_idx2, cropped_audio = self.crop_front(synched_audio, motion, samplerate)

            self.save_cropped_bvh(cur_bvh, dst_bvh, idx_st=cut_idx + cut_idx2)
            self.save_cropped_audio(cropped_audio, samplerate, dst_audio)
            # break

    def save_cropped_bvh(self, bvh_file, dst_file, idx_st=0, idx_end=None):
        inputFile = open(bvh_file, "r")
        exportFile = open(dst_file, "w")

        writable_line = []
        cnt = 0
        while True:
            line = inputFile.readline()
            writable_line.append(line)
            if not line:
                break
            if line[:6].upper() == "FRAMES":
                time_changer = cnt
            if line[:10].upper() == "FRAME TIME":
                break
            cnt += 1

        cnt = 0
        write_cnt = 0
        frames = []
        while True:
            line = inputFile.readline()
            if not line:
                break
            if cnt >= idx_st and idx_end is None:
                writable_line.append(line)
                write_cnt += 1
            elif cnt >= idx_st and cnt < idx_end:
                writable_line.append(line)
                write_cnt += 1
            cnt += 1

        for i, line in enumerate(writable_line):
            if i == time_changer:
                line = "Frames: " + str(write_cnt) + "\n"

            exportFile.write(line)

        inputFile.close()
        exportFile.close()

    def save_cropped_audio(self, audio, sr, dst_file):
        import scipy.io.wavfile as wavfile

        wavfile.write(dst_file, sr, audio)

    def generate_zero_sound(self, sec, dst_file):
        sr = 22050
        pad = 2000
        audio = np.zeros(int(sr * sec) + pad)
        import scipy.io.wavfile as wavfile

        wavfile.write(dst_file, sr, audio)

    def synch(self, audio, motion):
        """
        Synchronize using onset detection from the sound and hand motion from the motion
        Clap and Motion synch
        Set them as 0th frame
        """
        # Audio synch
        import librosa

        data, samplerate = librosa.load(audio)
        raw_onset = librosa.onset.onset_detect(
            y=data, sr=samplerate, units="samples", delta=0.3
        )
        if len(raw_onset) > 0:
            synched_audio = data[raw_onset[0] :]
        else:
            synched_audio = data
        # print(raw_onset[0])

        # Motion synch
        init_frame = motion[0]
        init_left_hand = init_frame.get_component_transform_by_name(
            "LeftHand"
        ).translation[2]
        init_right_hand = init_frame.get_component_transform_by_name(
            "RightHand"
        ).translation[2]

        init_diff = init_left_hand - init_right_hand
        min_diff = init_diff
        move_thresh = 0.05
        cut_idx = 0

        for i in range(1, len(motion)):
            frame = motion[i]
            left_hand = frame.get_component_transform_by_name("LeftHand").translation[2]
            right_hand = frame.get_component_transform_by_name("RightHand").translation[
                2
            ]
            diff = left_hand - right_hand
            if diff < min_diff:
                min_diff = diff
            elif diff < init_diff - move_thresh:
                motion.cut_frame(idx_st=i - 1)
                cut_idx = i - 1
                break

        return synched_audio, motion, cut_idx, samplerate

    def crop_front(self, synched_audio, synched_motion, sr):
        """
        Detect the lowest hand motion to crop the motion
        """
        audio_fr = sr * synched_motion.frame_time
        vel_thr = 10
        cut_idx2 = 0
        clap_buffer = 30
        start_buffer = 6
        stopped = False

        """
        Method 1 : Only crop using the lowest hand motion
        """
        frame = synched_motion[0]
        left_hand = frame.get_component_transform_by_name("LeftHand").translation[1]
        right_hand = frame.get_component_transform_by_name("RightHand").translation[1]
        init_hand = left_hand + right_hand
        min_hand = init_hand
        epsilon = 0.10

        for i in range(0, len(synched_motion)):
            frame = synched_motion[i]
            if stopped:
                break

            else:
                left_hand = frame.get_component_transform_by_name(
                    "LeftHand"
                ).translation[1]
                right_hand = frame.get_component_transform_by_name(
                    "RightHand"
                ).translation[1]
                tot_hand = left_hand + right_hand
                if tot_hand < min_hand:
                    min_hand = tot_hand
                elif tot_hand < init_hand - epsilon:
                    cut_idx2 = i
                    break

        # Step 3: Pad the buffer
        # cut_idx2 += start_buffer
        cropped_audio = synched_audio[int(cut_idx2 * audio_fr) :]
        return cut_idx2, cropped_audio

    def force_crop_back(
        self,
    ):
        """
        뒤의 frame 자르는 코드 --> 이전에는 눈으로 index 보고 자름
        지금은 쓰지 말것
        """
        bvh_names = natsort.natsorted(os.listdir(self._bvh_folder))
        init_motion_file = os.path.join(self._bvh_folder, bvh_names[0])

        from core.skeleton import Skeleton, Motion

        skeleton = Skeleton(name="skel")
        skeleton.load_hierarchy_from_bvh(init_motion_file)

        cut_indices = [23538, 9369, 28809, 13000, 17833, 24211, 28103]
        audio_fr = 0

        for idx in range(len(bvh_names)):
            cur_bvh = os.path.join(self._bvh_folder, bvh_names[idx])
            dst_bvh = os.path.join(self._dst_bvh_folder, bvh_names[idx])
            audio_name = bvh_names[idx][:-4] + ".wav"
            cur_audio = os.path.join(audio_folder, audio_name)
            dst_audio = os.path.join(self._dst_audio_folder, audio_name)
            cut_idx = cut_indices[idx]
            import librosa

            data, samplerate = librosa.load(cur_audio)
            if idx == 0:
                cur_motion = Motion(skeleton, file_path=cur_bvh)
                cur_motion.load_data()
                audio_fr = samplerate * cur_motion.frame_time
            cropped_audio = data[: int((cut_idx - 1) * audio_fr) + 1]

            self.save_cropped_bvh(cur_bvh, dst_bvh, idx_end=cut_idx)
            self.save_cropped_audio(cropped_audio, samplerate, dst_audio)


if __name__ == "__main__":
    audio_folder = "/path/to/audio"
    bvh_folder = "/path/to/bvh"
    ams = Single_audio_motion_synch()
    ams.synch_crop()
    # ams.force_crop_back()
