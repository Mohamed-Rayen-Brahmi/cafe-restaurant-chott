import sharp from "sharp";
import { mkdirSync } from "node:fs";

mkdirSync("public/images/pour", { recursive: true });

const frames = ["frame-1-empty", "frame-2-third", "frame-3-twothirds", "frame-4-full"];

for (const frame of frames) {
  const src = `src-images/pour-sequence/${frame}.png`;
  // Source is 200x200; upscale modestly with a light sharpen since it's a small decorative element, not a hero-scale image.
  await sharp(src)
    .resize(480, 480, { kernel: "lanczos3" })
    .sharpen({ sigma: 0.6 })
    .webp({ quality: 90 })
    .toFile(`public/images/pour/${frame}-480.webp`);
  await sharp(src)
    .resize(480, 480, { kernel: "lanczos3" })
    .sharpen({ sigma: 0.6 })
    .png({ quality: 90 })
    .toFile(`public/images/pour/${frame}-480.png`);
  console.log("done:", frame);
}
