package minio

import (
	"bytes"
	"fmt"
	"log"

	"github.com/minio/minio-go"
)

var minioClient *minio.Client

func Init() error {
	var err error
	minioClient, err = minio.New("localhost:9000", "ozontech", "minio123", false)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println("Connecction established")
	return err
}

func CreateBucket(name string) {
	exists, err := minioClient.BucketExists(name)
	if err != nil || exists {
		fmt.Println(err)
		fmt.Println("Smth went wrong")
		fmt.Println(name)

		return
	}
	errorus := minioClient.MakeBucket(name, "")
	if errorus != nil {
		fmt.Print(errorus)
	}
	fmt.Println("Bucket create")

}

func DownloadFile(buffer []byte, name string, workspace string) bool {
	reader := bytes.NewReader(buffer)

	rSize := reader.Size()

	uploadInfo, err := minioClient.PutObject(workspace, name, reader, rSize, minio.PutObjectOptions{})
	if err != nil {
		fmt.Println(err)
	}
	fmt.Println(uploadInfo)
	return true
}
func UploadFile(workspace string, path string) []byte {
	file, err := minioClient.GetObject(workspace, path, minio.GetObjectOptions{})
	if err != nil {
		fmt.Println(err)
		return nil
	}
	defer file.Close()

	fileStat, statErr := file.Stat()
	if statErr != nil {
		return nil
	}
	buffer := make([]byte, fileStat.Size)
	file.Read(buffer)

	return buffer
}
func DeleteFile(path string, workspace string) {
	err := minioClient.RemoveObject(workspace, path)
	if err != nil {
		fmt.Println(err)
	}

	return
}
