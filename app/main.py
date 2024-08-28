import time

import psycopg
from fastapi import FastAPI, HTTPException, Response, status
from psycopg.rows import dict_row
from pydantic import BaseModel


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


app = FastAPI()

while True:
    try:
        conn = psycopg.connect(
            host="localhost", dbname="fastapi", user="jj", password="josh2000"
        )

        cursor = conn.cursor(row_factory=dict_row)
        print("connected succesfully")
        break
    except Exception as error:
        print("connecting failed")
        print(error)
        time.sleep(2)


def raise_404(id: int):
    raise HTTPException(
        status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found"
    )


@app.get("/")
async def root():
    return {"message": "Hello World!"}


@app.get("/posts")
async def get_posts():
    cursor.execute("""SELECT * FROM post""")
    posts = cursor.fetchall()
    print(posts)
    return {"posts": posts}


@app.get("/posts/{id}")
async def get_post(id: int):
    cursor.execute("""SELECT * FROM post WHERE id = %s""", (str(id),))
    post = cursor.fetchone()
    if not post:
        raise_404(id)
    return post


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post):
    cursor.execute(
        """INSERT INTO post (title, content, published)
           VALUES (%s, %s, %s ) RETURNING *""",
        (post.title, post.content, post.published),
    )
    conn.commit()
    new_post = cursor.fetchone()

    return new_post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    cursor.execute("""DELETE FROM post WHERE id = %s RETURNING *""", (str(id),))
    post = cursor.fetchone()
    if not post:
        raise_404(id)
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(
        """UPDATE post SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
        (post.title, post.content, post.published, id),
    )
    returned_post = cursor.fetchone()
    if not returned_post:
        raise_404(id)
    conn.commit()
    return returned_post
