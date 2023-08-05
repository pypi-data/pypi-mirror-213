import math
from re import L

import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from vaaibody.viewer.obj_loader import HEAD_OBJ, HEAD_OBJ_SIZE, HEAD_BOX

import math

quad_obj = gluNewQuadric()


class Color:
    colors = []
    colors.append([0.3, 0.3, 0.3])
    colors.append([247.0 / 255.0, 191.0 / 255.0, 55.0 / 255.0])
    colors.append([215.0 / 255.0, 57.0 / 255.0, 55.0 / 255.0])
    colors.append([49.0 / 255.0, 130.0 / 255.0, 225.0 / 255.0])
    colors.append([45.0 / 255.0, 195.0 / 255.0, 46.0 / 255.0])
    colors.append([219.0 / 255.0, 84.0 / 255.0, 162.0 / 255.0])
    colors.append([184.0 / 255.0, 108.0 / 255.0, 76.0 / 255.0])
    colors.append([46.0 / 255.0, 168.0 / 255.0, 238.0 / 255.0])
    colors.append([254.0 / 255.0, 128.0 / 255.0, 35.0 / 255.0])
    colors.append([41.0 / 255.0, 173.0 / 255.0, 119.0 / 255.0])
    colors.append([174.0 / 255.0, 73.0 / 255.0, 201.0 / 255.0])


def draw_hand(current_hand_frame, connection, color):
    # Must contains alpha
    if len(color) == 3:
        color.append(0.5)
    glColor4f(*color)
    glLineWidth(5.0)
    for pair in connection:
        glBegin(GL_LINES)
        glVertex3f(*current_hand_frame.get_joint_3d(pair[0]) + np.array([0.0, 0, 0.0]))
        glVertex3f(*current_hand_frame.get_joint_3d(pair[1]) + np.array([0.0, 0, 0.0]))
        glEnd()
        glPushMatrix()
        glTranslatef(*current_hand_frame.get_joint_3d(pair[0]))
        draw_sphere(0.001)
        glPopMatrix()


def draw_skeleton(skel, current_frame, color, shape_type="box"):
    glColor4f(*color)
    if shape_type == "line":
        glLineWidth(5.0)
        for idx, j in enumerate(skel.joints):
            if j.parent is not None:
                glColor4f(*color)
                idx_p = skel.joint_dict[j.parent.name]
                glBegin(GL_LINES)
                glVertex3f(*current_frame.get_global_transform(idx_p).translation)
                glVertex3f(*current_frame.get_global_transform(idx).translation)
                glEnd()
                glPushMatrix()
                glTranslatef(*current_frame.get_global_transform(idx).translation)
                draw_sphere(0.01)
                glPopMatrix()
            if j._is_end:
                glColor4f(*color)
                end_trans = np.matmul(
                    current_frame.get_global_transform(idx).rotation_np,
                    j._end_site_transform.translation,
                )
                glBegin(GL_LINES)
                glVertex3f(*current_frame.get_global_transform(idx).translation)
                glVertex3f(
                    *current_frame.get_global_transform(idx).translation + end_trans
                )
                glEnd()

            # Draw Head and gaze direction
            if j.name == "Head":
                glColor3f(0, 1.0, 0)
                end_trans = np.matmul(
                    current_frame.get_global_transform(idx).rotation_np,
                    j._end_site_transform.translation,
                )
                head = (
                    current_frame.get_global_transform(idx).translation + end_trans / 2
                )
                # glColor3f(1.0, 0, 0)
                x_axis = np.matmul(
                    current_frame.get_global_transform(idx).rotation_np,
                    np.array([0, 0, 0.1]),
                )
                euler = current_frame.get_global_transform(idx).rotation.as_euler(
                    "ZXY", degrees=True
                )
                # draw_arrow(head, head + x_axis, 0.01)
                draw_head(head, euler)

    else:
        for idx, j in enumerate(skel.joints):
            body_pose = current_frame.get_body_global_transform(idx)
            # body_pose = current_frame.get_global_transform(idx) * skel.joints[idx].body_transform
            orientation = body_pose.rotation.as_rotvec()
            center = body_pose.translation
            glPushMatrix()
            glTranslatef(*(center))
            glRotatef(
                np.linalg.norm(orientation) / math.pi * 180,
                *(orientation / np.linalg.norm(orientation))
            )
            if shape_type == "capsule":
                draw_capsule(
                    skel.joints[idx]._body_radius, skel.joints[idx]._body_height
                )
            elif shape_type == "box":
                draw_box(
                    [
                        skel.joints[idx]._body_radius,
                        skel.joints[idx]._body_height / 2.0,
                        skel.joints[idx]._body_radius,
                    ]
                )
            glPopMatrix()


