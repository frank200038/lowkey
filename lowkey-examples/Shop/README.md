# Shop Example

## Structure

![Image](./img/shop_metamodel.png)

- [/editor](./editor) - Simple command-line editor containing necessary commands to create and manipulate the Shop model.
- [/metamodel](./metamodel) - Metamodel of Shop
- [/facilites](./facilities) - Contains the helper function to print out a Shop model in a readable form.

## Execute

1. Open a terminal and start the server in [/lowkey/network](./lowkey/network): ```python Server.py -log debug```.
2. Open a number of editor clients in [/editor](./editor) in separate terminals: ```python Editor.py -log debug```.
3. Refer to the command language below to start modeling.

### Command Language
**For available types and the right name of associations, please refer to the [`ShopPackage.py`](./metamodel/ShopPackage.py)**

**Commands are case-sensitive.**

1. `READ` - Returns the Shop model in a readable form.
2. `OBJECTS` - Lists every object in the local session.
3. `CREATE [type] [name]` - Creates an instance with name `[name]` of the domain-specific type `[type]`.
    - Ex: `CREATE Shop Shop1`, `CREATE Product Product1`
4. `LINK [source].[port] TO [target]` - Links object `[target]` to object `[source]` via port `[port]`.
    - Ex: `LINK Shop1.members TO Member1`, `LINK Shop1.employees TO Employee1`
5. `UPDATE [name] [attribute] [newValue]` - Updates attribute `[attribute]` in object with `[name]` to value `[newValue]`.
    - Ex: `UPDATE Shop1 shopName Shop2`, `UPDATE Film1 price 20`
6. ~~`DELETE [name]` - Deletes object `[name]`~~ (Not currently supported, but will be in the future)
