import os

from core.motion import Motion
from tqdm import tqdm


class Exporter:
    def __init__(self, sample, path=None, file_name=None):
        self.sample_bvh = sample
        if path is not None and file_name is not None:
            if not os.path.exists(path):
                os.makedirs(path)
            self.file_path = path + file_name
        elif path is None:
            self.file_path = None
        else:
            self.file_path = path
        self.hierarchy = None
        if os.path.isfile(self.sample_bvh):
            self.hierarchy_from_sample()

    def change_path(self, path):
        if os.path.isfile(path):
            cnt = int(path[-6:-4])
            cnt += 1
            if cnt >= 10:
                str_cnt = str(cnt)
            else:
                str_cnt = "0" + str(cnt)
            path = path[:-6] + str_cnt + ".bvh"
        self.file_path = path

    def hierarchy_from_sample(
        self,
    ):
        self.hierarchy = []
        sample = open(self.sample_bvh, "r")
        while True:
            line = sample.readline()
            self.hierarchy.append(line)
            if not line:
                break
            if line[:10].upper() == "FRAME TIME":
                break

    def init_export(self, len_motion, reduce_dof=False):
        self.exportFile = open(self.file_path, "w")
        for line in self.hierarchy:
            if line[:6].upper() == "FRAMES":
                new_line = line[:8] + str(len_motion) + "\n"
                self.exportFile.write(new_line)
            else:
                self.exportFile.write(line)

    def export_single_frame(self, frame, XYZ=False, DOF_6=False):
        local_tranl = []
        if DOF_6:
            for i in range(len(self.hierarchy)):
                line = self.hierarchy[i]
                line = line.strip()
                if line[:5].upper() == "JOINT":
                    next_line = self.hierarchy[i + 2].strip()
                    _, x, y, z = next_line.split(" ")
                    local_tranl.append([x, y, z])

        global_trans = frame.get_root_transform() * frame.get_local_transform(0)
        translate = global_trans.translation * 100
        if XYZ:
            rotate = global_trans.rotation.as_euler("XYZ", degrees=True)
        else:
            rotate = global_trans.rotation.as_euler("ZXY", degrees=True)
        self.exportFile.write(format(translate[0], ".6f") + " ")
        self.exportFile.write(format(translate[1], ".6f") + " ")
        self.exportFile.write(format(translate[2], ".6f") + " ")
        self.exportFile.write(format(rotate[0], ".6f") + " ")
        self.exportFile.write(format(rotate[1], ".6f") + " ")
        self.exportFile.write(format(rotate[2], ".6f") + " ")

        local = frame.get_local_transforms()
        for i, loci in enumerate(local):
            if i == 0:
                continue
            if XYZ:
                degree = loci.rotation.as_euler("XYZ", degrees=True)
            else:
                degree = loci.rotation.as_euler("ZXY", degrees=True)
            if DOF_6:
                for j in range(3):
                    self.exportFile.write(str(100 * loci.translation[j]) + " ")
            self.exportFile.write(format(degree[0], ".6f") + " ")
            self.exportFile.write(format(degree[1], ".6f") + " ")
            self.exportFile.write(format(degree[2], ".6f") + " ")
        self.exportFile.write("\n")

    def export_frames(self, frame_list, DOF_6=False):
        for frame in frame_list:
            self.export_single_frame(frame, DOF_6=DOF_6)
        self.exportFile.close()

    def export_motion(self, motion: Motion, XYZ=False, DOF_6=False):
        for i in range(len(motion)):
            self.export_single_frame(motion[i], XYZ, DOF_6)
        self.exportFile.close()

    def export_angles(self, angles):
        pass

    def change_frame_time(self, motion_file, motion_size):
        src = motion_file
        dst = self.file_path
        inputFile = open(src, "r")
        exportFile = open(dst, "w")
        for line in inputFile:
            if line[:6].upper() == "FRAMES":
                new_line = line[:8] + str(motion_size) + "\n"
                exportFile.write(new_line)
            else:
                exportFile.write(line)

        inputFile.close()
        exportFile.close()


def export_db(db, path, sample, XYZ=False, DOF_6=False) -> None:
    path = path[:-1] + "_upper/"
    if not os.path.isdir(path):
        os.makedirs(path)
    # exporter = Exporter("data/motion/cropped/cropped_VAAI_Basic_01_01.bvh")
    exporter = Exporter(sample)
    for i in tqdm(range(db.num_motion())):
        motion = db.get_motion(i)
        motion_file = motion.file_path
        motion_name = motion_file.split("/")[-1]
        exporter.change_path(path + motion_name)
        exporter.init_export(len(motion))
        exporter.export_motion(motion, XYZ, DOF_6)


def change_frametime_db(db, path, sample) -> None:
    if not os.path.isdir(path):
        os.makedirs(path)
    exporter = Exporter(sample)
    for i in tqdm(range(db.num_motion())):
        motion = db.get_motion(i)
        motion_file = motion.file_path
        motion_name = motion_file.split("/")[-1]
        exporter.change_path(path + motion_name)
        exporter.change_frame_time(motion_file, len(motion))