def draw_fixed_skeleton(skel, current_frame, color):
    glColor4f(*color)
    glLineWidth(5.0)
    original_root = current_frame.get_root_transform()
    original_root.translation[0] = 0
    original_root.translation[1] = 0
    original_root.translation[2] = 0
    current_frame.set_root_transform(original_root)
    for idx, j in enumerate(skel.joints):
        if j.parent is not None:
            idx_p = skel.joint_dict[j.parent.name]
            glBegin(GL_LINES)
            glVertex3f(*current_frame.get_global_transform(idx_p).translation)
            glVertex3f(*current_frame.get_global_transform(idx).translation)
            glEnd()
        if j._is_end:
            end_trans = np.matmul(
                current_frame.get_global_transform(idx).rotation_np,
                j._end_site_transform.translation,
            )
            glBegin(GL_LINES)
            glVertex3f(*current_frame.get_global_transform(idx).translation)
            glVertex3f(*current_frame.get_global_transform(idx).translation + end_trans)
            glEnd()


def draw_head(start, euler):
    # glColor3f(0, 0, 0)
    scaled_size = 0.26
    scene_scale = [scaled_size / HEAD_OBJ_SIZE[1] for i in range(3)]
    scene_trans = np.array([-(HEAD_BOX[1][i] + HEAD_BOX[0][i]) / 2 for i in range(3)])
    scene_trans_offset = np.zeros(3)
    scene_trans_offset += start / scene_scale
    scene_trans_offset[0] += 0.1
    scene_trans_offset[1] -= 0.25

    glColor4f(0.7, 0.2, 0.2, 0.25)
    # scene_trans +
    glPushMatrix()
    glScalef(*scene_scale)
    glTranslatef(*scene_trans)
    glTranslatef(*scene_trans_offset)
    glRotatef(euler[0], 0, 0, 1)
    glRotatef(euler[1], 1, 0, 0)
    glRotatef(euler[2], 0, 1, 0)

    glRotatef(-90, 0, 1, 0)
    glRotatef(180, 1, 0, 0)
    glRotatef(10, 0, 0, 1)

    for mesh in HEAD_OBJ.mesh_list:
        glBegin(GL_TRIANGLES)
        for face in mesh.faces:
            # glColor
            for vertex_i in face:
                glVertex3f(*HEAD_OBJ.vertices[vertex_i])
        glEnd()
    glPopMatrix()


