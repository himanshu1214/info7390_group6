# AWS web application
http://ec2-54-145-233-135.compute-1.amazonaws.com

click Welcome to navigate through the website

# Docker full pipeline

1. Dockerfile
  ```
  docker build -t <imageName> .
  ```
2. script.sh

  &nbsp;&nbsp; full pipeline of whole project
  
3. Run

```
  docker run -ti -p 8888:8888 -p 80:80 xinglong/wayfair
```

4. Dockerhub link  

https://hub.docker.com/r/xinglong/wayfair
