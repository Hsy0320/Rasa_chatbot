### 目前
0.安装docker √

1.生成项目镜像 

## 安装`docker`
略

## 1.build镜像

命令行进到项目目录, 执行`build`命令
```
docker build -t hengsiyu/rasa-demo .
```

## 2.运行`rasa`容器

```
docker run -itd -p 5005:5005 hengsiyu/rasa-demo:latest
```

## 3.修改`js文件`

根据上方定义的端口对应修改，比如上方是5005，则对应改成5005
```js
window.WebChat.default({
      customData: {language: "en"},
      socketUrl: "http://localhost:5005",
      // add other props here
   },
   null
);
```
