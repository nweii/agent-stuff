# Before and after

The pairs below are real revisions to this owner's public READMEs, with the rule each shows. The last section describes patterns from other well-regarded projects.

## Opening: outcome before mechanism

Before:

> Every gesture is a fix-tap. You hold one finger still, then tap with another. A resting hand cannot make this motion, so the gestures do not fire by accident.

After:

> Trigger an action without taking your hand off the mouse.
>
> Trickpad turns finger gestures on a Magic Mouse or Magic Trackpad into keyboard shortcuts, built-in actions, custom URLs, or executable scripts.

The first draft named an internal term and defended against a concern no reader had raised yet.

## Opening: scope boundary, no owner

Before:

> MCP ServerKit standardizes the server plumbing repeated across the owner's self-hosted MCP repositories.

After:

> MCP ServerKit standardizes recurring server plumbing for long-lived Bun + Express MCP services, usually running in Docker behind a reverse proxy.

A "When to use it" section follows, so a stranger can decide quickly.

## Feature bullet: outcome, not count

Before:

> **Sixteen gestures per device.** Bind taps, swipes, and deliberate motions…

After:

> **Flexible gestures for each device.** Configure taps, swipes, and hold gestures independently for a Magic Mouse and Magic Trackpad.

"Sixteen" sat in a feature lead-in and would change whenever gestures were added. The default gestures table, which is built to be updated, carries the full list.

## Feature bullet: outcome, not controls

Before:

> **Explain what your tags mean.**

After:

> **Matches your tag system.** Your definitions and rules shape which tags fit a note, even when their names alone would suggest something else.

## Feature bullet: accurate model

Before:

> Hold Fn to give any gesture a second action.

After:

> Bind gestures that run only while Fn is held.

The Fn binding does not depend on the plain gesture being bound, so "second action" described a model the app does not follow.

## Privacy: the boundary, not the mechanics

Before:

> It contacts the network only for updates. That means checking whether one exists, and downloading one you choose to install. Automatic checks are off by default… The app never downloads an update without being asked.

After:

> The app has no telemetry, analytics, or crash reporting. It uses the network only for updates.

The removed sentence became false within a day, when the update behaviour changed.

## Install: plain instruction, no personification

Before:

> Three ways in. Whichever you take, the last step is the same: grant Accessibility permission, which is what lets the app send keystrokes.
>
> Gatekeeper stays out of the way for a build you compiled yourself.

After:

> Trickpad requires macOS 13 or later. The first time you run the app, macOS asks for Accessibility permission so it can send keystrokes.
>
> A local build does not require the Gatekeeper steps above, but it still needs Accessibility permission.

## Alarming warning: calm and specific

Before:

> The app is ad-hoc signed and not notarized, so macOS blocks it the first time you open it. Click **Done**, then open System Settings > Privacy & Security.

After:

> …so macOS shows a verification warning the first time you open it. Choose **Done**, not **Move to Trash**. Then open System Settings > Privacy & Security and scroll down to the **Security** section.

## Even comparison

Before:

> An official packaged build requires the Gatekeeper steps above. Building from source requires the Xcode Command Line Tools but skips those steps.

After:

> The official packaged build needs the one-time approval above, after which updates are a download. Building from source needs the Xcode Command Line Tools and a rebuild for every update.

The first version made the free path sound easier by leaving out its ongoing cost.

## Plain words for insider shorthand

Before:

> **Disconnect your host's dashboard build before you turn this on.** Two connected builds are not redundancy. Both run on the same push, both deploy, and whichever finishes last wins.

After:

> **If your host already rebuilds the site when you push, disconnect it from this repo first.** Otherwise both will compete for each deploy.

## Natural sentences over clipped ones

Before:

> By default it sends Return. Bind it to any shortcut you want. It runs in the background with no interface. Clicking is unchanged.

After (the owner's own edit):

> By default it sends Return, but you can bind this to any shortcut you want. It runs in the background with no interface and does not affect normal clicks or existing gestures by default.

Simple English has a floor: once sentences turn staccato, rejoin them.

## Patterns from other projects

Described, not quoted; see each repo for the full text.

- **Category, then outcome.** Maccy opens by calling itself a lightweight clipboard manager for macOS, then says what it keeps and lets you do. cmdk follows its category sentence with the division of labour: you render items, it filters and sorts them.
- **Privacy as a list of services.** Stats says it collects no telemetry or analytics, then lists the exact external APIs it calls and why.
- **A network fallback with its off switch.** Defuddle explains when it contacts a third-party service (only for pages with no usable HTML), names the service, and gives the option that disables it.
- **A boundary with its cost.** Dataview says its regular queries are sandboxed and cannot harm the vault, and adds that the trade is being more limited.
- **An install path demoted in the open.** ripgrep kept its snap instructions but says plainly they are no longer recommended, so readers who find snap elsewhere know why.
- **Limits next to the pitch.** np places a short "Why not" list right after its reasons to use it; ripgrep answers "Why shouldn't I use ripgrep?" and sends readers who need portability back to grep.
- **Concept, then a concrete case.** QuickAdd defines each building block in one sentence, then gives one specific use for it.
- **FAQ as question and short answer.** cmdk answers a feature question with "No", its performance ceiling, and where to read about bringing your own.
- **Proof with its conditions.** uv captions its benchmark chart with the test conditions (a warm cache, the dataset used).
- **Front door once a docs site exists.** Sonner's README keeps a demo, a one-line identity, install, the smallest usage sample, and a docs link. Obsidian Web Clipper replaced about 250 lines of template docs with a link, to avoid duplicating its help site.
