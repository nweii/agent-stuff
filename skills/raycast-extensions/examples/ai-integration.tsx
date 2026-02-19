// ABOUTME: Example of Raycast AI integration with AI.ask and streaming.
// ABOUTME: Shows basic usage, error handling, access checks, and streaming responses.

import { AI, Clipboard, showToast, Toast, showHUD, environment } from "@raycast/api";

// Basic AI.ask usage - great for no-view commands
export default async function Command() {
  // Check if user has AI access (Raycast Pro required)
  if (!environment.canAccess(AI)) {
    await showToast({
      style: Toast.Style.Failure,
      title: "AI Unavailable",
      message: "Raycast Pro subscription required for AI features",
    });
    return;
  }

  // Show loading toast
  const toast = await showToast({
    style: Toast.Style.Animated,
    title: "Generating...",
  });

  try {
    // Basic usage with default model
    const answer = await AI.ask("Suggest 5 creative project ideas for a weekend");

    // Copy result to clipboard
    await Clipboard.copy(answer);

    // Update toast to success
    toast.style = Toast.Style.Success;
    toast.title = "Copied to Clipboard";
    toast.message = "AI response copied";
  } catch (error) {
    toast.style = Toast.Style.Failure;
    toast.title = "AI Error";
    toast.message = error instanceof Error ? error.message : "Unknown error";
  }
}

// Example: Using specific model and creativity
export async function askWithOptions() {
  const answer = await AI.ask("Write a haiku about programming", {
    model: AI.Model.Anthropic_Claude_Sonnet,
    creativity: "high", // or "none", "low", "medium", "maximum"
  });

  return answer;
}

// Example: Streaming response for real-time feedback
export async function streamingExample() {
  await showHUD("Generating...");

  let fullResponse = "";

  const stream = AI.ask("Explain quantum computing in simple terms");

  // Listen to streaming data events
  stream.on("data", (chunk) => {
    fullResponse += chunk;
    // You could update a file or state here as data streams in
    console.log("Received chunk:", chunk);
  });

  // Wait for completion
  await stream;

  await Clipboard.copy(fullResponse);
  await showHUD("Done! Response copied to clipboard");
}

// Example: Using AbortController to cancel requests
export async function cancellableRequest() {
  const controller = new AbortController();

  // Cancel after 5 seconds
  const timeout = setTimeout(() => controller.abort(), 5000);

  try {
    const answer = await AI.ask("Tell me a long story", {
      signal: controller.signal,
    });
    clearTimeout(timeout);
    return answer;
  } catch (error) {
    if (error instanceof Error && error.name === "AbortError") {
      await showToast({
        style: Toast.Style.Failure,
        title: "Request Cancelled",
        message: "AI request was aborted",
      });
    }
    throw error;
  }
}
