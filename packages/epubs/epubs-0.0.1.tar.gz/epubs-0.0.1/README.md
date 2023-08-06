# epubs

## 介绍
解析epub的工具

## 安装


    pip install epubs


## 使用

- epub 转 html


    import epubs
    
    epubs.to_html('xxxxx.epub', save_path='./xxxxx')


- epub 转 text
    

    import epubs
    
    text = epubs.to_text('xxxxx.epub')
    print(text)