def draw_ground(center=np.zeros(3)):
    start = -30
    end = 30
    interval = 30

    glColor4f(1.0, 1.0, 1.0, 0.36)
    glBegin(GL_QUADS)
    for i in range(start, end, interval):
        for j in range(start, end, interval):
            i_ = i + center[0]
            j_ = j + center[2]
            glNormal3f(0.0, 1.0, 0.0)
            glVertex3f(i_, 0.0, j_)
            glVertex3f(i_, 0.0, j_ + interval)
            glVertex3f(i_ + interval, 0.0, j_ + interval)
            glVertex3f(i_ + interval, 0.0, j_)
    glEnd()
    start = -30
    end = 30
    interval = 1
    c_x = int(center[0])
    c_z = int(center[2])
    glColor3f(0.05, 0.05, 0.05)
    glLineWidth(1.2)
    for i in range(start, end, interval):
        glBegin(GL_LINES)
        glNormal3f(0.0, 1.0, 0.0)
        glVertex3f(c_x + i, 0.01, c_z + start)
        glNormal3f(0.0, 1.0, 0.0)
        glVertex3f(c_x + i, 0.01, c_z + end)

        glNormal3f(0.0, 1.0, 0.0)
        glVertex3f(c_x + start, 0.01, c_z + i)
        glNormal3f(0.0, 1.0, 0.0)
        glVertex3f(c_x + end, 0.01, c_z + i)
        glEnd()

    # draw wall
    glColor3f(0.9, 0.9, 0.9)
    glBegin(GL_QUADS)
    glNormal3f(1.0, 0.0, 0.0)
    glVertex3f(center[0] - 100.0, -100.0, -100.0 + center[1])
    glNormal3f(1.0, 0.0, 0.0)
    glVertex3f(center[0] - 100.0, 100.0, -100.0 + center[1])
    glNormal3f(1.0, 0.0, 0.0)
    glVertex3f(center[0] - 100.0, 100.0, 100.0 + center[1])
    glNormal3f(1.0, 0.0, 0.0)
    glVertex3f(center[0] - 100.0, -100.0, 100.0 + center[1])

    glNormal3f(-1.0, 0.0, 0.0)
    glVertex3f(center[0] + 100.0, -100.0, -100.0 + center[1])
    glNormal3f(-1.0, 0.0, 0.0)
    glVertex3f(center[0] + 100.0, 100.0, -100.0 + center[1])
    glNormal3f(-1.0, 0.0, 0.0)
    glVertex3f(center[0] + 100.0, 100.0, 100.0 + center[1])
    glNormal3f(-1.0, 0.0, 0.0)
    glVertex3f(center[0] + 100.0, -100.0, 100.0 + center[1])

    glNormal3f(0.0, 0.0, 1.0)
    glVertex3f(center[0] - 100.0, -100.0, -100.0 + center[1])
    glNormal3f(0.0, 0.0, 1.0)
    glVertex3f(center[0] - 100.0, 100.0, -100.0 + center[1])
    glNormal3f(0.0, 0.0, 1.0)
    glVertex3f(center[0] + 100.0, 100.0, -100.0 + center[1])
    glNormal3f(0.0, 0.0, 1.0)
    glVertex3f(center[0] + 100.0, -100.0, -100.0 + center[1])

    glNormal3f(0.0, 0.0, -1.0)
    glVertex3f(center[0] - 100.0, -100.0, 100.0 + center[1])
    glNormal3f(0.0, 0.0, -1.0)
    glVertex3f(center[0] - 100.0, 100.0, 100.0 + center[1])
    glNormal3f(0.0, 0.0, -1.0)
    glVertex3f(center[0] + 100.0, 100.0, 100.0 + center[1])
    glNormal3f(0.0, 0.0, -1.0)
    glVertex3f(center[0] + 100.0, -100.0, 100.0 + center[1])
    glEnd()


