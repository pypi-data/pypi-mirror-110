docker build -t _project .
docker run -dp 8080:8080 _project
#debug - docker run -it -p 8080:8080 scoops_project
