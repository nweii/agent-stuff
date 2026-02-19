// ABOUTME: Example of data fetching in Raycast using useFetch hook.
// ABOUTME: Shows loading states, error handling, pagination, and revalidation.

import { ActionPanel, Action, List, showToast, Toast, Icon } from "@raycast/api";
import { useFetch } from "@raycast/utils";
import { useState } from "react";

interface Post {
  userId: number;
  id: number;
  title: string;
  body: string;
}

export default function Command() {
  const [searchText, setSearchText] = useState("");

  const { data, error, isLoading, revalidate } = useFetch<Post[]>(
    "https://jsonplaceholder.typicode.com/posts",
    {
      // Keep previous data while loading new data
      keepPreviousData: true,
    }
  );

  // Show error toast if fetch fails
  if (error) {
    showToast({
      style: Toast.Style.Failure,
      title: "Failed to load posts",
      message: error.message,
    });
  }

  // Filter posts based on search text
  const filteredPosts = data?.filter((post) =>
    post.title.toLowerCase().includes(searchText.toLowerCase())
  );

  return (
    <List
      isLoading={isLoading}
      searchText={searchText}
      onSearchTextChange={setSearchText}
      searchBarPlaceholder="Search posts..."
      throttle
    >
      {filteredPosts?.map((post) => (
        <List.Item
          key={post.id}
          title={post.title}
          subtitle={`Post #${post.id}`}
          accessories={[{ text: `User ${post.userId}` }]}
          actions={
            <ActionPanel>
              <Action.Push
                title="View Details"
                icon={Icon.Eye}
                target={<PostDetail post={post} />}
              />
              <Action.CopyToClipboard title="Copy Title" content={post.title} />
              <Action
                title="Refresh"
                icon={Icon.ArrowClockwise}
                shortcut={{ modifiers: ["cmd"], key: "r" }}
                onAction={() => revalidate()}
              />
            </ActionPanel>
          }
        />
      ))}

      {!isLoading && filteredPosts?.length === 0 && (
        <List.EmptyView
          title="No posts found"
          description="Try a different search term"
          icon={Icon.MagnifyingGlass}
        />
      )}
    </List>
  );
}

// Detail view for a single post
function PostDetail({ post }: { post: Post }) {
  // Fetch comments for this post
  const { data: comments, isLoading } = useFetch<{ id: number; name: string; body: string }[]>(
    `https://jsonplaceholder.typicode.com/posts/${post.id}/comments`
  );

  const markdown = `
# ${post.title}

${post.body}

---

## Comments (${comments?.length || 0})

${
  comments
    ?.map(
      (comment) => `
### ${comment.name}

${comment.body}
`
    )
    .join("\n") || "Loading comments..."
}
`;

  return (
    <List.Item.Detail markdown={markdown} isLoading={isLoading} />
  );
}
