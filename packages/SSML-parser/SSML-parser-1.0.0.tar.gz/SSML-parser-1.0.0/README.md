## This is a simple SSML-parser and is currently under development.

Example:

File output
```python
parseObject = parseSSML("test.xml") ## input file
parseObject.parse()
with (open("test.txt","w")) as f:
    ## output file
f.write(parseObject.final_string)
```
Text output
```python
parseObject = parseSSML("test.xml") ## input file
parseObject.parse()
print(parseObject.final_string)
