FROM golang:latest
WORKDIR /build/golang
COPY . /build/golang
EXPOSE 8785
RUN go mod tidy
CMD go run main.go
