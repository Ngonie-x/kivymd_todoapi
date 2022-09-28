import sqlite3


class Database:
    def __init__(self):
        self.con = sqlite3.connect('todo.db')
        self.cursor = self.con.cursor()
        self.create_task_table()

    def create_task_table(self):
        """Create tasks table"""
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS tasks(id integer PRIMARY KEY AUTOINCREMENT, task varchar(50) NOT NULL, due_date varchar(50), completed BOOLEAN NOT NULL CHECK (completed IN (0, 1)))")
        self.con.commit()

    def create_task(self, task, due_date=None):
        """Create a task"""
        self.cursor.execute(
            "INSERT INTO tasks(task, due_date, completed) VALUES(?, ?, ?)", (task, due_date, 0))
        self.con.commit()

        # GETTING THE LAST ENTERED ITEM SO WE CAN ADD IT TO THE TASK LIST
        created_task = self.cursor.execute(
            "SELECT * FROM tasks ORDER BY id DESC LIMIT 1").fetchone()
        return created_task

    def get_task(self, task_id):
        """Gets task with the specified ID
        """
        task = self.cursor.execute(
            "SELECT * FROM tasks WHERE id=?", (task_id,)
        )

        return task.fetchone()

    def get_tasks(self):
        """Get tasks"""
        tasks = self.cursor.execute(
            "SELECT * FROM tasks").fetchall()
        return tasks

    def mark_task_as_complete(self, taskid):
        """Marking tasks as complete"""
        self.cursor.execute(
            "UPDATE tasks SET completed=1 WHERE id=?", (taskid,))
        self.con.commit()

    def mark_task_as_incomplete(self, taskid):
        """Mark task as uncomplete"""
        self.cursor.execute(
            "UPDATE tasks SET completed=0 WHERE id=?", (taskid,))
        self.con.commit()

        # return the text of the task
        task_text = self.cursor.execute(
            "SELECT task FROM tasks WHERE id=?", (taskid,)).fetchall()
        return task_text[0][0]

    def update_task(self, taskid, task):
        """Update the task text

        Args:
            taskid (int): id of the task to be updated
            task (str): The new text for the update
        """

        self.cursor.execute(
            "UPDATE tasks SET task=? WHERE id=?", (task, taskid)
        )
        self.con.commit()

    def delete_task(self, taskid):
        """Delete a task"""
        self.cursor.execute("DELETE FROM tasks WHERE id=?", (taskid,))
        self.con.commit()

    def close_db_connection(self):
        self.con.close()
