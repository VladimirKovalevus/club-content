package fileprocessor

import "github.com/h2non/bimg"

func CompressImage(image []uint8, quality int) ([]byte, error) {

	convert, err := bimg.NewImage(image).Convert(bimg.WEBP)

	if err != nil {
		return image, err
	}
	processed, err := bimg.NewImage(convert).Process(bimg.Options{Quality: quality})

	bimg.Write("abc.webp", processed)

	return processed, err
}
