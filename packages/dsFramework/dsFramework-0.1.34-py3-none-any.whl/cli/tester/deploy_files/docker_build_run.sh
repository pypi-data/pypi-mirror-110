docker build -t {name-your-service} .
docker run -dp 8080:8080 {name-your-service}
#debug - docker run -it -p 8080:8080 {name-your-service}
