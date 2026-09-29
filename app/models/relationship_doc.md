**`ForeignKey` is a database thing.** `user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))` creates a column in the `todos` table that holds a number, and it tells the database that the number must match a real row in `users`. That's all it does. On the Python side, `todo.user_id` is just an integer.

**`relationship()` is an ORM thing.** It doesn't create any column or change the database at all. It lets you work with actual objects in Python instead of raw IDs.

Here is the difference in practice.

With only the foreign key:

```python
todo = session.get(Todo, 1)
print(todo.user_id)  # 5  (just a number)

# To get the user, you have to query yourself
user = session.get(User, todo.user_id)
print(user.name)

# To create a todo, you must already know the user's id
new_todo = Todo(title="Buy milk", user_id=user.id)
```

With the relationship added:

```python
todo = session.get(Todo, 1)
print(todo.user.name)  # SQLAlchemy loads the User for you

# You can pass objects, even before they have an id
user = User(name="Alice")
new_todo = Todo(title="Buy milk", user=user)
session.add(new_todo)
session.commit()  # SQLAlchemy inserts the user, gets its id, fills user_id for you
```

So the foreign key is the storage, and the relationship is the convenience layer on top of it. SQLAlchemy uses the foreign key to figure out how the two classes connect, which is why you don't have to repeat the join condition.

**Why write it on both sides?** Each side gives one direction of navigation:

- `Todo.user` lets you go from a todo to its user.
- `User.todo` lets you go from a user to their todo.

`back_populates` links the two so they stay in sync. Without it, they would be treated as two unrelated relationships:

```python
todo.user = user
print(user.todo)  # with back_populates: this todo. Without it: None until you refresh from the DB
```

**Are both sides required?** No. If you only ever go from todo to user, you can define just `Todo.user` and skip the other side (and skip `back_populates`). If you don't need navigation at all, you can even skip `relationship()` entirely and only use the foreign key, and everything will still work at the database level. You'd just have to do the queries and joins yourself.

**What about `cascade="all, delete-orphan"`?** That's an optional extra, and it only goes on the parent side. It tells SQLAlchemy what to do with the child when the parent changes: delete the todo when the user is deleted, or when you set `user.todo = None`. Without it, deleting a user would try to set `todos.user_id` to NULL (which fails if the column is not nullable).

In short: the `ForeignKey` is required for the database relationship, and `relationship()` is optional but almost always worth adding because it lets you work with objects instead of IDs.