def init_lights(center=np.zeros(3)):
    ambient0 = [0.15, 0.15, 0.15, 1.0]
    diffuse0 = [0.2, 0.2, 0.2, 1.0]
    specular0 = [0.1, 0.1, 0.1, 1.0]
    position0 = [0.0, 3.0, 0.0, 1.0]
    position0[0] = center[0]
    position0[2] = center[2]

    # diffuse_tmp = []
    # diffuse_tmp = glGetLightfv(GL_LIGHT0, GL_DIFFUSE)
    # print(diffuse_tmp)

    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambient0)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse0)
    glLightfv(GL_LIGHT0, GL_SPECULAR, specular0)
    glLightfv(GL_LIGHT0, GL_POSITION, position0)
    glLightf(GL_LIGHT0, GL_SPOT_CUTOFF, 30.0)
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 2.0)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 1.0)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 1.0)

    ambient1 = [0.02, 0.02, 0.02, 1.0]
    diffuse1 = [0.01, 0.01, 0.01, 1.0]
    specular1 = [0.01, 0.01, 0.01, 1.0]
    position1 = [0.0, 1.0, -1.0, 0.0]

    glEnable(GL_LIGHT1)
    glLightfv(GL_LIGHT1, GL_AMBIENT, ambient1)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, diffuse1)
    glLightfv(GL_LIGHT1, GL_SPECULAR, specular1)
    glLightfv(GL_LIGHT1, GL_POSITION, position1)
    glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, 2.0)
    glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, 1.0)
    glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, 1.0)

    glEnable(GL_LIGHTING)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    # glColorMaterial(GL_FRONT_AND_BACK, GL_SPECULAR);
    glEnable(GL_COLOR_MATERIAL)

    front_mat_shininess = [24.0]
    front_mat_specular = [0.2, 0.2, 0.2, 1.0]
    front_mat_diffuse = [0.2, 0.2, 0.2, 1.0]
    glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, front_mat_shininess)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, front_mat_specular)
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, front_mat_diffuse)

    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glDisable(GL_CULL_FACE)
    glEnable(GL_NORMALIZE)


def draw_transform(transform, scale=1):
    ori = transform.translation
    ori_x = transform.apply(np.array([1, 0, 0]) * scale)
    ori_y = transform.apply(np.array([0, 1, 0]) * scale)
    ori_z = transform.apply(np.array([0, 0, 1]) * scale)

    glLineWidth(10)
    glPushMatrix()
    glTranslatef(0.0, 0.05, 0.0)
    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_LINES)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(1.0, 0.0, 0.0)
    glEnd()
    glPopMatrix()
    glPushMatrix()
    glTranslatef(0.0, 0.05, 0.0)
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_LINES)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 1.0, 0.0)
    glEnd()
    glPopMatrix()
    glPushMatrix()
    glTranslatef(0.0, 0.05, 0.0)
    glColor3f(0.0, 0.0, 1.0)
    glBegin(GL_LINES)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 1.0)
    glEnd()
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.0, 0.05, 0.0)
    glLineWidth(5.0)
    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_LINES)
    glVertex3f(*ori)
    glVertex3f(*ori_x)
    glEnd()
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.0, 0.05, 0.0)
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_LINES)
    glVertex3f(*ori)
    glVertex3f(*ori_y)
    glEnd()
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.0, 0.05, 0.0)
    glColor3f(0.0, 0.0, 1.0)
    glBegin(GL_LINES)
    glVertex3f(*ori)
    glVertex3f(*ori_z)
    glEnd()
    glPopMatrix()


def draw_sphere(radius, resolution=8):
    global quad_obj

    gluQuadricDrawStyle(quad_obj, GLU_FILL)
    gluQuadricNormals(quad_obj, GLU_SMOOTH)

    gluSphere(quad_obj, radius, resolution, resolution)


def draw_dome(radius, num_slices=8, num_stacks=4):
    # draw top

    glBegin(GL_TRIANGLE_FAN)
    glNormal3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, radius, 0.0)

    y = math.cos(0.5 * math.pi / num_stacks)
    r_xz = math.sin(0.5 * math.pi / num_stacks)
    for i in range(num_slices + 1):
        z = r_xz * math.cos(2 * math.pi * i / num_slices)
        x = r_xz * math.sin(2 * math.pi * i / num_slices)

        glNormal3f(x, y, z)
        glVertex3f(radius * x, radius * y, radius * z)

    glEnd()

    # draw remainder
    glBegin(GL_TRIANGLE_STRIP)
    for j in range(1, num_stacks):
        y_0 = math.cos(0.5 * math.pi * j / num_stacks)
        y_1 = math.cos(0.5 * math.pi * (j + 1) / num_stacks)

        r_xz_0 = math.sin(0.5 * math.pi * j / num_stacks)
        r_xz_1 = math.sin(0.5 * math.pi * (j + 1) / num_stacks)

        for i in range(num_slices + 1):
            z_0 = r_xz_0 * math.cos(2 * math.pi * i / num_slices)
            x_0 = r_xz_0 * math.sin(2 * math.pi * i / num_slices)

            z_1 = r_xz_1 * math.cos(2 * math.pi * i / num_slices)
            x_1 = r_xz_1 * math.sin(2 * math.pi * i / num_slices)
            glNormal3f(x_0, y_0, z_0)
            glVertex3f(radius * x_0, radius * y_0, radius * z_0)

            glNormal3f(x_1, y_1, z_1)
            glVertex3f(radius * x_1, radius * y_1, radius * z_1)
    glEnd()


