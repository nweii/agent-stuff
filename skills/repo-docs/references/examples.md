# Before and after

These fictional examples demonstrate README writing judgments. Adapt their wording only after checking the behaviour of the project being documented. The last section describes patterns from other well-regarded projects.

## Opening: outcome before mechanism

Before:

> Every recording is a clip-session. The recorder combines an input stream with a capture buffer. Background noise cannot start a session because capture requires a button press.

After:

> Record a voice memo without leaving the app you are using.
>
> This menu bar recorder captures audio from your chosen microphone when you press a keyboard shortcut.

The first draft named an internal term and defended against a concern no reader had raised yet.

## Opening: scope boundary, no owner

Before:

> This deployment toolkit packages the setup repeated across the owner's web services.

After:

> This deployment toolkit provides health checks, request logging, and graceful shutdown for persistent web services running in containers.

A "When to use it" section follows, so a stranger can decide quickly.

## Feature bullet: outcome, not count

Before:

> **Twelve export presets.** Export images at different sizes and quality levels…

After:

> **Reusable export settings.** Save an image size, format, and quality level as a preset for later exports.

The preset count can change without changing the capability. Put the full list in a reference table that is easy to keep current.

## Feature bullet: outcome, not controls

Before:

> **Set your search folders.**

After:

> **Search the folders you choose.** Include shared reference folders and exclude archives from search results.

## Feature bullet: accurate model

Before:

> Add a schedule to give any saved report a second way to run.

After:

> Run a saved report on a schedule, whether or not you also run it manually.

Scheduled runs do not depend on manual runs, so "second way" implies a dependency the software does not have.

## Feature bullet: meaningful choice

For a service with configurable access:

Before:

> **Read and write access.** Clients can read and edit calendar events.

After:

> **Configurable permissions.** Choose read-only access or allow connected clients to create and edit events.

The lead-in names the choice; the support explains its effect. Use it only when those permission modes exist.

## Feature lead-ins: useful overview and concrete support

Read the bold lead-ins alone for an overview, then read the support for the reason each capability matters:

> - **Include less-used sources.** Balance frequently searched folders with a sample of the rest, so older reference material still gets considered.
> - **Configuration in one readable file.** Inspect, edit, and back up your settings without exporting them from a dashboard.
> - **Protect documents from conflicting edits.** Version checks reject a save when another editor has changed the document since it was loaded.

Each bullet has one main point. The support explains a consequence, a practical use, or the protection behind a claim.

Keep the explanation as strong as the lead-in. A word such as "Flexible" gives little to a scanning reader; a controls bullet that accumulates unrelated settings can hide its main point. A technical feature list can use literal capabilities as lead-ins when those terms help its intended readers decide.

## Privacy: control and access

For a self-hosted service:

Before:

> Only you have access. The project maintainer has no access to your data.

After:

> Self-hosted and under your control. You control the server, credentials, and which clients can connect. Authorized clients receive the data they request; a hosting provider runs the server if you deploy it on hosted infrastructure.

This describes ownership and access without introducing the author into product copy. Verify each boundary against the deployment and client model; self-hosting alone does not establish exclusive access.

## Privacy: the boundary, not the mechanics

Before:

> It contacts the network only for updates. That means checking whether one exists, and downloading one you choose to install. Automatic checks are off by default… The app never downloads an update without being asked.

After:

> The app has no telemetry, analytics, or crash reporting. It uses the network only for updates.

The automatic-update details belong in the update settings reference, where they can be maintained alongside the controls.

## Install: plain instruction, no personification

Before:

> Three ways in. Whichever you take, the last step is the same: grant Accessibility permission, which is what lets the app send keystrokes.
>
> Gatekeeper stays out of the way for a build you compiled yourself.

After:

> The utility requires macOS 13 or later. The first time you run the app, macOS asks for Accessibility permission so it can send keystrokes.
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

> By default it checks every hour. Pick any interval you want. It runs in the background. Notifications are off.

After:

> It checks for changes hourly by default, but you can choose another interval. It runs in the background and sends notifications only if you enable them.

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
