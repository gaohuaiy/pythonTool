# 打包

```
pyinstaller -F Oracle_Process_Clob_JSON.py
```

# 修改生成的 Oracle_Process_Clob_JSON.spec

```
-- 修改此节点
hiddenimports=['getpass','secrets','asyncio','oracledb','json','uuid']
```

## 再次运行

```
pyinstaller Oracle_Process_Clob_JSON.spec
```

