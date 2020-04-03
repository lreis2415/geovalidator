
- 导入的本体中（skos、software等），应该避免存在间接导入的本体（已经导入的除外，例如skos），否则 owlready 会自动尝试连接网络下载，从而报错
    若有，则可以注释掉
    如 task.owl 中需要注释
    ```xml
    <!--
        <owl:imports rdf:resource="http://www.egc.org/ont/data"/>
        <owl:imports rdf:resource="http://www.egc.org/ont/domain/geospatial"/>
        <owl:imports rdf:resource="http://www.egc.org/ont/model/geospatial"/>
    -->
    ```
    **但是生成之后需要打开注释/重新导入**
- 在生成本体时， task.owl 会被修改，增加 task 实例及 hasProcessTool 属性
- 若多次生成本体，可能会由于task中存在相应的工具实例，导致具体的本体中不再生成实例。因此，需要使用原来未修改的task（task-backup.owl）替换掉已修改的task（将task-backup.owl重命名为task.owl），然后重新生成
