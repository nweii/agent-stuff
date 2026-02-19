# AI API Reference

Raycast provides seamless AI access without API keys or configuration.

> [!IMPORTANT]
> AI requires Raycast Pro subscription. Check access with `environment.canAccess(AI)`.

## AI.ask

Use in "no-view" commands, callbacks, or effects.

### Basic Usage

```tsx
import { AI, Clipboard } from "@raycast/api";

export default async function Command() {
  const answer = await AI.ask("Suggest 5 jazz songs");
  await Clipboard.copy(answer);
}
```

### With Options

```tsx
const answer = await AI.ask("Explain quantum computing", {
  model: AI.Model.Anthropic_Claude_Sonnet,
  creativity: "medium",
});
```

### Streaming

```tsx
import { AI, showHUD } from "@raycast/api";

export default async function Command() {
  let fullText = "";
  
  const answer = AI.ask("Write a haiku");
  
  answer.on("data", (chunk) => {
    fullText += chunk;
    console.log(chunk);
  });
  
  await answer;
  await showHUD("Done!");
}
```

### Error Handling

```tsx
import { AI, showToast, Toast, environment } from "@raycast/api";

export default async function Command() {
  if (!environment.canAccess(AI)) {
    await showToast({ style: Toast.Style.Failure, title: "AI requires Raycast Pro" });
    return;
  }

  try {
    const answer = await AI.ask("Hello");
  } catch (error) {
    await showToast({ style: Toast.Style.Failure, title: "AI Error", message: String(error) });
  }
}
```

---

## useAI Hook

For React components. Preferred over AI.ask in views.

```tsx
import { Detail } from "@raycast/api";
import { useAI } from "@raycast/utils";

export default function Command() {
  const { data, isLoading } = useAI("Explain React hooks in simple terms");

  return <Detail markdown={data || "Loading..."} isLoading={isLoading} />;
}
```

### With Options

```tsx
const { data, isLoading, revalidate } = useAI(prompt, {
  model: AI.Model.OpenAI_GPT4o,
  creativity: "low",
  stream: true,
});
```

---

## AI.Model

Available models (Raycast falls back if user's selected model unavailable):

### OpenAI
- `OpenAI_GPT4o` - Fast, complex problem solving
- `OpenAI_GPT4o-mini` - Fast, everyday tasks
- `OpenAI_GPT4` - Broad knowledge
- `OpenAI_o1` - Advanced STEM reasoning
- `OpenAI_o3-mini` - Fast STEM reasoning

### Anthropic
- `Anthropic_Claude_Sonnet` - Complex tasks, visual reasoning
- `Anthropic_Claude_Haiku` - Fastest, large context
- `Anthropic_Claude_4_Opus` - Exceptional fluency

### Google
- `Google_Gemini_2.5_Pro` - Complex problem solving
- `Google_Gemini_2.5_Flash` - Fast, well-rounded
- `Google_Gemini_2.0_Flash` - Low-latency, agentic

### Others
- `Perplexity_Sonar` - Search integration
- `Llama3.3_70B` - Open source reasoning
- `DeepSeek_R1` - Matches o1 performance
- `xAI_Grok_3` - Enterprise coding/data

---

## AI.Creativity

Controls randomness/temperature:

| Value | Use Case |
|-------|----------|
| `"none"` | Deterministic, factual |
| `"low"` | Focused, consistent |
| `"medium"` | Balanced |
| `"high"` | Creative, varied |
| `"maximum"` | Most creative |

Or use numeric value 0-2.

---

## AI.AskOptions

| Option | Type | Description |
|--------|------|-------------|
| `model` | AI.Model | Model to use |
| `creativity` | AI.Creativity | Temperature setting |
| `signal` | AbortSignal | Cancel request |
