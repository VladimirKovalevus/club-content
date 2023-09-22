package main

import (
	"context"
	"fmt"
	"hahaton/database"
	"hahaton/minio"
	minio_service "hahaton/minio-service"
	"log"
	"net"
	"os"
	"os/signal"

	"google.golang.org/grpc"
)

type server struct {
	minio_service.TransmissionServer
}

// CreateUser(ctx context.Context, in *User, opts ...grpc.CallOption) (*User, error)
// UpdateUser(ctx context.Context, in *User, opts ...grpc.CallOption) (*User, error)
// ReadUser(ctx context.Context, in *User, opts ...grpc.CallOption) (*User, error)
// CreateWorkspace(ctx context.Context, in *Workspace, opts ...grpc.CallOption) (*Workspace, error)
// CreateFile(ctx context.Context, in *File, opts ...grpc.CallOption) (*File, error)
// GetFile(ctx context.Context, in *Path, opts ...grpc.CallOption) (*User, error)
// DeleteFile(ctx context.Context, in *File, opts ...grpc.CallOption) (*User, error)
// CreateFolder(ctx context.Context, in *Folder, opts ...grpc.CallOption) (*Folder, error)
// GetFolder(ctx context.Context, in *Folder, opts ...grpc.CallOption) (*Folder, error)
// DeleteFolder(ctx context.Context, in *Folder, opts ...grpc.CallOption) (*Folder, error)

func (s *server) CreateUser(ctx context.Context, req *minio_service.User) (*minio_service.User, error) {
	var responce minio_service.User
	responce = database.CreateDBUser(*req)
	return &responce, nil
}

func (s *server) UpdateUser(ctx context.Context, req *minio_service.User) (*minio_service.User, error) {
	var responce minio_service.User
	responce = database.CreateDBUser(*req)
	return &responce, nil
}

func (s *server) ReadUser(ctx context.Context, req *minio_service.User) (*minio_service.User, error) {
	var responce minio_service.User
	responce = database.ReadUser(*req)
	return &responce, nil
}
func (s *server) CreateWorkspace(ctx context.Context, req *minio_service.Workspace) (*minio_service.ID, error) {
	responce := minio_service.ID{}
	responce.Id = database.CreateBucket(*req)

	if responce.Id == "" {
		return &responce, nil
	}
	minio.CreateBucket(req.Name)
	return &responce, nil
}
func (s *server) CreateFile(ctx context.Context, req *minio_service.File) (*minio_service.ID, error) {
	var responce minio_service.ID
	responce.Id = database.CreateFile(*req)
	name := database.GetWorkspaceName(req.WorkspaceId)
	minio.DownloadFile(req.Buffer, req.Path, name)
	return &responce, nil
}
func (s *server) GetFile(ctx context.Context, req *minio_service.WorkspaceFile) (*minio_service.File, error) {
	var responce minio_service.File
	path := database.GetFile(req.Path, req.WorkspaceId)
	responce.Path = path
	responce.Buffer = minio.UploadFile(req.WorkspaceId, path)
	return &responce, nil
}

func (s *server) DeleteFile(ctx context.Context, req *minio_service.File) (*minio_service.Status, error) {
	var responce minio_service.Status
	responce.Status = database.DeleteFile()
	return &responce, nil
}
func (s *server) CreateFolder(ctx context.Context, req *minio_service.Folder) (*minio_service.Status, error) {
	var responce minio_service.Status
	responce = database.CreateFolder(*req)
	return &responce, nil
}
func (s *server) GetFolder(ctx context.Context, req *minio_service.Folder) (*minio_service.Files, error) {
	resp := database.PullFolder(req.Path, req.WorkspaceId)
	return &resp, nil
}
func (s *server) DeleteFolder(ctx context.Context, req *minio_service.Folder) (*minio_service.Status, error) {
	var responce minio_service.Status
	responce = database.DeleteFolder(*req)
	return &responce, nil
}

func main() {
	dbErr := database.Init()
	if dbErr != nil {
		log.Fatal("Cant connect to database")
		return
	}

	s3Err := minio.Init()

	if s3Err != nil {
		log.Fatal("Cant connect to s3 server")
		return
	}

	lis, err := net.Listen("tcp", "localhost:8785")

	if err != nil {
		log.Fatal(err)
	}
	var opts []grpc.ServerOption
	s := grpc.NewServer(opts...)

	minio_service.RegisterTransmissionServer(s, &server{})

	go func() {
		fmt.Println("Starting Server...")
		if err := s.Serve(lis); err != nil {
			log.Fatalf("failed to serve: %v", err)
		}
	}()

	ch := make(chan os.Signal, 1)
	signal.Notify(ch, os.Interrupt)

	<-ch
	fmt.Println("Goodbye")

	s.Stop()

}
