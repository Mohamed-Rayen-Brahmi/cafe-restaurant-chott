import sharp from "sharp";
import { mkdirSync } from "node:fs";

mkdirSync("public/images", { recursive: true });

const jobs = [
  // [source, outBase, {width, height?, fit}]
  { src: "src-images/hero-port.jpg", out: "hero", widths: [2400, 1600, 1000], crop: { width: 2400, height: 1100 } },
  { src: "src-images/port-day.jpg", out: "about-port", widths: [1400, 900, 600] },
  { src: "src-images/terrace.jpg", out: "terrace", widths: [800, 500] },
  { src: "src-images/port-vertical.jpg", out: "menu-side", widths: [1000, 700], crop: { width: 1000, height: 1300 } },
  { src: "src-images/port-panorama.jpg", out: "cta-band", widths: [2200, 1400, 900], crop: { width: 2200, height: 900 } },
];

for (const job of jobs) {
  for (const w of job.widths) {
    let pipeline = sharp(job.src).rotate();
    if (job.crop) {
      const h = Math.round((job.crop.height / job.crop.width) * w);
      pipeline = pipeline.resize(w, h, { fit: "cover", position: "attention" });
    } else {
      pipeline = pipeline.resize({ width: w });
    }
    await pipeline.clone().webp({ quality: 78 }).toFile(`public/images/${job.out}-${w}.webp`);
    await pipeline.clone().jpeg({ quality: 80, mozjpeg: true }).toFile(`public/images/${job.out}-${w}.jpg`);
  }
  console.log("done:", job.out);
}
