import arcade as arc
import random

MAX_X = round(640 * 1)
MAX_Y = round(640 * 1)

WIDTH = 10
HEIGHT = 10

BLOCK_OPACITY = [0, 16, 8, 4, 0,
                 16, 0, 8, 16, 0,
                 0, 8, 0, 0, 0]
BLOCK_REFLECTANCE = [[14, 15, 16], [9, 12, 6], [5, 8, 12], [3, 8, 3], [16, 16, 16],
                     [16, 16, 16], [16, 16, 16], [16, 16, 16], [16, 16, 16], [16, 16, 16],
                     [16, 0, 0], [16, 0, 0], [16, 0, 0], [0, 16, 16], [16, 16, 0]]
BLOCK_EMISSION = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                  [16, 16, 16], [16, 0, 0], [0, 16, 0], [0, 0, 16], [12, 9, 6],
                  [0, 0, 0], [0, 0, 0], [0, 16, 0], [0, 0, 0], [0, 0, 0]]

MAX_LIGHT = 16
TYPES = 2  # 0 - sunlight RGB, 1 - block RGB
AIR_ID = 0


class Canvas(arc.Window):

    def __init__(self):
        super().__init__(MAX_X, MAX_Y, "Main World")
        arc.set_background_color((0, 0, 0))

        self.global_light = [16, 16, 16]

        self.block_id = [[0 for y in range(HEIGHT)] for x in range(WIDTH)]
        self.light_val = [[[[0 for c in range(3)] for t in range(TYPES)] for y in range(HEIGHT)] for x in range(WIDTH)]

        self.view_mode = 0
        self.target_x = 0
        self.target_y = 0

        self.face_check = [[1, 0], [0, 1], [-1, 0], [0, -1]]

    def setup(self):
        self.target_x = 0
        self.target_y = 0

        self.populate()

    def update(self, delta_time):
        pass

    def on_draw(self):
        arc.start_render()

        for x in range(WIDTH):
            for y in range(HEIGHT):
                light = [max(self.light_val[x][y][0][0], self.light_val[x][y][1][0]) / MAX_LIGHT,
                         max(self.light_val[x][y][0][1], self.light_val[x][y][1][1]) / MAX_LIGHT,
                         max(self.light_val[x][y][0][2], self.light_val[x][y][1][2]) / MAX_LIGHT]
                reflectance = [self.to_clr(BLOCK_REFLECTANCE[self.block_id[x][y]][i]) for i in range(3)]

                if self.view_mode == 0:
                    arc.draw_rectangle_filled(self.to_px(x + 0.5), self.to_py(y + 0.5), self.to_px(1), self.to_py(1),
                                              [int(reflectance[i] * light[i]) for i in range(3)])
                elif self.view_mode == 1:
                    arc.draw_rectangle_filled(self.to_px(x + 0.5), self.to_py(y + 0.5), self.to_px(1), self.to_py(1),
                                              [int(reflectance[0] * self.light_val[x][y][1][0] / MAX_LIGHT), 0, 0])
                elif self.view_mode == 2:
                    arc.draw_rectangle_filled(self.to_px(x + 0.5), self.to_py(y + 0.5), self.to_px(1), self.to_py(1),
                                              [0, int(reflectance[1] * self.light_val[x][y][1][1] / MAX_LIGHT), 0])
                elif self.view_mode == 3:
                    arc.draw_rectangle_filled(self.to_px(x + 0.5), self.to_py(y + 0.5), self.to_px(1), self.to_py(1),
                                              [0, 0, int(reflectance[2] * self.light_val[x][y][1][2] / MAX_LIGHT)])
                elif self.view_mode == 4:
                    arc.draw_rectangle_filled(self.to_px(x + 0.5), self.to_py(y + 0.5), self.to_px(1), self.to_py(1),
                                              [int(reflectance[i] * self.light_val[x][y][1][i] / MAX_LIGHT) for i in range(3)])
                elif self.view_mode == 5:
                    reflectance[0] = 255 * max(self.light_val[x][y][0][0], self.light_val[x][y][0][1], self.light_val[x][y][0][2]) / MAX_LIGHT
                    reflectance[1] = 255 * max(self.light_val[x][y][1][0], self.light_val[x][y][1][1], self.light_val[x][y][1][2]) / MAX_LIGHT
                    reflectance[2] = 0
                    arc.draw_rectangle_filled(self.to_px(x + 0.5), self.to_py(y + 0.5), self.to_px(1), self.to_py(1), reflectance)

        arc.draw_rectangle_outline(self.to_px(self.target_x + 0.5), self.to_py(self.target_y + 0.5), self.to_px(1),
                                   self.to_py(1), [255, 0, 0])

    def on_key_press(self, key, modifiers):
        if key == arc.key.LEFT:
            if self.target_x > 0:
                self.target_x -= 1
        if key == arc.key.RIGHT:
            if self.target_x < WIDTH - 1:
                self.target_x += 1
        if key == arc.key.DOWN:
            if self.target_y > 0:
                self.target_y -= 1
        if key == arc.key.UP:
            if self.target_y < HEIGHT - 1:
                self.target_y += 1

        if key == arc.key.KEY_1:
            self.modify_voxel(self.target_x, self.target_y, 0)
        if key == arc.key.KEY_2:
            self.modify_voxel(self.target_x, self.target_y, 1)
        if key == arc.key.KEY_3:
            self.modify_voxel(self.target_x, self.target_y, 3)
        if key == arc.key.KEY_4:
            self.modify_voxel(self.target_x, self.target_y, 5)
        if key == arc.key.KEY_5:
            self.modify_voxel(self.target_x, self.target_y, 6)
        if key == arc.key.KEY_6:
            self.modify_voxel(self.target_x, self.target_y, 7)
        if key == arc.key.KEY_7:
            self.modify_voxel(self.target_x, self.target_y, 9)
        if key == arc.key.KEY_8:
            self.modify_voxel(self.target_x, self.target_y, 10)
        if key == arc.key.KEY_9:
            self.modify_voxel(self.target_x, self.target_y, 11)
        if key == arc.key.KEY_0:
            self.modify_voxel(self.target_x, self.target_y, 12)

        old_global_light = [self.global_light[i] for i in range(3)]
        if key == arc.key.A and self.global_light[0] < MAX_LIGHT:
            self.global_light[0] += 1
        if key == arc.key.Z and self.global_light[0] > 0:
            self.global_light[0] -= 1
        if key == arc.key.S and self.global_light[1] < MAX_LIGHT:
            self.global_light[1] += 1
        if key == arc.key.X and self.global_light[1] > 0:
            self.global_light[1] -= 1
        if key == arc.key.D and self.global_light[2] < MAX_LIGHT:
            self.global_light[2] += 1
        if key == arc.key.C and self.global_light[2] > 0:
            self.global_light[2] -= 1
        if old_global_light[0] != self.global_light[0] or old_global_light[1] != self.global_light[1] or old_global_light[2] != self.global_light[2]:
            self.relight()

        if key == arc.key.Q:
            self.view_mode = 0
        if key == arc.key.W:
            self.view_mode = 1
        if key == arc.key.E:
            self.view_mode = 2
        if key == arc.key.R:
            self.view_mode = 3
        if key == arc.key.T:
            self.view_mode = 4
        if key == arc.key.Y:
            self.view_mode = 5

    def populate(self):
        emission_to_check_x = []
        emission_to_check_y = []
        for vx in range(WIDTH):
            terrain_height = HEIGHT / 2  # + random.randint(-2, 1)
            for vy in range(HEIGHT):
                if vy == terrain_height:
                    if vx != 8:
                        self.block_id[vx][vy] = 1
                else:
                    if vx == 2 and vy == 2:
                        self.block_id[vx][vy] = 6
                    else:
                        self.block_id[vx][vy] = 0

                vox_id = self.block_id[vx][vy]
                if BLOCK_EMISSION[vox_id][0] + BLOCK_EMISSION[vox_id][1] + BLOCK_EMISSION[vox_id][2] > 0:
                    emission_to_check_x.append(vx)
                    emission_to_check_y.append(vy)

        while len(emission_to_check_x) > 0:
            vx = emission_to_check_x.pop(0)
            vy = emission_to_check_y.pop(0)

            vox_id = self.block_id[vx][vy]
            if BLOCK_EMISSION[vox_id][0] > 0:
                self.check_max_light(vx, vy, 1, 0)
            if BLOCK_EMISSION[vox_id][1] > 0:
                self.check_max_light(vx, vy, 1, 1)
            if BLOCK_EMISSION[vox_id][2] > 0:
                self.check_max_light(vx, vy, 1, 2)

        for i in range(3):
            self.set_light(0, HEIGHT - 1, 0, i, self.global_light[i])

    def relight(self):
        emission_to_check_x = []
        emission_to_check_y = []
        for vx in range(WIDTH):
            for vy in range(HEIGHT):
                for c in range(3):
                    self.light_val[vx][vy][0][c] = 0
                    self.light_val[vx][vy][1][c] = 0
                vox_id = self.block_id[vx][vy]
                if BLOCK_EMISSION[vox_id][0] + BLOCK_EMISSION[vox_id][1] + BLOCK_EMISSION[vox_id][2] > 0:
                    emission_to_check_x.append(vx)
                    emission_to_check_y.append(vy)

        while len(emission_to_check_x) > 0:
            vx = emission_to_check_x.pop(0)
            vy = emission_to_check_y.pop(0)

            vox_id = self.block_id[vx][vy]
            for c in range(3):
                if BLOCK_EMISSION[vox_id][c] > 0:
                    self.check_max_light(vx, vy, 1, c)

        for i in range(3):
            self.set_light(0, HEIGHT - 1, 0, i, self.global_light[i])

    def modify_voxel(self, vx, vy, new_id):
        old_id = self.block_id[vx][vy]
        self.block_id[vx][vy] = new_id

        for i in range(3):
            if BLOCK_OPACITY[new_id] != BLOCK_OPACITY[old_id] or BLOCK_REFLECTANCE[new_id][i] != BLOCK_REFLECTANCE[old_id][i]:
                self.check_max_light(vx, vy, 0, i)
            if BLOCK_OPACITY[new_id] != BLOCK_OPACITY[old_id] or BLOCK_EMISSION[new_id][i] != BLOCK_EMISSION[old_id][i] or BLOCK_REFLECTANCE[new_id][i] != BLOCK_REFLECTANCE[old_id][i]:
                self.set_light(vx, vy, 1, i, BLOCK_EMISSION[new_id][i])
                self.check_max_light(vx, vy, 1, i)

    def set_light(self, vx, vy, t, c, value):
        old_light = self.light_val[vx][vy][t][c]
        if value != old_light:
            self.light_val[vx][vy][t][c] = value
            if value > old_light:
                self.propagate_light(vx, vy, t, c)
            elif value < old_light:
                self.propagate_light_remove(vx, vy, t, c)

    def propagate_light(self, vx, vy, t, c):
        for p in range(4):
            nx = vx + self.face_check[p][0]
            ny = vy + self.face_check[p][1]
            if self.is_in_world(nx, ny):
                cast_light = self.get_cast_light(vx, vy, nx, ny, t, c)
                if self.light_val[nx][ny][t][c] < cast_light:
                    self.set_light(nx, ny, t, c, cast_light)

    def propagate_light_remove(self, vx, vy, t, c):
        for p in range(4):
            nx = vx + self.face_check[p][0]
            ny = vy + self.face_check[p][1]
            if self.is_in_world(nx, ny):
                self.check_max_light(nx, ny, t, c)

    def check_max_light(self, vx, vy, t, c):
        max_cast = BLOCK_EMISSION[self.block_id[vx][vy]][c] if t == 1 else 0

        for p in range(4):
            nx = vx + self.face_check[p][0]
            ny = vy + self.face_check[p][1]
            if self.is_in_world(nx, ny):
                cast_light = self.get_cast_light(nx, ny, vx, vy, t, c)
                if cast_light > max_cast:
                    max_cast = cast_light

        self.set_light(vx, vy, t, c, max_cast)

    def get_cast_light(self, vx, vy, nx, ny, t, c):
        if not self.is_in_world(nx, ny):
            return

        if t == 0 and BLOCK_OPACITY[self.block_id[nx][ny]] <= BLOCK_OPACITY[AIR_ID] \
                and BLOCK_REFLECTANCE[self.block_id[nx][ny]][c] >= BLOCK_REFLECTANCE[AIR_ID][c]:
            if vy == ny and (vy + 1 > HEIGHT - 1 or self.light_val[nx][ny + 1][0][c] == self.global_light[c]):
                return self.global_light[c]

            if vx == nx and self.light_val[vx][vy][0][c] == self.global_light[c] :
                return self.global_light[c] if ny < vy else 0

        emission = BLOCK_EMISSION[self.block_id[nx][ny]][c] if t == 1 else 0
        absorption = MAX_LIGHT - BLOCK_REFLECTANCE[self.block_id[nx][ny]][c]
        opacity = BLOCK_OPACITY[self.block_id[nx][ny]]

        return min(max(self.light_val[vx][vy][t][c] + emission - absorption - opacity - 1, 0), MAX_LIGHT)

    @staticmethod
    def is_in_world(vx, vy):
        if 0 <= vx < WIDTH and 0 <= vy < HEIGHT:
            return True
        return False

    @staticmethod
    def to_px(value):
        return value * MAX_X / WIDTH

    @staticmethod
    def to_py(value):
        return value * MAX_Y / HEIGHT

    @staticmethod
    def to_clr(value):
        return int(value * 255 / 16)


def main():
    canv = Canvas()
    canv.setup()
    arc.run()


if __name__ == "__main__":
    main()