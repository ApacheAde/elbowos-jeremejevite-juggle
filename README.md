# Jeremejevite Juggle

Full-colour Python 3 neon multi-orb arcade for [ElbowOS](https://x.com/ElbowOS).

Keep teal, sapphire, rose, gold, and violet orbs aloft. The copper paddle adds spin. Dropped orbs cost points. A fresh orb joins the set every few seconds, up to six.

Not a commercial emulator and not a ROM player.

## Play

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 jeremejevite_juggle.py --play
```

A / Left and D / Right move the paddle. Mouse click also aims. R restarts.

## Record a 9:16 reel

```bash
python3 jeremejevite_juggle.py --record
```

Headless autoplay writes a 1080x1920, 15s, 30fps H.264 MP4 (yuv420p, CRF 20, +faststart). Override the path with `ELBOWOS_MP4`.

## Links

- Featured account: https://x.com/ElbowOS
- Drive reel: https://drive.google.com/file/d/1wVQUGUdXaEWuNiixnO_hlan_EQB8yjzA/view
- Source: https://github.com/ApacheAde/elbowos-jeremejevite-juggle
