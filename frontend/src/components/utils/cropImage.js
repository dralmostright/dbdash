import { createImage } from "./createImage";

/**
 * Crops an image using percentages from react-easy-crop
 * Works reliably with objectFit="contain"
 */
export async function getCroppedImg(imageSrc, croppedAreaPercentages, outputSize = 300) {
  const image = await createImage(imageSrc);

  const canvas = document.createElement("canvas");
  canvas.width = outputSize;
  canvas.height = outputSize;

  const ctx = canvas.getContext("2d");

  const { naturalWidth, naturalHeight } = image;

  // Convert percentages to actual pixels
  const cropX = (croppedAreaPercentages.x / 100) * naturalWidth;
  const cropY = (croppedAreaPercentages.y / 100) * naturalHeight;
  const cropWidth = (croppedAreaPercentages.width / 100) * naturalWidth;
  const cropHeight = (croppedAreaPercentages.height / 100) * naturalHeight;

  ctx.drawImage(
    image,
    cropX,
    cropY,
    cropWidth,
    cropHeight,
    0,
    0,
    outputSize,
    outputSize
  );

  return new Promise((resolve) => {
    canvas.toBlob((blob) => resolve(blob), "image/jpeg", 0.95);
  });
}
