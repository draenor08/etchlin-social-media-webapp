import styled from "styled-components";

const PostContainer = styled.div`
  border: 1px solid #ddd;
  padding: 10px;
  margin: 10px;
`;

function Post({ post }) {
  return (
    <PostContainer>
      <h2>{post.caption}</h2>
      <img src={post.image_url} alt="Post" />
    </PostContainer>
  );
}

export default Post;
