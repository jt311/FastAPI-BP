import pytest
from app.schemas import PostOutput, PostResponse
from fastapi import status

#@pytest.mark.skip()
def test_get_posts(authorise_client, generate_posts):
    response = authorise_client.get("/posts")
    validatePostSchema = lambda x: PostOutput(**x)
    postMap = list(map(validatePostSchema, response.json()))

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == len(generate_posts)
    for i, post in enumerate(postMap):
        assert post.Post.id == generate_posts[i].id
        assert post.Post.title == generate_posts[i].title
        assert post.Post.content == generate_posts[i].content
        assert post.Post.user_id == generate_posts[i].user_id
        assert post.Post.published == generate_posts[i].published

#@pytest.mark.skip()
def test_unauthorised_user_get_all_posts(client, generate_posts):
    response = client.get("/posts")
    print(f"Generated {len(generate_posts)} posts")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

#@pytest.mark.skip()
def test_unauthorised_user_get_post_by_id(client, generate_posts):
    response = client.get(f"/posts/{generate_posts[0].id}")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

#@pytest.mark.skip()
@pytest.mark.parametrize('id', [888, 389, 422])
def test_get_post_by_id_not_exist(authorise_client, id, generate_posts):
    response = authorise_client.get(f"posts/{id}")
    print(f"Generated {len(generate_posts)} posts")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json().get('detail') == f"Post with id {id} does not exist"

#@pytest.mark.skip()
@pytest.mark.parametrize('idx', [0,1,2])
def test_get_post_by_id(authorise_client, generate_posts, idx):
    response = authorise_client.get(f"/posts/{generate_posts[idx].id}")
    post = PostOutput(**response.json())
    assert response.status_code == status.HTTP_200_OK
    assert post.Post.id == generate_posts[idx].id
    assert post.Post.title == generate_posts[idx].title
    assert post.Post.content == generate_posts[idx].content
    assert post.Post.user_id == generate_posts[idx].user_id


#@pytest.mark.skip()
@pytest.mark.parametrize('title, content, published', [
    ("Title1", "newContent", True),
    ("Title2", "newContent2", False),
])
def test_create_post(authorise_client, test_user, title, content, published):
    response = authorise_client.post("/posts",
        json = {"title": title,
                "content": content,
                "published": published})
    
    created_post = PostResponse(**response.json())
    assert response.status_code == status.HTTP_201_CREATED
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.user_id == test_user['id']


#@pytest.mark.skip()
def test_unauthorised_user_delete_post(client, generate_posts):
    response = client.delete(f"/posts/{generate_posts[0].id}")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


#pytest.mark.skip()
@pytest.mark.parametrize('id', [888, 389, 422])
def test_delete_post_not_exist(authorise_client, generate_posts, id):
    response = authorise_client.delete(f"/posts/{id}")
    print(f"Generated {len(generate_posts)} posts")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == f"Post with id {id} does not exist"


#pytest.mark.skip()
def test_delete_post_not_permitted(authorise_client, generate_posts):
    response = authorise_client.delete(f"/posts/{generate_posts[3].id}")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()['detail'] == "Not authorised to delete post"

#pytest.mark.skip()
@pytest.mark.parametrize('idx', [0,1,2])
def test_delete_post(authorise_client, generate_posts, idx):
    response = authorise_client.delete(f"/posts/{generate_posts[idx].id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT


#pytest.mark.skip()
@pytest.mark.parametrize('title, content, published, idx', [
    ('updatedTitle1', 'updatedContent1', True, 0),
    ('updatedTitle2', 'updatedContent2', False, 1),
    ('updatedTitle3', 'updatedContent3', True, 2),
])
def test_update_post(authorise_client, generate_posts, title, content, published, idx):
    response = authorise_client.put(f"/posts/{generate_posts[idx].id}",
            json = {"title": title,
                    "content": content,
                    "published": published})
    
    updated_post = PostResponse(**response.json())
    assert response.status_code == status.HTTP_200_OK
    assert updated_post.title == title
    assert updated_post.content == content
    assert updated_post.published == published


#pytest.mark.skip()
def test_unauthorised_update_post(client, generate_posts):
    response = client.put(f"/posts/{generate_posts[0].id}",
        json = {"title": "updatedTitle",
                "content": "updatedContent",
                "published": True})
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


#pytest.mark.skip()
def test_update_post_not_permitted(authorise_client, generate_posts):
    response = authorise_client.put(f"/posts/{generate_posts[3].id}",
                json = {"title": "updatedTitle",
                        "content": "updatedContent",
                        "published": True})
    
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()['detail'] == "Not authorised to update post"


#pytest.mark.skip()
@pytest.mark.parametrize('id', [888, 389, 422])
def test_update_post_not_exist(authorise_client, generate_posts, id):
    response = authorise_client.put(f"/posts/{id}",
                 json = {"title": "updatedTitle",
                         "content": "updatedContent",
                         "published": True})
    
    print(f"Generated {len(generate_posts)} posts")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == f"Post with id: {id} does not exist"