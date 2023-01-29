import pytest
from fastapi import status

#@pytest.mark.skip()
@pytest.mark.parametrize('vote_direction', [0,1])
def test_vote_post_not_exist(authorise_client, generate_posts, vote_direction):
    data = {"post_id": 8000,
            "vote_direction": vote_direction}
    
    print(f"Generated {len(generate_posts)} posts")
    response = authorise_client.post("/vote", json = data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == f"Post with id: {data['post_id']} does not exist"

#@pytest.mark.skip()
@pytest.mark.parametrize('vote_direction', [0,1])
def test_unauthorised_vote_post(client, generate_posts, vote_direction):
    data = {"post_id": generate_posts[0].id,
            "vote_direction": vote_direction}
    
    response = client.post("/vote", json = data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

#@pytest.mark.skip()
def test_upvote_post(authorise_client, generate_posts):
    data = {"post_id": generate_posts[2].id,
            "vote_direction": 1}
    
    response = authorise_client.post("/vote", json = data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['message'] == "Successfully added vote"


#@pytest.mark.skip()
@pytest.mark.parametrize('postIdx', [0,1])
def test_upvote_exists(authorise_client, generate_posts, generate_votes, postIdx):
    data = {"post_id": generate_posts[postIdx].id,
            "vote_direction": 1}
    
    response = authorise_client.post("/vote", json = data)
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()['detail'] == f"User: {generate_votes[0].user_id} has already voted for post with ID: {data['post_id']}"


#@pytest.mark.skip()
@pytest.mark.parametrize('postIdx', [0,1])
def test_downvote_post(authorise_client, generate_posts, generate_votes, postIdx):
    data = {"post_id": generate_posts[postIdx].id,
            "vote_direction": 0}
    
    print(f"Generated {len(generate_votes)} votes")
    response = authorise_client.post("/vote", json = data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['message'] == "Successfully deleted vote"


#@pytest.mark.skip()
def test_downvote_post_not_exist(authorise_client, generate_posts, generate_votes):
    data = {"post_id": generate_posts[2].id,
            "vote_direction": 0}
    
    print(f"Generated {len(generate_votes)} votes")
    response = authorise_client.post("/vote", json = data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == f"Vote for Post with ID: {data['post_id']} does not exist. Cannot downvote"


## Can condense into single function for upvote and downvote tests with parametrize