### Note
修改 `list4.py`、```list5.py` 之后，需重新运行 `list6.py`、`list8.py`。因为后者依赖前者
---
**Note** that the validation condition implemented by an **ASK** query is "in the inverse direction" from its SELECT counterpart: **ASK** queries return `true` for value nodes that **conform** to the constraint, while **SELECT** queries **return those value nodes that do not conform**.