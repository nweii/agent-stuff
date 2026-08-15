# Lab access control

Read this when the user chooses protected labs or the host already protects internal routes. Public direct-access labs do not need this branch.

## Reuse the host boundary

Apply one policy to the lab section rather than adding protection inside each lab. Prefer the first existing boundary that fits:

1. The codebase's route middleware or authentication system.
2. The hosting platform's deployment or path protection.
3. An identity-aware proxy or access gateway in front of the site.

Record the chosen boundary and its local verification command in the host agents file. Keep `noindex` when appropriate, but treat it only as discovery metadata.

Application-level shared-password handling is a separate authentication feature. Build it only when the user explicitly chooses it and the host already provides secure server-side secrets, sessions, and abuse controls; otherwise shape that work separately instead of inventing auth inside the lab scaffold.

## Protection scope

Protect the `/lab` index and every nested lab route. Include lab-only data endpoints, server actions, source maps, or generated assets when they reveal material the user intends to restrict. Public site assets shared with production stay under their existing policy.

## Verification

Done when an unauthenticated request is denied at both the lab index and one nested route, an authorized request renders both, redirects cannot bypass the boundary, protected supporting endpoints follow the same policy, and no credential appears in source, browser-delivered code, logs, or committed configuration.
