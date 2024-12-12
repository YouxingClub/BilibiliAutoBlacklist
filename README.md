# B站批量拉黑处理程序

## 使用方法
1. 在文件夹内放置**B站直播间机器人_实时更新.xlsx**
2. 打开批量拉黑.exe
3. 文件目录下会生成**loginqr.png**，打开后扫描二维码
4. 登录成功后会自动根据表格进行拉黑操作

## excel表格数据源

[B站直播间机器人_实时更新](https://docs.qq.com/sheet/DUkdEbXlzYnFqTmlt?tab=BB08J2)

## 如何编译本代码

安装[pixi](https://pixi.sh/latest/)软件包管理器

~~~powershell
pixi install

# 直接运行
pixi run run

# 打包为exe
pixi run build
~~~