def draw_cylinder(radius, height, resolution=8):
    glPushMatrix()
    glRotatef(90.0, 1.0, 0.0, 0.0)
    glTranslatef(0, 0, -height / 2)

    gluQuadricDrawStyle(quad_obj, GLU_FILL)
    gluQuadricNormals(quad_obj, GLU_SMOOTH)

    gluCylinder(quad_obj, radius, radius, height, resolution, resolution)
    glPopMatrix()


def draw_capsule(radius, height):
    if height - 2 * radius > 1e-6:
        draw_cylinder(radius, height - 2 * radius)
        glPushMatrix()
        glTranslatef(0.0, height / 2 - radius, 0.0)
        draw_dome(radius)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(0.0, -height / 2 + radius, 0.0)
        glRotatef(180.0, 1.0, 0.0, 0.0)
        draw_dome(radius)
        glPopMatrix()
    else:
        draw_sphere(min(radius, height / 2))


def draw_box(size):
    glPushMatrix()
    glScalef(*size)
    glBegin(GL_QUADS)
    glNormal3f(1, 0, 0)
    glVertex3f(1, 1, 1)
    glVertex3f(1, -1, 1)
    glVertex3f(1, -1, -1)
    glVertex3f(1, 1, -1)

    glNormal3f(-1, 0, 0)
    glVertex3f(-1, 1, 1)
    glVertex3f(-1, -1, 1)
    glVertex3f(-1, -1, -1)
    glVertex3f(-1, 1, -1)

    glNormal3f(0, 1, 0)
    glVertex3f(1, 1, 1)
    glVertex3f(-1, 1, 1)
    glVertex3f(-1, 1, -1)
    glVertex3f(1, 1, -1)

    glNormal3f(0, -1, 0)
    glVertex3f(1, -1, 1)
    glVertex3f(-1, -1, 1)
    glVertex3f(-1, -1, -1)
    glVertex3f(1, -1, -1)

    glNormal3f(0, 0, 1)
    glVertex3f(1, 1, 1)
    glVertex3f(1, -1, 1)
    glVertex3f(-1, -1, 1)
    glVertex3f(-1, 1, 1)

    glNormal3f(0, 0, -1)
    glVertex3f(1, 1, -1)
    glVertex3f(1, -1, -1)
    glVertex3f(-1, -1, -1)
    glVertex3f(-1, 1, -1)
    glEnd()
    glPopMatrix()


def draw_arrow(start, end, rad):
    direction = end - start
    dist = np.linalg.norm(direction)
    arrow_length = 0.1 * dist

    direction /= dist

    gluQuadricDrawStyle(quad_obj, GLU_FILL)
    gluQuadricNormals(quad_obj, GLU_SMOOTH)

    glPushMatrix()
    glTranslatef(*start)
    glRotatef(math.acos(direction[2]) * 180 / math.pi, -direction[1], direction[0], 0)
    gluCylinder(quad_obj, rad, rad, dist - arrow_length, 8, 8)

    glTranslatef(0, 0, dist - arrow_length)
    gluCylinder(quad_obj, rad * 1.5, 0.0, arrow_length, 8, 8)

    glPopMatrix()
