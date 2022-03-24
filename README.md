## 简介
Wagner, M.G. J Real-Time Image Proc (2019). https://doi.org/10.1007/s11554-019-00886-7

The paper can be found at https://link.springer.com/article/10.1007/s11554-019-00886-7.

## 编译

进入根目录

```bash
cmake ./ && make
```

完成后在根目录下生成**libMySharedLib.so**文件
将文件复制进./example/python 目录下
运行python main.py即可查看效果

## 输出

example中的输出为json格式，格式为：

```json
{
    features:[
        {
            id:0,
            coordinates:[[x0,y0],[x1,y1],...]
        },
        ...
    ]
}
```

features中的每一个id对应一条线，coordinates中的坐标对应图片中的像素（不是地理坐标）
