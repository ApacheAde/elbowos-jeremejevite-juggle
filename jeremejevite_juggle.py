#!/usr/bin/env python3
"""Jeremejevite Juggle — neon multi-orb arcade for ElbowOS. Python 3 + pygame."""
import math, os, random, subprocess, sys

RECORD = "--record" in sys.argv or os.environ.get("ELBOWOS_RECORD") == "1"
PLAY = "--play" in sys.argv and not RECORD
if not PLAY:
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame

W, H, FPS, SECS = 1080, 1920, 30, 15
OUT = os.environ.get("ELBOWOS_MP4", "/workspace/artifacts/JEREMEJEVITE_JUGGLE_ElbowOS.mp4")
TITLE, HANDLE = "JEREMEJEVITE JUGGLE", "x.com/ElbowOS"
INK = (6, 10, 22)
TEAL, BLUE = (46, 230, 199), (58, 160, 255)
ROSE, GOLD, VIO = (255, 93, 154), (255, 200, 87), (168, 92, 255)
WHITE = (246, 248, 255)
PAL = [TEAL, BLUE, ROSE, GOLD, VIO]


class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        flags = 0 if PLAY else pygame.HIDDEN
        try:
            self.screen = pygame.display.set_mode((W, H), flags)
        except pygame.error:
            os.environ["SDL_VIDEODRIVER"] = "dummy"
            pygame.display.quit()
            pygame.display.init()
            self.screen = pygame.display.set_mode((W, H), pygame.HIDDEN)
        self.big = pygame.font.SysFont("dejavusans", 58, bold=True)
        self.mid = pygame.font.SysFont("dejavusans", 46, bold=True)
        self.small = pygame.font.SysFont("dejavusans", 34, bold=True)
        self.reset()

    def reset(self):
        self.score = 0
        self.t = 0
        self.px, self.py, self.pw = W / 2, 1560, 300
        self.parts = []
        self.motes = [[random.randrange(W), random.randrange(H), random.uniform(0.5, 1.8)] for _ in range(48)]
        self.orbs = []
        for i in range(4):
            self.spawn(i)

    def spawn(self, i=0):
        self.orbs.append({
            "x": 200 + (i % 4) * 190 + random.randint(-30, 30),
            "y": 480 + random.randint(0, 220),
            "vx": random.uniform(-5, 5),
            "vy": random.uniform(1, 6),
            "r": random.choice([30, 36, 44]),
            "c": PAL[len(self.orbs) % len(PAL)],
            "spin": random.uniform(-0.18, 0.18),
            "a": random.random() * 6.28,
        })

    def burst(self, x, y, c, n=12):
        for _ in range(n):
            ang = random.random() * math.tau
            sp = random.uniform(2.2, 9)
            self.parts.append([x, y, math.cos(ang) * sp, math.sin(ang) * sp - 2, c, 18])

    def step(self, aim):
        self.t += 1
        self.px += max(-32, min(32, aim - self.px))
        self.px = max(160, min(W - 160, self.px))
        for o in self.orbs:
            o["vy"] += 0.62
            o["vx"] *= 0.996
            o["x"] += o["vx"]
            o["y"] += o["vy"]
            o["a"] += o["spin"]
            if o["x"] < o["r"] + 36:
                o["x"], o["vx"] = o["r"] + 36, abs(o["vx"]) * 0.92
            if o["x"] > W - o["r"] - 36:
                o["x"], o["vx"] = W - o["r"] - 36, -abs(o["vx"]) * 0.92
            if o["y"] < 280:
                o["y"], o["vy"] = 280, abs(o["vy"]) * 0.55
            if o["vy"] > 0 and abs(o["x"] - self.px) < self.pw / 2 + 8 and self.py - 20 < o["y"] + o["r"] < self.py + 40:
                hit = (o["x"] - self.px) / (self.pw / 2)
                o["vy"] = -random.uniform(17, 23)
                o["vx"] += hit * 9
                o["spin"] = hit * 0.3
                o["y"] = self.py - o["r"] - 8
                self.score += 20 + int(o["r"])
                self.burst(o["x"], o["y"], o["c"])
            if o["y"] > H + 30:
                o.update(x=random.randint(220, W - 220), y=340, vx=random.uniform(-4, 4), vy=3)
                self.score = max(0, self.score - 20)
        if self.t % 80 == 0 and len(self.orbs) < 6:
            self.spawn()
        live = []
        for p in self.parts:
            p[0] += p[2]
            p[1] += p[3]
            p[3] += 0.18
            p[5] -= 1
            if p[5] > 0:
                live.append(p)
        self.parts = live[-200:]
        for m in self.motes:
            m[1] -= m[2]
            if m[1] < 0:
                m[1], m[0] = H, random.randrange(W)

    def aim_auto(self):
        falling = [o for o in self.orbs if o["vy"] > -1]
        target = min(falling or self.orbs, key=lambda o: self.py - o["y"])
        return target["x"] + target["vx"] * 4

    def draw(self):
        s = self.screen
        s.fill(INK)
        for i in range(9):
            y = 160 + i * 170 + int(math.sin(self.t * 0.05 + i) * 28)
            pygame.draw.ellipse(s, (12 + i * 3, 22 + i * 5, 40 + i * 2), (-120, y, W + 240, 150))
        for m in self.motes:
            pygame.draw.circle(s, (50, 90, 110), (int(m[0]), int(m[1])), 2)
        pygame.draw.rect(s, (22, 40, 62), (24, 230, W - 48, 1460), 5, border_radius=32)
        for o in self.orbs:
            x, y, r = int(o["x"]), int(o["y"]), int(o["r"])
            pygame.draw.circle(s, tuple(c // 3 for c in o["c"]), (x, y), r + 16)
            pygame.draw.circle(s, o["c"], (x, y), r)
            pygame.draw.circle(s, WHITE, (x - r // 3, y - r // 3), max(4, r // 5))
            pygame.draw.line(s, WHITE, (x, y), (x + int(math.cos(o["a"]) * r), y + int(math.sin(o["a"]) * r)), 3)
        for p in self.parts:
            pygame.draw.circle(s, p[4], (int(p[0]), int(p[1])), max(2, p[5] // 4))
        px, py = int(self.px), int(self.py)
        pygame.draw.rect(s, (255, 122, 48), (px - self.pw // 2, py, self.pw, 28), border_radius=14)
        pygame.draw.rect(s, GOLD, (px - self.pw // 2 + 10, py + 5, self.pw - 20, 8), border_radius=6)
        title = self.big.render(TITLE, True, WHITE)
        s.blit(title, (W // 2 - title.get_width() // 2, 52))
        sc = self.mid.render(f"SCORE  {self.score}", True, GOLD)
        s.blit(sc, (W // 2 - sc.get_width() // 2, 132))
        hand = self.small.render(HANDLE, True, TEAL)
        s.blit(hand, (W // 2 - hand.get_width() // 2, 1764))
        sub = self.small.render("KEEP THE ORBS ALOFT", True, (180, 206, 230))
        s.blit(sub, (W // 2 - sub.get_width() // 2, 1824))
        pygame.display.flip()

    def record(self):
        os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
        cmd = [
            "ffmpeg", "-y", "-f", "rawvideo", "-vcodec", "rawvideo",
            "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
            "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20",
            "-movflags", "+faststart", OUT,
        ]
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            for _ in range(FPS * SECS):
                self.step(self.aim_auto())
                self.draw()
                proc.stdin.write(pygame.image.tobytes(self.screen, "RGB"))
        finally:
            proc.stdin.close()
        err = proc.stderr.read().decode("utf-8", "ignore")
        rc = proc.wait()
        if rc != 0:
            raise SystemExit(f"ffmpeg failed ({rc}):\n{err[-1500:]}")
        print("wrote", OUT)

    def play_interactive(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            aim = self.px
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                elif e.type == pygame.KEYDOWN and e.key == pygame.K_r:
                    self.reset()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                aim = self.px - 48
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                aim = self.px + 48
            if pygame.mouse.get_pressed()[0]:
                aim = pygame.mouse.get_pos()[0]
            self.step(aim)
            self.draw()
            clock.tick(FPS)
        pygame.quit()


def main():
    g = Game()
    if PLAY:
        g.play_interactive()
    else:
        g.record()
        pygame.quit()


if __name__ == "__main__":
    main()
