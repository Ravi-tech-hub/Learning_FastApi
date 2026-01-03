from fastapi import FastAPI
from routers import user,auth,category,comment,post

app=FastAPI(title="Blog API")
app.include_router(auth.router,prefix="/auth",tags=["Authentication"])
app.include_router(category.router,prefix="/categories",tags=["Categories"])
app.include_router(comment.router,prefix="/comments",tags=["Comments"])
app.include_router(post.router,prefix="/posts",tags=["Posts"])




