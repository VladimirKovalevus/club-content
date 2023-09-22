package database

import (
	"database/sql"
	"fmt"
	fileprocessor "hahaton/file_processor"
	"hahaton/minio"
	minio_service "hahaton/minio-service"
	"hahaton/types"
	"log"
	"strings"

	_ "github.com/lib/pq"
)

var myPostgres *sql.DB

func Init() error {
	connStr := "host=localhost port=5432 user=admin password=root dbname=postgres sslmode=disable"

	var err error
	myPostgres, err = sql.Open("postgres", connStr)
	if err != nil {
		log.Fatal(err)
	}
	_, err = myPostgres.Exec(`create table if not exists workspaces(
		id uuid not null default gen_random_uuid(),
		name character varying not null unique
	);`)
	if err != nil {
		log.Fatal(err)
	}
	_, err = myPostgres.Exec(`create table if not exists users(
		id uuid not null default gen_random_uuid(),
		login character varying not null,
		password character varying not null,
		workspace_id uuid not null,
		role character varying
	);`)
	if err != nil {
		log.Fatal(err)
	}
	_, err = myPostgres.Exec(`create table if not exists files(
		id uuid not null default gen_random_uuid(),
		path character varying not null unique,
		parent_id uuid,
		workspace_id uuid not null
	);`)
	if err != nil {
		log.Fatal(err)
	}
	_, err = myPostgres.Exec(`create table if not exists folders(
		id uuid not null default gen_random_uuid(),
		path character varying not null,
		parent_id uuid,
		workspace_id uuid not null
	);`)
	if err != nil {
		log.Fatal(err)
	}
	return err
}

func CreateDBUser(user minio_service.User) minio_service.User {
	_, err := myPostgres.Exec("insert into users values(default,$1,$2,$3,$4);", user.Login, user.Password, user.WorkspaceId, user.Role)
	if err != nil {
		fmt.Println(err)
		return user
	}
	return user
}

func UpdateUser(user minio_service.User) minio_service.User {
	_, err := myPostgres.Exec("insert into users values(default,$1,$2,$3,$4);", user.Login, user.Password, user.WorkspaceId, user.Role)
	if err != nil {
		fmt.Println(err)
		return user
	}
	return user
}

func ReadUser(user minio_service.User) minio_service.User {
	Scan := myPostgres.QueryRow("select * from users where login = $1 and password = $2 and workspace_id;", user.Login, user.Password, user.WorkspaceId)
	var us minio_service.User

	switch err := Scan.Scan(&us); err {
	case sql.ErrNoRows:
		fmt.Println("No rows were returned!")
	case nil:
		fmt.Println(us)
	}
	return us
}

func CreateBucket(workspace minio_service.Workspace) string {
	Scan := myPostgres.QueryRow("select id from workspaces where name = $1", workspace.Name)
	var id string

	switch err := Scan.Scan(&id); err {
	case sql.ErrNoRows:
		fmt.Println("No rows were returned!")
	case nil:
		fmt.Println(id)
	}
	if id != "" {
		return id
	}

	_, err := myPostgres.Exec("insert into workspaces values(default,$1);", workspace.Name)
	if err != nil {
		fmt.Println(err)
		return ""
	}
	minio.CreateBucket(workspace.Name)
	scan := myPostgres.QueryRow("select id from workspaces where name = $1", workspace.Name)

	switch err := scan.Scan(&id); err {
	case sql.ErrNoRows:
		fmt.Println("No rows were returned!")
	case nil:
		fmt.Println(id)
	}
	if id != "" {
		return id
	}

	return id
}

func CreateFolder(folder minio_service.Folder) minio_service.Status {
	_, err := myPostgres.Exec("insert into folders values(default,$1,$2);", folder.Path, folder.WorkspaceId)
	var status minio_service.Status
	status.Status = true
	if err != nil {
		status.Status = false
	}
	return status
}
func GetFolder(folder minio_service.Folder) minio_service.Status {
	_, err := myPostgres.Exec("select * from folders where path like('$1') and path not like('$2/%');", folder.Path, folder.WorkspaceId)
	var status minio_service.Status
	status.Status = true
	if err != nil {
		status.Status = false
	}
	return status
}
func DeleteFolder(folder minio_service.Folder) minio_service.Status {
	_, err := myPostgres.Exec("delete from folders where path = '$1' and workspace_id = '$2';", folder.Path, folder.WorkspaceId)
	var status minio_service.Status
	status.Status = true
	if err != nil {
		status.Status = false
	}
	return status
}

func GetWorkspaceName(WorkspaceId string) string {

	var name string
	scan := myPostgres.QueryRow("select name from workspaces where id = $1", WorkspaceId)
	switch err := scan.Scan(&name); err {
	case sql.ErrNoRows:
		fmt.Println("No rows were returned!")
	case nil:
		fmt.Println(name)
	}
	return name
}

func CreateFile(file minio_service.File) string {
	path := strings.Split(file.Path, "/")
	var status minio_service.Status

	var newPath string
	for i := 0; i < len(path)-2; i++ {
		newPath = "/" + path[i]
	}
	res, err := myPostgres.Query("select * from folders where path = '$1' and workspace_id= '$2';", newPath, file.WorkspaceId)
	if err != nil {
		status.Status = false
		return ""
	}
	defer res.Close()

	var fold types.UploadFileModel
	scanErr := res.Scan(&fold)
	if scanErr != nil {
		status.Status = false
		return ""
	}
	_, inErr := myPostgres.Exec("insert into files values(default,$1,$2,$3);", file.Path, fold.Id, file.WorkspaceId)
	status.Status = true
	if inErr != nil {
		status.Status = false
	}
	fmt.Println(fold)
	fil, ferr := myPostgres.Query("select * from folders where path = '$1' and workspace_id= '$2';", newPath, file.WorkspaceId)
	if ferr != nil {
		fmt.Println(ferr)
		return ""
	}
	var id string
	fil.Scan(&id)
	return id
}
func GetFile(path string, workspace string) string {
	scan := myPostgres.QueryRow("select * from files where path = $1 and workspace_id = $2;", path, workspace)
	var file minio_service.File
	switch err := scan.Scan(&file); err {
	case sql.ErrNoRows:
		fmt.Println("No rows were returned!")
	case nil:
		fmt.Println(file)
	}
	return file.Path
}

func DeleteFile() bool {

	return true

}

func PullFolder(path string, workspace string) minio_service.Files {

	files := minio_service.Files{}
	scan := myPostgres.QueryRow(`select path from files where path like $1% and path not like $1/%/ and workspace_id = $2;`, path, workspace)
	var file minio_service.File
	switch err := scan.Scan(&files.Files); err {
	case sql.ErrNoRows:
		fmt.Println("No rows were returned!")
	case nil:
		fmt.Println(file)
	}

	for _, el := range files.Files {

		if strings.LastIndex(el.Path, "png") == len(el.Path)-3 || strings.LastIndex(el.Path, "jpg") == len(el.Path)-3 {
			buffer := minio.UploadFile(workspace, el.Path)
			compressed, _ := fileprocessor.CompressImage(buffer, 10)
			el.Buffer = compressed
		}

	}

	return files
}
