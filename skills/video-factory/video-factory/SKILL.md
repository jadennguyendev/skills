---
name: video-factory
description: Retired - video-factory is replaced by the movie-factory Claude Code plugin. Use when the user asks for video-factory or one of its old skills (story-writer, screen-adapter, narration-script, shot-list, script-qa, tts, vertical-short), or wants to start or continue a video, film, narration or Short with it. Tells the user it is retired and how to install movie-factory.
---

# video-factory is retired

video-factory is retired and no longer maintained. Use the **movie-factory** Claude Code plugin instead: https://github.com/jadennguyendev/movie-factory (a private repo). It is built on the video-factory skills and takes a YouTube channel's videos from pitch to finished cut.

Tell the user exactly that, give them the install steps below, and stop. Do not try to run the old pipeline: its skills are gone (they live on in this repo's git history).

## Install movie-factory

movie-factory installs from its own marketplace, from a clone. The clone becomes the engine home, so keep it somewhere stable:

```sh
gh repo clone jadennguyendev/movie-factory ~/movie-factory
claude plugin marketplace add ~/movie-factory
claude plugin install movie-factory@movie-factory
```

Then run its setup tiers (`sh ~/movie-factory/tools/setup.sh core`, then `voice` and `music`) as the Install section of its README describes.

Once movie-factory is installed, remove this pointer:

```sh
npx skills remove video-factory
```
